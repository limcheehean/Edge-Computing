# Code adapted from https://github.com/Uberi/speech_recognition/blob/master/examples/background_listening.py
import speech_recognition as sr

wake_word = "OK Google"

def callback(recognizer, audio):
    try:
        speech = recognizer.recognize_google(audio)
        if wake_word.lower() in speech.lower():
            print(f"{wake_word} detected!")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


r = sr.Recognizer()
m = sr.Microphone()
with m as source:
    r.adjust_for_ambient_noise(source)

print("Begin listening...")
stop_listening = r.listen_in_background(m, callback)

while True:
    pass

