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

backgroundMusic = ['https://www.youtube.com/watch?v=sqVARC8zTmY']
SFX = ['https://www.youtube.com/watch?v=I1ab_WQ9gVY']

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
	print("\nFiles correspondent to directory " + dirPath)
	print(os.listdir(path=dirPath))
	print("")

def getSeconds(timestamp):
	dt = datetime.datetime.strptime(timestamp, "%M:%S")
	return int(dt.minute*60 + dt.second)

def getVideoLength(video_path):
	command = ['ffprobe', '-v', 'fatal', '-show_entries', 'stream=width,height,r_frame_rate,duration', '-of', 'default=noprint_wrappers=1:nokey=1', video_path]
	ffmpeg = subprocess.Popen(command, stderr=subprocess.PIPE,stdout = subprocess.PIPE )
	out, err = ffmpeg.communicate()

	if err:
		print(err)
	
	return int((out.decode().split('\n')[3]).split('.')[0])

def getBackgroundPath():
	backgroundPath = "./backgroundMusic/" + input("Enter Background Music Filename: ") + ".mp4"
	if not os.path.exists(backgroundPath):
		print("Couldn't find Background with such a name")
		return getBackgroundPath()
	return backgroundPath
	
def userSelections():

	#Configure This Later
	#videoPath = input("Enter Video Path: ")
	videoPath = "./tateOutput.mp4"

	printFiles("./backgroundMusic/")
	backgroundPath = getBackgroundPath()

	backgroundTime = getSeconds(input("Enter Background Music Start Time (MM:SS): "))
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

def getFFMPEGMix(videoPath,backgroundPath, backgroundTime, backgroundPower, SFXInfo):
	
	# Get input command
	# -i vidPath.mp4 -i bckgrnd.mp4 -i sfx1.mp4 -i sfx2.mp4 ... -i sfxn.mp4
	inputCommand = "-i " + videoPath + " -i " + backgroundPath
	for SFXPath, _ in SFXInfo:
		inputCommand += " -i " + SFXPath
	
	vidLen = getVideoLength(videoPath)
	n = SFXInfo.length

	filterCommand = "" 
	factorialSection = "[0][a]"
	inc = 2
	for SFXPath, SFXTime in SFXInfo:
		filterCommand += "[{}] adelay={}|{} [{}];".format(str(inc),str(SFXTime * 1000),str(SFXTime * 1000),str(n + inc))
		factorialSection += "[{}]".format(str(n+inc))
		inc += 1
	filterCommand += "[1] atrim=end={}:atrim=start={}:volume={} [a];".format(str(backgroundTime + vidLen - 0.2),str(backgroundTime),str(float(backgroundPower/100)))
	filterCommand += "{} amix=inputs={}:duration=longest [audio_out]".format(factorialSection,n + 2)
	
	fullCommand = '{} -filter_complex "{}" -map 0:v -map "[audio_out]"'.format(inputCommand, filterCommand)

	# Get filter_complex command
	# filter_complex "[2] adelay=SFXTime*1000|SFXTime*1000 [n+2];
	#		  [3] adelay=SFXTime*1000|SFXTime*1000 [n+3];
	#		  ...
	#		  [n+1] adelay=SFXTime*1000|SFXTime*1000 [n+n+1];
	#		  [1] atrim=end=backgroundTime + vidLen - 0.2:atrim=start=backgroundTime:volume=float(backgroundPower/100) [a];
	#		  [0][a][n+2][n+3]...[n+n+1]amix=inputs=n+2:duration=longest [audio_out]"
	#		  -map 0:v -map "[audio_out]"

	return fullCommand 

def mergeAudios(videoPath, backgroundInfo, SFXInfo):

	command = "ffmpeg " + getFFMPEGMix(videoPath, *backgroundInfo, SFXInfo) + " -y tateSFX.mp4" 
	os.system(command)

	print("Successfully created video at ./tateSFX.mp4")

downloadAudios(backgroundMusic,0)
downloadAudios(SFX,1)

videoPath, backgroundInfo, SFXInfo = userSelections()
mergeAudios(videoPath, backgroundInfo, SFXInfo)
