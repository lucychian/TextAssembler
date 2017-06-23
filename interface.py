from flask import Flask
from flask import request
from flask import render_template
from dbgraph import GetTextFromOverlaps
import urllib


app = Flask(__name__)


#Home page
@app.route('/')
def index():
  return render_template("index.html")

#Results page
@app.route("/results", methods=['GET','POST'])
def results():
  strings = request.form['strings']

  #parse data
  data = [x.strip() for x in strings.split("\n")]

  #assemble fragments
  result = GetTextFromOverlaps(data)

  #display on results page
  return render_template("results.html", results=result)
  

if __name__ == "__main__":
  app.run()
