from gtts import gTTS 
import os 
from playsound import playsound


def bottalk(text:str):
    tts = gTTS(text, tld = 'com.vn', lang = 'vi')

    tts.save('hello2.wav')

    playsound('hello2.wav')

if __name__ == "__main__": 
    bottalk("em chào anh ạ")