from serial import Serial, SerialException
import speech_recognition as sr
from gtts import gTTS
from os import path
import playsound
import winsound
import os.path
import random
import time
import gc
import os

class SpeechToText:
    def __init__(self):
        gc.collect()

        self.ser = None

        self.SerialSetup()
        
        self.r = sr.Recognizer()

        self.TTS = TextToSpeech()

        self.keywords = [("jarvis", 0.95), ("hey jarvis", 0.95), ]

        with sr.Microphone() as self.source:
            self.r.adjust_for_ambient_noise(self.source)

##        print("Hello")

        option = random.choice([1, 2, 3])

        self.TTS.PlaySound("Startup" + str(option), ".wav")

        self.TTS.PlaySound("BeginSetup", ".mp3")

        stop_listening = self.r.listen_in_background(self.source, self.callback)
##        time.sleep(1000000)
        #Instead of this time.sleep forever, we will have the kivy gui running
        
##    def SerialSetup(self) :
##        '''Connects to the desired device'''
##        
##        try:
##            self.ser = Serial("COM6", 115200, timeout = 0)
##        except SerialException:
##            print("Port is already open.\n")
##            return None
##        except TypeError:
##            print("The device has been disconnected!\n")
##            return None
##        else:
##            pass
##            print("Connected to {}".format(ser.port))
##        finally:
##            return True

    def SerialSetup(self, ser):
        self.ser = ser

##    def JarvisOn(self):
##        try:
##            self.ser.write(b'3')
##        except SerialException:
##            stop_listening(wait_for_stop=False)
##            print("Failed to write!\n")
##            return False
##        return True
##
##    def JarvisOff(self):
##        try:
##            self.ser.write(b'2')
##        except SerialException:
##            stop_listening(wait_for_stop=False)
##            print("Failed to write!\n")
##            return False
##        return True
##
##    def LEDOn(self):
##        try:
##            self.ser.write(b'1')
##        except SerialException:
##            print("Failed to write!\n")
##            return False
##        return True
##
##    def LEDOff(self):
##        try:
##            self.ser.write(b'0')
##        except SerialException:
##            print("Failed to write!\n")
##            return False
##        return True

    def callback(self, recognizer, audio):
        try:   
            speech_as_text = recognizer.recognize_sphinx(audio, keyword_entries=self.keywords)
            print(speech_as_text)

            self.recognize_main()

        except sr.UnknownValueError:
            print("Oops! Didn't catch that")


    def recognize_main(self):
##        print("Jarvis is listening")
##        self.JarvisOn()
        
        if not self.TTS.CreateMP3("Jarvis", "Hey. I'm listening."):
            self.TTS.PlaySound("Jarvis", ".mp3")

        Flag = True

        audio = self.r.listen(self.source)
        
        while True:
            if not Flag:
                while True:
                    data = self.r.recognize_sphinx(audio)

                    if "jarvis" in data or "hey jarvis" in data:
##                        print("Jarvis is listening")
##                        self.JarvisOn()
                        
                        if not self.TTS.CreateMP3("Jarvis", "Hey. I'm listening."):
                            self.TTS.PlaySound("Jarvis", ".mp3")
                            
                        break
                    else:
                        audio = self.r.listen(self.source)

                audio = self.r.listen(self.source)

            Flag = False
            
            try:  
                data = self.r.recognize_sphinx(audio)
                
                if "cal" in data or "calibrate" in data:
                    print("Turning LED on!")
##                    self.LEDOn()
##                    self.JarvisOff()

                    #Send the calibrate signal

                    if not self.TTS.CreateMP3("Calibrate", \
                                              "Drone is now calibrating. Please wait."):
                        self.TTS.PlaySound("Calibrate", ".mp3")          
                    
                elif "shut down" in data:
                    print("Turning LED off!")
##                    self.LEDOff()
##                    self.JarvisOff()

                    #Send the abort signal
                    
                    if not self.TTS.CreateMP3("Abort", \
                                              "Abort. Abort. Dewey down."):
                        self.TTS.PlaySound("Abort", ".mp3")
                        
##                elif "spear" in data:
##                    try:
##                        self.ser.write(b'4')
##                    except SerialException:
##                        print("Failed to write!\n")
##                    finally:
##                        self.JarvisOff()
##                elif "exit" in data:
####                    print("Exiting...")
##
##                    if not self.TTS.CreateMP3("Exit", \
##                                              "Goodbye."):
##                        self.TTS.PlaySound("Exit", ".mp3")
##                    
##                    os._exit(0)
                else:
##                    print("This is the data: {}".format(data))
##                    self.JarvisOff()
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

    def _TTSSetup(self):
        myTTS = gTTS(text = "Hey, I'm Jarvis. Just say my name if you need me." + \
                     "Please connect to the transmitter to begin.", \
                     lang = self.language, slow = False)
        myTTS.save("BeginSetup.mp3")

        print("Saved the BeginSetup file.")

    def CreateMP3(self, file_name, text):

        if self._FileCheck(file_name + ".mp3"):
            return False
        
        myTTS = gTTS(text = text, lang = self.language, slow = False)

        myTTS.save(file_name + ".mp3")

        print("Saved the {} file.".format(file_name))

        self.PlaySound(file_name, ".mp3")

        return True

    def PlaySound(self, file_name, file_type):
        playsound.playsound(file_name + file_type, True)

    
if __name__ == "__main__":

    #Test = SpeechToText()
    Test = TextToSpeech()
    
