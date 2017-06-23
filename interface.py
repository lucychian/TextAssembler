from flask import Flask
from flask import request
from flask import render_template
from flask_bootstrap import Bootstrap


app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
  return render_template("index.html")


@app.route("/results", methods=['POST','GET'])
def results():
  strings = request.form['strings']
  return render_template("results.html", results=strings)

if __name__ == "__main__":
  Bootstrap(app)
  app.run()
