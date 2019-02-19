import sounddevice as sd
import numpy as np
import soundfile as sf
import git
import os
import speech_recognition as sr

#file that executes drone movement
f_drone = 'drone_init.txt'
f_sound1 = 'sound1.wav'
f_sound2 = 'sound2.wav'

#reset a file in git
def reset(f_name):
    if os.path.isfile(f_name):
        os.remove(f_name)

reset(f_drone)
reset(f_sound1)
reset(f_sound2)

#find repo as well as add commit message
repo_dir = '~/MediDrone'
commit_message = 'drone_init.txt sent'

#function to push all
def git_push():
    try:
        repo = git.Repo(repo_dir)
        repo.git.add('--all')
        repo.index.commit(commit_message)
        origin = repo.remote(name='origin')
        origin.push()
    except:
        print('error pushing')
    finally:
        print('done push!')

#sample rate same as necessary by the inbuilt mic, change as necessary
fs = 48000
sd.default.samplerate = fs

#duration of sound sample, change as necessary
duration = 5

#record sound
print('recording!')
curr_data = sd.rec(int(duration * fs), samplerate=fs, channels=2)
sd.wait(10)

#saving sound file
sf.write(f_sound1, curr_data, fs)


#checking for keywords
r = sr.Recognizer()
s1 = sr.AudioFile(f_sound1)
with s1 as source:
    audio = r.record(source)
print('got here')
print(r.recognize_google(audio))


git_push()
