from flask import Flask
from flask import request
from flask import render_template

from wtforms import Form, TextAreaField, SubmitField

app = Flask(__name__)


class Form(Form):
  strings = TextAreaField('Strings')
  submit = SubmitField('Submit')


@app.route('/', methods=['GET','POST'])
def index():

  form = Form()
  if request.method == 'POST':
    #submit to dbgraph.py
    strings = request.form['strings']
    #return strings
    return render_template("index.html", form=form)
  else:
    return render_template("index.html", form=form)



if __name__ == "__main__":
  app.run()