import moviepy.editor as mp 
import os 

for vid in os.listdir('mp4s'):
	clip = mp.VideoFileClip('mp4s/' + vid)
	clip.write_gif(vid.strip('.mp4') + '.gif')