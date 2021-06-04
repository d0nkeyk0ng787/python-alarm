#! /usr/bin/env python3
import os
import sys
import time
import spotipy
import wolframalpha
import spotipy.util as util
from gtts import gTTS
from random import randrange
from datetime import datetime
from playsound import playsound
from newsapi import NewsApiClient
from spotipy.oauth2 import SpotifyClientCredentials

# These variables must be set in your terminal before the program will work
# Plenty of documentation on the net if you're stuck
# set SPOTIPY_CLIENT_ID=USEYOURCLICENCETID
# set SPOTIPY_CLIENT_SECRET=USEYOURSECRET
# set SPOTIPY_REDIRECT_URI=USEYOURURI

# TODO Add recurring alarm functionality
# TODO Handle for invalid input with sportify or file (s/f) choice
# TODO Make a GUI version

ask = True
alarm_sounded = False

username = 'ENTERYOURUSERNAMEHERE'
scope = 'user-read-private,user-read-playback-state,user-modify-playback-state,user-read-currently-playing'

wolframkey = "ENTERYOURKEYHERE"
newskey = "ENTERYOURKEYHERE"
spotifydevice = "ENTERYOURDEVICEHERE"
spotifypl = "ENTERYOURPLAYLISTIDHERE"
audiofile = "ENTERYOURFILENAMEHERE"
town = "ENTERYOURTOWNHERE"
country = "ENTERYOURCOUNTRYHERE"

try:
	token = util.prompt_for_user_token(username, scope)
except:
	os.remove(f".cache-{username}")
	token = util.prompt_for_user_token(username, scope)

class Gets:

	def weather(self):
		self.client = wolframalpha.Client(wolframkey)
		self.res = self.client.query(f"{town} weather")
		self.wolfram_res = next(self.res.results).text

	def news(self):
		self.nc = NewsApiClient(api_key=newskey)
		self.hl = self.nc.get_top_headlines(sources='news-com-au') # The source can be pretty much any news outlet
		self.a = self.hl['articles']


# Get our spotify tracks from our playlist, put them in a list
# Pick a random song from that list to play
# In random order add our songs to the queue
def sp_usage(pl_id):

	sp = spotipy.Spotify(auth=token)
	t_uris = []

	pl_results = sp.playlist_tracks(pl_id)
	pl_results = pl_results['items']

	for i in pl_results:
		t_uris.append(i['track']['uri'])

	item = randrange(len(t_uris))
	sp.start_playback(uris=[t_uris[item]],device_id=spotifydevice)

	for i in range(len(t_uris)):
		rand_i = randrange(len(t_uris))
		sp.add_to_queue(t_uris[rand_i],device_id=spotifydevice)

# Perform the following after the sound_alarm tasks have been executed
def post_choice():

	g = Gets()
	g.weather()
	g.news()
	print(g.wolfram_res)
	w = gTTS(text="Hello "+name+". The weather in "+town+" is "+g.wolfram_res, lang="en", slow=False)
	w.save("weather.mp3")
	playsound("weather.mp3")
	s = f"The news headlines for {country} are as follows, "
	for i in g.a:
		s = s + i["title"] + ', '
	print(s)
	n = gTTS(text=s, lang="en", slow=False)
	n.save("news.mp3")
	playsound("news.mp3")
	alarm_sounded = True
	
# Perform the following tasks when the alarm conditions are met
def sound_alarm(alarm, twelve_time):

	if alarm == twelve_time:
		print("Your alarm is sounding "+name+", wake up")
		asounding = gTTS(text="Your alarm is sounding "+name+", wake up", lang="en")
		asounding.save("sounding.mp3")
		playsound("sounding.mp3")
		if sf.lower() == 's':
			sp_usage(f'spotify:playlist:{spotifypl}')
			post_choice()
		elif sf.lower() == 'f':
			os.startfile(audiofile)
			post_choice()

while ask:

	use = input("Would you like to set an alarm? (y/n): ")
	sf = input("Would you like to play your spotify playlist or a file? (s/f): ")	
	name = input("How would you like to be greeted? (E.G Mr Smith, Ms Smith): ")

	# Definately a better way to do this, will probably write it more efficiently at some point
	if use.lower() == 'y':
		h = input("What hour would you like your alarm set at? (01-12): ")
		m = input("What minute(s) would you like your alarm set at? (00-59): ")
		ap = input("Would you like that at AM or PM? ")

		if h.isdigit() and m.isdigit():
			a = h + ":" + m + " " + ap.upper()
			print(f"Your alarm is set for {a}")
			while alarm_sounded == False:
				time = datetime.now().time()
				twelve_time = time.strftime("%I:%M %p")
				sound_alarm(a, twelve_time)
				if alarm_sounded == True:
					break
		else:
			print("Please enter a valid integer for the hour and minutes")
	else:
		print("Goodbye!")
		ask = False
	break
		