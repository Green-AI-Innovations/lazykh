import subprocess


def Videofinisher(path,file_name):

  command = "ls | ffmpeg -r 30 -f image2 -s 1920x1080 -i "+path+file_name+"_frames/f%06d.png -i "+path+file_name+".wav -vcodec libx264 -b 4M -c:a aac -strict -2 "+file_name+"_final.mp4  > /dev/null 2>&1"
  try:
      subprocess.call(command, shell=True)
      print('Video created')
  except subprocess.CalledProcessError as e:
      print('Error creating video:', e)
  print('Video created')