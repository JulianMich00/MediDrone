import sounddevice as sd
import numpy as np
import soundfile as sf
import git

repo_dir = '~/MediDrone'
commit_message = 'added sound file to server from recording_sound.py'

def git_push():
    try:
        repo = git.Repo(repo_dir)
        print('after repo')
        repo.git.add('--all')
        print('after add')
        repo.index.commit(commit_message)
        origin = repo.remote(name='origin')
        origin.push()
    except:
        print('error pushing')
    finally:
        print('done push!')

fs = 48000
sd.default.samplerate = fs


duration = 3


curr_data = sd.rec(int(duration * fs), samplerate=fs, channels=2)
sd.wait(10)

f_name = 'new_sound_file.wav'

sf.write(f_name, curr_data, fs)

git_push()
