# importing Flask and other modules
from flask import Flask, request, render_template
import os
import re
from bs4 import BeautifulSoup
import urllib.request as urllib2
from urllib.request import urlretrieve
 
# Flask constructor
app = Flask(__name__)  
 
# A decorator used to tell the application
# which URL is associated function
@app.route('/', methods =["GET", "POST"])
def gfg():
   if request.method == "POST":
      # getting input with name = fname in HTML form
      first_name = request.form.get("fname")
      # getting input with name = lname in HTML form
      last_name = request.form.get("lname")

      base_url = 'https://papers.neurips.cc'
      url = base_url + '/paper/{}'.format(last_name)
      soup = BeautifulSoup(urllib2.urlopen(url), "html.parser")
      papers = [x for x in soup.find_all('li') if x.find('a')]
      paper = papers[-1]
      title = paper.find('a').text
      abstract_url = base_url + paper.find('a')['href']
      paper_url = abstract_url.replace('hash','file').replace('Abstract', 'Paper').replace('html', 'pdf')
      os.makedirs('neurips_papers', exist_ok=True)
      path = 'neurips_papers/{}.pdf'.format(title)
      urlretrieve(paper_url, path)
      return "Downloading paper: " + title
   return render_template("form.html")
 
if __name__=='__main__':
   app.run()