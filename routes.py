from application import app
from flask import Flask
from flask import render_template, flash, redirect, request, url_for, jsonify, session
from wtforms import Form, StringField, SubmitField
from wtforms.validators import DataRequired

from route import dashboard, channel



# Request User name

class UsernameForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('')

@app.route("/", methods=['GET', 'POST'])
def index():

	#verify if user already has active session 
	#if 'username' in session:
	#	flash('Welcome back ' + session['username'] +'!', 'alert alert-success')
	#	return redirect(url_for('dashboard'))


	form = UsernameForm(request.form)

	if request.method == 'POST' and form.validate():
		username = form.username.data
		session['username'] = username

		#TODO: double check existing username

		flash('Welcome ' + session['username'] +'!', 'alert alert-success')
		return redirect(url_for('dashboard'))

	return render_template('index.html', form=form, is_homepage=True)