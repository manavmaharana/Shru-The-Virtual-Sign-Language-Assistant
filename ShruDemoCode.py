import time
import string
import numpy as np
from moviepy.editor import *
import subprocess

try:
    import azure.cognitiveservices.speech as speechsdk

except ImportError:
    print("""Importing the Speech SDK for Python failed. Refer to https://docs.microsoft.com/azure/cognitive-services/speech-service/quickstart-python for installation instructions.""")
    import sys
    sys.exit(1)

def extract_audio(video,output):
    command = "ffmpeg -y -i {video} -ab 160k -ac 2 -ar 44100 -vn {output}".format(video=video, output=output)
    subprocess.call(command,shell=True)

speech_key, service_region = "subscriptionkey", "region"

extract_audio('Input.mp4','OutputAudio.wav')

audiofilename = "OutputAudio.wav"

def speech_recognize_continuous_from_file():
    """performs continuous speech recognition with input from an audio file"""
    # <SpeechContinuousRecognitionWithFile>
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    audio_config = speechsdk.audio.AudioConfig(filename=audiofilename)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    done = False

    def stop_cb(evt):
        """callback that signals to stop continuous recognition upon receiving an event `evt`"""
        print('CLOSING on {}'.format(evt))
        nonlocal done
        done = True

    all_results = []

    def handle_final_result(evt):
        all_results.append(evt.result.text)

    speech_recognizer.recognized.connect(handle_final_result)
    # Connect callbacks to the events fired by the speech recognizer
    speech_recognizer.recognizing.connect(lambda evt:print('RECOGNIZING: {}'.format(evt)))
    speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt)))
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
    # stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Start continuous speech recognition
    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(.5)

    #print("Printing all results:")
    #print(all_results)

    speech_recognizer.stop_continuous_recognition()
    # </SpeechContinuousRecognitionWithFile>

    return all_results

def main():
    results = speech_recognize_continuous_from_file()
    gif_db=['welcome to hackathon 2020',
            'our one week hackathon represents what is core to both our mission as well as our culture',
            'im always inspired by the passion',
            'creativity',
            'the ingenuity of a hack teams using microsoft'
            ,'as a platform to make a difference']


    bigstr = ','.join(results)
    bigstr=bigstr.replace(',','.')
    hh = bigstr.split('.')
    hh = [item.replace(",", "") for item in hh]
    hh = list(filter(None, hh))
    ans = [x.strip(' ') for x in hh]

    x=0
    size = len(ans)
    index_arr = np.zeros(len(ans))
    clip = [None]*size
    loadclip = [None]*size


    for i in ans:

        a=i.lower()
        for c in string.punctuation:
            a = a.replace(c, "")

        if a.lower() in gif_db:
            print(a)
            index_arr[x] = gif_db.index(a)
            clip[x] = str(gif_db[gif_db.index(a)])

        else:
            print('No Match in DB!')
            clip[x]='error'

        x=x+1

    for i in range(size):
        loadclip[i]=VideoFileClip(str(clip[i])+'.mp4')

    final_clip = concatenate_videoclips(loadclip)
    final_clip = final_clip.speedx(factor=3)
    final_clip.write_videofile("Concatenated_mp4s.mp4")


    clip1 = VideoFileClip("Input.mp4")
    clip2 = VideoFileClip("Concatenated_mp4s.mp4")
    clip2 = clip2.resize(0.35)
    clip2 = clip2.set_start(2)
    video = CompositeVideoClip([clip1, clip2.set_position(("right", "bottom"))])

    video.write_videofile("Output.mp4")





if __name__ == "__main__":
    main()
