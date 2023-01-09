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

backgroundMusic = [,]
SFX = ['https://www.youtube.com/watch?v=I1ab_WQ9gVY',]

# soundType = 0 --> BackgroundMusic	
# soundType = 1 --> SFX	
def downloadAudios(URLs,soundType):
	if not os.path.exists('./backgroundMusic'):
		os.makedirs('./backgroundMusic')
	if not os.path.exists('./SFX'):
		os.makedirs('./SFX')

	for url in URLs:
		yt = YouTube(url)

		if soundType==0:
			title = yt.title.replace(" ","-")[0:10]
			dirPath = './backgroundMusic'
		else:
			title = yt.title.replace(" ","-")[0:5]
			dirPath = './SFX'

		if os.path.exists(dirPath + '/' + title + '.mp4'):
			print("Background/SFX " + title + " --> Already Downloaded")
		else:
			video_stream = yt.streams.get_audio_only()
			print(video_stream)
			video_stream.download(output_path=dirPath,filename=title + '.mp4')
			print("Background/SFX " + title + " --> Successfully Downloaded")
def printFiles(dirPath):
	print("\nFiles correspondent to directory " + dirPath + "\n" + os.listdir(path=dirPath))

def userSelections():

	#Configure This Later
	#videoPath = input("Enter Video Path: ")
	videoPath = "./tateOutput.mp4"

	printFiles("./backgroundMusic/")
	backgroundPath = "./backgroundMusic/" + input("Enter Background Music Filename: ")

	backgroundTime = input("Enter Background Music Start Time (MM:SS): ")
	backgroundPower = int(input("Enter Background Music Volume (%): "))

	printFiles("./SFX/")
	SFXInfo = []

	while(True):
		SFXFile = input("Enter SFX Filename: ")
		if SFXFile == "":
			break
		else:
			if not os.path.exists("./SFX/" + SFXFile + ".mp4"):
				print("Couldn't find SFX with such a name")
				continue

			SFXTime = float(input("Enter Time For SFX Appearance In Original Video (SS.MSS): "))
			SFXInfo.append(["./SFX/" + SFXFile + ".mp4" , SFXTime])

	return videoPath, [backgroundPath, backgroundTime, backgroundPower], SFXInfo

downloadAudios(backgroundMusic,0)
downloadAudios(SFX,1)

videoPath, backgroundInfo, SFXInfo  = userSelections()

