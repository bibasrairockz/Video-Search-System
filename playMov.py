from moviepy.editor import VideoFileClip 
import pygame
import os

def ply(s,e,r,f,pat):
    n=s/f
    m=e/f
    print(n, m)
    p = pat+".mp4"
    dir=os.path.join("C:\\Users\\bibas\\Music\\videos",p)
    clip = VideoFileClip(dir).subclip(n,m)
    
    #clip.preview()
    clip.write_videofile(f"C:\\Users\\bibas\\Music\\result\\{pat}{r}.mp4")


"""
x = int(input('start:'))
y = int(input('stop:'))

ply(840,990,0)
ply(1840,1990,1)
"""
