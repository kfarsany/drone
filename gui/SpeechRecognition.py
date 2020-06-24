from pynput.mouse import Button, Controller
from serial import Serial, SerialException
import SerialWrite_DirectGUI as Direct
import speech_recognition as sr
from gtts import gTTS
from os import path
import threading
import playsound
import winsound
import os.path
import random
import time
import gc
import os

#Used for Jarvis to turn on/off camera sound
global sound
sound = 0

class SpeechToText:
    def __init__(self):
        gc.collect()

        self.ser = None

        self.Direct = None

        self.mouse = Controller()
        
        self.r = sr.Recognizer()

        self.r.energy_threshold = 600

        self.TTS = TextToSpeech()

        self.keywords = [("jarvis", 0.95), ("hey jarvis", 0.95), ]

        with sr.Microphone() as self.source:
            self.r.adjust_for_ambient_noise(self.source)

        self.TTS.CreateMP3("BeginSetup", "Hey, I'm Jarvis. Just say my name if you need me." + \
                     "Please connect to the transmitter to begin.", False)
##        self.TTS.CreateMP3("Calibrate2", "Calibration complete. Please quit if "
##                           + "you have aborted.", False)


##        option = random.choice([1, 2, 3])
##
##        t = threading.Thread(target = self.TTS.PlaySound, \
##                             args = ("Startup" + str(option), ".wav"))
##        t.start()

        t = threading.Thread(target = self.TTS.PlaySound, \
                             args = ("BeginSetup", ".mp3", 8))
        t.start()

        stop_listening = self.r.listen_in_background(self.source, self.callback)

    def Setup(self, ser: 'serial.serialwin32.Serial', Direct: 'class SerialWrite_DirectGUI.DirectControl'):
        self.ser = ser
        self.Direct = Direct

    def callback(self, recognizer, audio):
        try:   
            speech_as_text = recognizer.recognize_sphinx(audio, keyword_entries=self.keywords)
            print(speech_as_text)

            self.recognize_main()

        except sr.UnknownValueError:
            print("Oops! Didn't catch that")


    def recognize_main(self):
        if not self.TTS.CreateMP3("Jarvis", "Hey. I'm listening."):
            self.TTS.PlaySound("Jarvis", ".mp3")

        Flag = True

        audio = self.r.listen(self.source)
        
        while True:
            if not Flag:
                while True:
                    data = self.r.recognize_sphinx(audio)

                    if "jarvis" in data or "hey jarvis" in data:
                        if not self.TTS.CreateMP3("Jarvis", "Hey. I'm listening."):
                            self.TTS.PlaySound("Jarvis", ".mp3")
                            
                        break
                    else:
                        audio = self.r.listen(self.source)

                audio = self.r.listen(self.source)

            Flag = False
            
            try:  
                data = self.r.recognize_sphinx(audio)
                print("This is what I thought you said: {}".format(data))

                if "rest" in data:
                    if self.ser != None:
                        self.Direct.WriteToBoard(0, 127, 127, 127, 0, 0)
                        if not self.TTS.CreateMP3("Idle", \
                                                  "Dewey is now in sloth mode."):
                            self.TTS.PlaySound("Idle", ".mp3")
                    else:
                        if not self.CreateMP3("Connect", "Sorry, I can't do that right now." \
                                       "Please connect to the transmitter."):
                                self.TTS.PlaySound("Connect", ".mp3")
                elif "shut down" in data:
                    #Send the abort signal
                    if self.ser != None:
                        self.Direct.ESC_ABORT(self.ser)
                        self.Direct.WriteCalibration(self.ser, 0)
                        
                        if not self.TTS.CreateMP3("Abort", \
                                                  "Abort. Abort. Dewey down."):
                            self.TTS.PlaySound("Abort", ".mp3")
                            
                    else:
                        if not self.CreateMP3("Connect", "Sorry, I can't do that right now." \
                                       "Please connect to the transmitter."):
                                self.TTS.PlaySound("Connect", ".mp3")
                            
##                elif "exit" in data:
##                    print("Exiting...")
##
##                    if not self.TTS.CreateMP3("Exit", \
##                                              "Goodbye."):
##                        self.TTS.PlaySound("Exit", ".mp3")
##                    
##                    os._exit(0)
                elif "cam" in data or "camera" in data:
                    global sound
                    if sound:
                        sound = 0
                    else:
                        sound = 1
                else:
                    if not self.TTS.CreateMP3("Invalid", "Sorry, I didn't " + \
                                             "get that. Please use a valid command."): 
                        self.TTS.PlaySound("Invalid", ".mp3")
            except sr.UnknownValueError:  
                print("Sphinx could not understand audio")  
            except sr.RequestError as e:  
                print("Sphinx error; {0}".format(e))

class TextToSpeech():
    def __init__(self):
        self.language = "en"

        if not self._FileCheck("BeginSetup.mp3"):
            self._TTSSetup()

    def _FileCheck(self, file):
        return path.exists(file)

##    def _TTSSetup(self):
##        myTTS = gTTS(text = "Hey, I'm Jarvis. Just say my name if you need me." + \
##                     "Please connect to the transmitter to begin.", \
##                     lang = self.language, slow = False)
##        myTTS.save("BeginSetup.mp3")
##
##        print("Saved the BeginSetup file.")

    def CreateMP3(self, file_name, text, play = True):

        if self._FileCheck(file_name + ".mp3"):
            return False
        
        myTTS = gTTS(text = text, lang = self.language, slow = False)

        myTTS.save(file_name + ".mp3")

        print("Saved the {} file.".format(file_name))

        if play:
            self.PlaySound(file_name, ".mp3")

        return True

    def PlaySound(self, file_name, file_type, delay = 0):
        time.sleep(delay)
        playsound.playsound(file_name + file_type, True)
        return True

def audio():
    global sound
    return sound

def TabCheck():
    global switch
    curr_switch = switch
    switch = False
    return curr_switch, tab

    
if __name__ == "__main__":

    #Test = SpeechToText()
    Test = TextToSpeech()
    
