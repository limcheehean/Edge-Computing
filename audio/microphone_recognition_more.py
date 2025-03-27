from time import time

import speech_recognition as sr

# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)

apis = [
    {
        "name": "Sphnix",
        "recognise": lambda a: r.recognize_sphinx(a)
    },
    {
        "name": "Google",
        "recognise": lambda a: r.recognize_google(a)
    },
    {
        "name": "Wit.ai",
        "recognise": lambda a: r.recognize_wit(a, key="PMAWWIXPXDFK47FFFYCXM3J2RIFSIL6T")
    },
    {
        "name": "Houndify",
        "recognise": lambda a: r.recognize_houndify(a, client_id="K5BUs4U9r-hXwtSABfLScQ==", client_key="x69HwXq1JIp9X8Ly_hvP9AKrrRrkRhkqKHvHB3RcBJWptF-KqPYwSpDzS7yf-6U4LmWxWJaDYhTvDulmbKSy7g==")[0]
    },
    {
        "name": "Whisper",
        "recognise": lambda a: r.recognize_whisper(a, language="english")
    }
]

results = {}

for api in apis:
    start = time()
    name, recognise = api["name"], api["recognise"]
    try:
        print(f"{name} thinks you said {recognise(audio)}")
        duration = round(time() - start, 2)
        print(f"Time taken for {name} recognition: {duration} seconds")
        results[name] = duration
    except sr.UnknownValueError:
        print(f"{name} could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from {name} {e}")

print(f"{'API'.center(10)} | Time Taken")
print("-" * 30)
for key, value in results.items():
    print(f"{key.center(10)} | {value} seconds")
