from application import app
from flask import Flask
from flask import render_template, flash, redirect, request, url_for, jsonify, session
from wtforms import Form, StringField, SubmitField
from wtforms.validators import DataRequired
from flask_socketio import SocketIO, emit, send
#from flask_cors import CORS, cross_origin

#cors = CORS(app, resources={r"/channel/*": {"origins": "http://127.0.0.1:5000/"}})

socketio = SocketIO(app)


class ChannelForm(Form):
    channel_name = StringField('Channel Name', validators=[DataRequired()])
    submit = SubmitField('')

#Offer to create channel

@app.route("/channel/add", methods=['GET', 'POST'])
def add_channel():

	#verify if user exists
	if 'username' in session:

		channel = []
		form = ChannelForm(request.form)

		#add channel

		if request.method == 'GET':
			return render_template('add_channel.html', form=form)

		if request.method == 'POST' and form.validate():
			channel_name = form.channel_name.data
			#print("Channel Name", channel_name)

			if 'user_channel' in session:
				#print("What is sessoin channel", session['user_channel'])
				session['user_channel'].append(channel_name) 
			else:
				channel.append(channel_name)
				session['user_channel'] = channel

			flash( '"' + channel_name  + '" channel successfully added!', 'alert alert-success') 
			return redirect(url_for('dashboard'))
	else:
		return redirect(url_for('index'))



#Enter a channel - see 100 previous message

#Leave a message

#remember last channel visited



@app.route("/channel/<string:channel_name>", methods=['GET', 'POST'])
def channel_room(channel_name):

	new_participant = session['username']

	#add this channel to this member channels session
	#verify channel isn't already there
	channel = []

	if 'user_channel' in session:
		#print("What is sessoin channel", session['user_channel'])
		session['user_channel'].append(channel_name) 
	else:
		channel.append(channel_name)
		session['user_channel'] = channel


	#collect 100 last messages from channel room
	
	return render_template('channel_room.html')



#get participants
@socketio.on('enter channel')
def channel_participants(json):
	#print("made it to channel_participants function")
	#print('received json: ' + str(json))

	new_participant =  str(json['data'])

	socketio.emit('newParticipant', new_participant);



@socketio.on('chatMessage')
def channel_chats(json):
	#print("made it to channel chats function")
	#print('received json: ' + str(json['data']))


	message =  str(json['data'])

	username = str(json['username'])
	#print('received json usrname: ' + json['username'])

	msg_time = str(json['msg_time'])
	#print('received json mgs time: ' + json['msg_time'])

	all_message = {'message':message, 'username': username, 'msg_time': msg_time }


	socketio.emit('newUserMessage', all_message)


	

