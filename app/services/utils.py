# There is probably a smarter, more efficient way to do this with regex. This runs nearly instantly though, so no big deal.
import re
import wave
import shutil
import time
from fastapi.responses import StreamingResponse
import random
import string
import os




def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__} took {end_time - start_time} seconds to execute.")
        return result
    return wrapper


def removeTags(script):
  TO_REMOVE = ["[","]","/"]

  newScript = script.replace("-"," ")
  for charToRemove in TO_REMOVE:
      newScript = newScript.replace(charToRemove,"")

  while "<" in newScript:
      start = newScript.index("<")
      end = newScript.index(">")+1
      newScript = newScript[:start]+newScript[end:]
  while "  " in newScript:
      newScript = newScript.replace("  "," ")
  while "\n " in newScript:
      newScript = newScript.replace("\n ","\n")
  while " \n" in newScript:
      newScript = newScript.replace(" \n","\n")
  while newScript[0] == " ":
      newScript = newScript[1:]

  return newScript


def creat_randome_name():
    # Define the length of the random string
    length = 12
    while True:
        # Generate a random string of length 8
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        # Check if a file with that name already exists in the directory
        if not os.path.exists(random_string):
            break
    # Use the unique random string for the file name
    filename = random_string 

    return filename



def save_audio(audio_data, file_path, file_name):
    """
    Save an audio file to a specified path with a given filename.

    Args:
    - audio_data: bytes, the binary data of the audio file to be saved
    - file_path: str, the path to the directory where the audio file should be saved
    - file_name: str, the name of the audio file

    Returns:
    - None
    """

    # Concatenate the file path and file name to create the full file path
    full_path = file_path + file_name+'.wav'

    # Load the audio data into an AudioFileClip object
    # Write the audio data to a file
    with open(full_path, 'wb') as f:
        f.write(audio_data)



def delete_cache():
    for filename in os.listdir():
        # Check if the file ends with '_final.mp4'
        if filename.endswith('_final.mp4'):
            file_path = os.path.join(os.getcwd(), filename)
            try:
                # Check if the file is in use
                with open(file_path, 'r'):
                    pass
                # If not in use, delete the file
                os.remove(file_path)
                print(f"{filename} deleted successfully.")
            except PermissionError:
                print(f"{filename} is in use. Skipping deletion.")
            except Exception as e:
                print(f"Error deleting {filename}: {e}")




def get_video_from_file(path):
    # Read the video file as binary data
        def iterfile():  # 
             with open(path+'_final.mp4', mode="rb") as file_like:  # 
                yield from file_like  # 

        return StreamingResponse(iterfile(), media_type="video/mp4")



def delete_temprory_files(folder_path, prefix):
    """
    Deletes all files in a folder that start with a given prefix and end with either ".csv" or ".json".
    """

    transcript=prefix+'.txt'
    os.remove(folder_path+transcript)
    phonemes=prefix+'.json'
    os.remove(folder_path+phonemes)
    audio=prefix+'.wav'
    os.remove(folder_path+audio)
    schedule=prefix+'_schedule.csv'
    os.remove(folder_path+schedule)
    video_without_sound=prefix+'.mp4'
    os.remove(folder_path+video_without_sound)
    # specify the path to delete frames
    frames=prefix+'_frames'
    # remove the directory and all its contents
    shutil.rmtree(frames)


def getFilenameOfLine(line):
    topic = getTopic(line)
    return re.sub(r'[^A-Za-z0-9 -]+', '',  topic.lower())

def getTopic(stri):
    if "[" in stri:
        start = stri.index("[")+1
        end = stri.index("]")
        return stri[start:end]
    else:
        return removeTags(stri)

def capitalize(stri):
    words = stri.split(" ")
    result = ""
    for i in range(len(words)):
        if i >= 1:
            result = result+" "
        w = words[i]
        result = result+w[0].upper()+w[1:]
    return result
