import os 

def makeSubtitlesFile(response=None):
	return "./tateSubtitles.srt"

def generateVisualSubtitles(clipPath, subtitle_file):
	subtitles = "subtitles={}:fontsdir='/usr/share/fonts/truetype/ubuntu':force_style='Alignment=10,FontName=Mercadillo,FontSize=22,OutlineColour=&H00000000,Outline=1.5,PrimaryColour=&H00FFFFFF,Spacing=1.2'".format(subtitle_file)
	print(subtitles)
	command = 'ffmpeg -i {} -vf "{}" -c:v libx264 -crf 18 -c:a copy -y tateOutput.mp4'.format(clipPath, subtitles)

	os.system(command)
	print("Successfully created video at tateOutput.mp4")


clipPath = input("Enter Video Path: ")
generateVisualSubtitles(clipPath, makeSubtitlesFile())
