from application import app
from flask import Flask
from flask import render_template, flash, redirect, request, url_for, jsonify, session
from wtforms import Form, StringField, SubmitField
from wtforms.validators import DataRequired


@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():

	#verify if user exists
	if 'username' in session:
		#Look for existing channels
		channels = []
		
		if 'user_channel' in session:
			#Show existing channels
			channels = session['user_channel']

		return render_template('dashboard.html', channels=channels)

	else:
		return redirect(url_for('index'))



			

		