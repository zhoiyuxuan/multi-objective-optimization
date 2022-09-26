from moviepy.editor import VideoFileClip,CompositeVideoClip
clip1 = VideoFileClip('/Users/tommyzhou/Downloads/animeking.mp4').subclip(0,599)
clip2 = VideoFileClip('/Users/tommyzhou/Downloads/animeking.mp4').subclip(600,1199)
clip3 = VideoFileClip('/Users/tommyzhou/Downloads/animeking.mp4').subclip(1200,1798)

video1 = CompositeVideoClip([clip1])
video1.write_videofile('animeking1.mp4')

video2 = CompositeVideoClip([clip2])
video2.write_videofile('animeking2.mp4')

video3 = CompositeVideoClip([clip3])
video3.write_videofile('animeking3.mp4')