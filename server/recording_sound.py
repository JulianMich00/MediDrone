import sounddevice as sd
import numpy as np
import soundfile as sf
import git
import os
import speech_recognition as sr
import time 

#sample rate same as necessary by the inbuilt mic, change as necessary
fs = 48000
sd.default.samplerate = fs

#duration of sound sample, change as necessary
duration = 5

#file that executes drone movement
f_drone = 'drone_init.txt'
f_sound1 = 'sound1.wav'
f_sound2 = 'sound2.wav'

#find repo as well as add commit message
repo_dir = '~/MediDrone'
commit_message = 'drone_init.txt sent'

#reset a file in git
def reset(f_name):
    if os.path.isfile(f_name):
        os.remove(f_name)

#function to push all
def GitPush():
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

#conversion between sound file and analysed text
def SpeechAnalysis(input_sound):
    r = sr.Recognizer()
    sound = sr.AudioFile(input_sound)
    with sound as source:
        audio = r.record(source)
    try:
        message = r.recognize_google(audio)
        print(message)
        if ('help' in message) and ('medic' in message):
            GitPush()
            print('sending out drone')
    except:
        print('no voice detected this block')
        
        
reset(f_drone)
reset(f_sound1)
reset(f_sound2)

while True:
    print('recording!')
    curr_data = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    time.sleep(duration)
    print('stopped')
    
    #saving sound file
    sf.write(f_sound1, curr_data, fs)
    sd.wait(10)
    SpeechAnalysis(f_sound1)
    
