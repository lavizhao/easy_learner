#!/usr/bin/python
#coding: utf-8

from flask import Flask
from flask import render_template
from flask import request
from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired
from flask import abort, redirect, url_for

from searcher import search,get_text

from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig
from flask_wtf import Form, RecaptchaField
from wtforms import TextField, HiddenField, ValidationError, RadioField,\
BooleanField, SubmitField, IntegerField, FormField, validators
from wtforms.validators import Required


class search_form(Form):
    name = StringField('', validators=[DataRequired()])


app = Flask(__name__)

Bootstrap(app)
# in a real app, these should be configured through Flask-Appconfig
app.config['SECRET_KEY'] = 'devkey'
app.config['RECAPTCHA_PUBLIC_KEY'] = \
'6Lfol9cSAAAAADAkodaYl9wvQCwBMr3qGR_PPHcw'
    

@app.route('/', methods=('GET','POST'))
def main():
    #return 'Hello World!'
    print("main")
    form = search_form()
    if form.validate_on_submit():
        words = form.name.data
        murl = url_for('fsearch',words=words)
        return redirect(murl)
        
    return render_template('main.html',form=form)

@app.route('/search/<words>')
def fsearch(words):
    print("search")
    form2 = search_form()
    result = search(words)
    for line in result:
        print line[0],line[1]
            
    return render_template('exform.html',words=words,result = get_text(result),form=form2)

    
@app.route('/submit', methods=('GET', 'POST'))
def submit():
    print("submit")
    form = search_form()
    if form.validate_on_submit():
        return redirect('/')
    return render_template('form.html', form=form)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

    
if __name__ == '__main__':
    app.run(debug=True)
