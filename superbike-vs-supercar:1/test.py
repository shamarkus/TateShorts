import json
import io
from google.protobuf.json_format import MessageToJson
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from apiclient.discovery import build
from google.cloud import speech

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
		model = "latest_long",
		enable_word_time_offsets= True,
	)

	response = client.recognize(config=config, audio=audio)
	print(response)	

transcribe_file("tateSound.flac")



