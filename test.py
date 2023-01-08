import os, sys
import requests
import urllib.request
import re
import subprocess
import shlex
import random
import ffmpeg
import srt
import datetime
import json
import math
import google.auth
import io

from pytube import YouTube
from google.protobuf.json_format import MessageToJson
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.cloud import speech

def getWordTime(secondsTime):
	return float(secondsTime.split('s')[0])
def transcribe_file(speech_file):
	client = speech.SpeechClient()

	with io.open(speech_file, "rb") as audio_file:
		content = audio_file.read()

	audio = speech.RecognitionAudio(content=content)
	config = speech.RecognitionConfig(
		encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
		sample_rate_hertz=44100,
		language_code="en-US",
		audio_channel_count = 2,
		model = "video",
		enable_word_time_offsets= True,
	)

	response = client.recognize(config=config, audio=audio)
	response = json.loads(MessageToJson(response._pb))
	
	return makeSubtitlesFile(response)

def makeSubtitlesFile(response):
	entries = []
	contentBuffer = ""
	window_s, window_f = -1, -1 
	segment_duration = 0.40
	index = 1
	
	print(response)

	for result in response.get("results"):
		if "words" in result.get("alternatives")[0]:
			for word in result.get("alternatives")[0].get("words"):

				start_time = getWordTime(word.get("startTime"))
				end_time = getWordTime(word.get("endTime"))
				content = word.get("word")

				contentBuffer += content + " "

#			if end_time - start_time > 0.3:
#				start_time = end_time - 0.3
				# Initializer
				if window_s == -1:
					window_s, window_f = start_time, start_time + segment_duration

				if end_time > window_f:
					entry = srt.Subtitle(index = index, start = datetime.timedelta(seconds=int(window_s),milliseconds=int((window_s - math.floor(window_s))*1000)),end = datetime.timedelta(seconds=int(end_time),milliseconds=int((end_time - math.floor(end_time))*1000)), content = contentBuffer)
					entries.append(entry)
					window_s, window_f = -1, -1
					contentBuffer = ""
					index += 1

	subtitle_file = "./tateSubtitles.srt"

	with open(subtitle_file, "w") as subtitle_file:
		subtitle_file.write(srt.compose(entries))

	return subtitle_file

transcribe_file('/home/shamarkus/TateShorts/the-secrets-of-telegram:f/tateSound.flac')
