from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.cache import Cache
from view_layout import ControllerView, DroneView, DroneAdvView, DocView
import SerialWrite_DirectGUI as Direct
import SerialWrite_RampGUI as Ramp
import SerialSetupGUI as Setup
import SpeechRecognition as Speech
from Map_functions import Mapping
from PIL import Image
import threading
import time
import ImageProcessing
import concurrent.futures

from decimal import *
getcontext().prec = 6

'''Handles Controller Signals'''
##############################################################      
class Controller:
    def __init__(self) -> None:
        #For Connection Setup
        self.Setup = Setup.SerialConnection()
        self.ConnectionSuccess = None
        self.ser = None

        #For Direct Control Signals
        self.DirectControl = Direct.DirectControl()
        
        #Contains all 6 signals shown below
        self.values = None
        self.Throttle = 0
        self.Yaw = 0
        self.Pitch = 0
        self.Roll = 0
        self.AUX1 = 0
        self.AUX2 = 0

        #For Ramping Signals
        self.Ramping = Ramp.Ramping()
        self.Throttle_Ramp = None
        self.Yaw_Ramp = None
        self.Pitch_Ramp = None
        self.Roll_Ramp = None

        #Info Needed for Button Controls
        self.Prev_Val = None

        #Speech Recognition
        self.Speech = Speech.SpeechToText()

    def PortCheck(self) -> list:
        ports = self.Setup.SerialPorts()

        return ports

    def Connect(self, port: str, bauds: int) -> bool:
        self.Setup.Setup(port, bauds)

        Connection = self.Setup.StartConnection()

        if Connection != None:
            self.SetConnection(Connection)
            self.ConnectionSuccess = True
            return True
        return False

    def CheckConnect(self) -> bool:
        return self.ConnectionSuccess

    def SetConnection(self, ser: 'serial.serialwin32.Serial') -> None:
        self.ser = ser
        self.DirectControl.Setup(ser)
        self.Ramping.Setup(ser, self.DirectControl)
        self.Speech.Setup(ser, self.DirectControl)

    def Disconnect(self) -> None:
        self.Setup.EndConnection()

    def DirectValueCheck(self) -> bool:
        '''Sets the desired signals'''
        
        self.values = [self.Throttle, self.Yaw, self.Pitch, \
                       self.Roll, self.AUX1, self.AUX2]
        if all(v >= 0 for v in self.values) and all(v <= 255 for v in self.values):
            if not self.DirectControl.WriteToBoard(self.Throttle, self.Yaw, self.Pitch, \
                                       self.Roll, self.AUX1, self.AUX2):
                return False
            else:
                return True
        return False

    def RampValueCheck(self) -> bool:
        '''Ramps up the desired signals'''
        '''Only one signal can be ramped up at a time!'''
        curr_val = self.Ramping.PreviousValues()

        if len(curr_val) == 0:
            return False
        
        if self.Throttle_Ramp == None and self.Yaw_Ramp == None and\
           self.Pitch_Ramp == None and self.Roll_Ramp == None:
            return False
        
        curr_throttle = curr_val[0]
        curr_yaw = curr_val[1]
        curr_pitch = curr_val[2]
        curr_roll = curr_val[3]

        if self.Throttle_Ramp != None:
            if self.Throttle_Ramp != curr_throttle:
                if self.Throttle_Ramp < curr_throttle:
                    t = threading.Thread(target = self.Ramping.Throttle_Ramp, \
                                         args = (self.Throttle_Ramp, \
                                                 curr_val, "Down"))
                    t.start()
                elif self.Throttle_Ramp > curr_throttle:
                    t = threading.Thread(target = self.Ramping.Throttle_Ramp, \
                                         args = (self.Throttle_Ramp, \
                                                 curr_val, "Up"))
                    t.start()
        if self.Yaw_Ramp != None:
            if self.Yaw_Ramp != curr_yaw:
                if self.Yaw_Ramp < curr_yaw:
                    t = threading.Thread(target = self.Ramping.Yaw_Ramp, \
                                         args = (self.Yaw_Ramp, \
                                                 curr_val, "Down"))
                    t.start()
                elif self.Yaw_Ramp > curr_yaw:
                    t = threading.Thread(target = self.Ramping.Yaw_Ramp, \
                                         args = (self.Yaw_Ramp, \
                                                 curr_val, "Up"))
                    t.start()
        if self.Pitch_Ramp != None:
            if self.Pitch_Ramp != curr_pitch:
                if self.Pitch_Ramp < curr_pitch:
                    t = threading.Thread(target = self.Ramping.Pitch_Ramp, \
                                         args = (self.Pitch_Ramp, \
                                                 curr_val, "Down"))
                    t.start()
                elif self.Pitch_Ramp > curr_pitch:
                    t = threading.Thread(target = self.Ramping.Pitch_Ramp, \
                                         args = (self.Pitch_Ramp, \
                                                 curr_val, "Up"))
                    t.start()
        if self.Roll_Ramp != None:
            if self.Roll_Ramp != curr_roll:
                if self.Roll_Ramp < curr_roll:
                    t = threading.Thread(target = self.Ramping.Roll_Ramp, \
                                         args = (self.Roll_Ramp, \
                                                 curr_val, "Up"))
                    t.start()
                elif self.Roll_Ramp > curr_roll:
                    t = threading.Thread(target = self.Ramping.Roll_Ramp, \
                                         args = (self.Roll_Ramp, \
                                                 curr_val, "Up"))
                    t.start()
                    
        return True


    def Up(self) -> bool:
        if self.Prev_Val[0] < 255:
            NewValue = self.Prev_Val[0] + 1
            if not self.DirectControl.WriteThrottle(NewValue):
                return False
            return True
        return False

    def Down(self) -> bool:
        if self.Prev_Val[0] > 0:
            NewValue = self.Prev_Val[0] - 1
            if not self.DirectControl.WriteThrottle(NewValue):
                return False
            return True
        return False

    def Forward(self) -> bool:
        if self.Prev_Val[2] < 255:
            NewValue = self.Prev_Val[2] + 1
            if not self.DirectControl.WritePitch(NewValue):
                return False
            return True
        return False

    def Backward(self) -> bool:
        if self.Prev_Val[2] > 0:
            NewValue = self.Prev_Val[2] - 1
            if not self.DirectControl.WritePitch(NewValue):
                return False
            return True
        return False

    def Right(self) -> bool:
        if self.Prev_Val[3] < 255:
            NewValue = self.Prev_Val[3] + 1
            if not self.DirectControl.WriteRoll(NewValue):
                return False
            return True
        return False

    def Left(self) -> bool:
        if self.Prev_Val[3] > 0:
            NewValue = self.Prev_Val[3] - 1
            if not self.DirectControl.WriteRoll(NewValue):
                return False
            return True
        return False

    def Hover(self) -> bool:
        if not self.DirectControl.WriteToBoard(0, 125, 131, 135, 0, 0):
            return False
        return True

    def Startup(self) -> bool:
        self.Delay(2)
        self.DirectControl.WriteCalibration(1)
        self.Delay(1)
        self.DirectControl.ESC_Turn_On(1)
        self.DirectControl.WriteCalibration(0)
        return True

    def Abort(self) -> bool:
        self.DirectControl.WriteThrottle(0)
        self.DirectControl.WriteAUX1(1)
        t = threading.Thread(target = self.Finish_Abort, args = ())
        t.start()

        return True

    def Finish_Abort(self) -> bool:
        self.Delay(1)
        self.DirectControl.ESC_ABORT()

        return True

    def Delay(self, delay) -> None:
        time.sleep(delay)

    def ReturnSerial(self) -> None:
        return self.ser

class TargetInfo():

    def __init__(self) -> None:
        self.num = 0
        self.targets_sent = False
        self.targets = []

        self.start = (-117.695380, 33.586521)
        self.home = (-117.695380, 33.586521)

        #Used for parsing GPS Data
        self.ser = None

        #Separate class used to call mapping functions
        self.Mapping = Mapping()

    def Setup(self, num) -> None:
        if num == '':
            self.num = 0
        else:
            self.num = int(num)

        '''Default starting values'''
        ###
        '''Add functionality to set home and start in GUI'''
        ###

    def ParsingSetup(self, ser: 'serial.serialwin32.Serial') -> None:
        self.ser = ser

    def SetStart(self):
        t = threading.Thread(target=self.ReadGPS, args=(False, ))
        t.start()

    def NumTargets(self) -> int:
        return self.num

    def TargetsSet(self) -> None:
        self.targets_sent = True

    def LatLongCheck(self, *args) -> bool:
        for i in range(0, 20, 2):
            if (i/2 < self.num):
                try:
                    sp_long = args[i].split('.', 1)
                    sp_lat = args[i+1].split('.', 1)
                    tup = (float(args[i]), float(args[i+1])) 
                    self.targets.append(tup)
                except:
                    self.targets = []
                    return False
    
        t = threading.Thread(target=self.Mapping.GUIpath, \
                             args=(self.targets, self.start, ))
        t.start()
        return True

    def TestPath(self) -> None:
        targets = [(-117.843930, 33.645871), (-117.843801, 33.645590)]
        big_list = [(-117.842715, 33.645892),
                    (-117.842916, 33.646009),
                    (-117.843142, 33.646009),
                    (-117.843480, 33.645978),
                    (-117.843748, 33.645934),
                    (-117.843930, 33.645871),
                    (-117.844118, 33.645893),
                    (-117.844381, 33.645867),
                    (-117.844236, 33.645652),
                    (-117.843962, 33.645603),
                    (-117.843801, 33.645590),
                    (-117.843576, 33.645603),
                    (-117.843329, 33.645594),
                    (-117.843125, 33.645652),
                    (-117.842900, 33.645688),
                    (-117.842717, 33.645782),
                    (-117.842715, 33.645892)]
        self.Mapping.set_info(targets, (-117.842715, 33.645892))

        t = threading.Thread(target=self.TestLoop, args=(big_list, ))
        t.start()

    def TestLoop(self, big_list) -> None:
        for p in big_list:
            self.Mapping.track_drone(p)
            time.sleep(0.1)
        self.Mapping.reset()

    def ReadGPS(self, flag = True) -> bool:
        if flag:
            self.Mapping.set_info(self.targets, self.start)
        while True:
            line = self.ser.readline()
            if line != b'':
                s =  line.decode("utf-8")
                if s[0:23] == "Data Sent GPS Recieved:":
                    sp = s[23:].split(',', 1)
                    if len(sp) == 2:
                        try:
                            lat_split = sp[0][1:].split(" ", 1)
                            long_split = sp[1][1:].split(" ", 1)
                            lat = Decimal(lat_split[1])/Decimal(1000000)
                            long = Decimal(long_split[1])/Decimal(1000000)
                            long = float(long)
                            lat = float(lat)
                            if flag:
                                self.Mapping.track_drone((long, lat))
                            else:
                                self.start = (long, lat)
                                self.start = self.home
                                print("Current GPS: {}".format(self.start))
                                return True
                        except ValueError:
                            pass
        return True


'''Kivy GUI'''        
class TabbedPanelApp(App):
    def __init__(self) -> None:
        App.__init__(self)

        #Allows access to controller class to send signals
        self.Controller = Controller()

        #For GPS/Mapping
        self.TargetInfo = TargetInfo()

        self.tp = None
        self.th_drone_control = None
        self.th_drone_adv_control = None
        self.th_doc = None

        Cache.remove('kv.image')
        Cache.remove('kv.texture')

        image = Image.open("Gmap/default.png")
        temp = image.copy()
        temp.save("Gmap/drone_path.png")

        image = Image.open("images/default_score.png")
        temp = image.copy()
        temp.save("images/scored.png")
        temp.save("images/prescored.png")
    
    def build(self) -> 'kivy.uix.tabbedpanel.TabbedPanel':
        self.tp = TabbedPanel()
        self.tp.tab_width = 500
        

        #Default tab: Main Controller
        self.tp.default_tab_text = "Main Controller Page"
        self.tp.default_tab_content = ControllerView()
        self.tp.default_tab.background_normal = 'images/strong_blue.png'
        self.tp.default_tab.background_down = 'images/lime_green.png'

        #Drone Control
        self.th_drone_adv_control = TabbedPanelHeader(text='Drone Control')
        self.th_drone_adv_control.content= DroneView()
        self.th_drone_adv_control.background_normal = 'images/strong_blue.png'
        self.th_drone_adv_control.background_down = 'images/lime_green.png'

        #Drone Control
        self.th_drone_control = TabbedPanelHeader(text='DIPS and Mapping')
        self.th_drone_control.content= DroneAdvView()
        self.th_drone_control.background_normal = 'images/strong_blue.png'
        self.th_drone_control.background_down = 'images/lime_green.png'

        #Documentation
        self.th_doc = TabbedPanelHeader(text='Documentation')
        self.th_doc.content= DocView()
        self.th_doc.background_normal = 'images/strong_blue.png'
        self.th_doc.background_down = 'images/lime_green.png'        

        self.tp.add_widget(self.tp.default_tab)
        self.tp.add_widget(self.th_drone_adv_control)
        self.tp.add_widget(self.th_drone_control)
        self.tp.add_widget(self.th_doc)

        return self.tp

    def do_directcheck(self, throttle_text, yaw_text, pitch_text, roll_text, aux1_text, aux2_text, *args) -> bool:
        if throttle_text == '' or yaw_text == '' or \
           pitch_text == '' or roll_text == '':
            return False
        else:
            try:
                throttle_text = int(throttle_text)
                yaw_text = int(yaw_text)
                pitch_text = int(pitch_text)
                roll_text = int(roll_text)
                aux1_text = int(aux1_text)
                aux2_text = int(aux2_text)
            except ValueError:
                return False
            else:
                self.Controller.Throttle = throttle_text
                self.Controller.Yaw = yaw_text
                self.Controller.Pitch = pitch_text
                self.Controller.Roll = roll_text
                self.Controller.AUX1 = aux1_text
                self.Controller.AUX2 = aux2_text

                return self.Controller.DirectValueCheck()

    def do_rampcheck(self, *args) -> None:
        return self.Controller.RampValueCheck()

    def set_s1(self, value) -> None:
        self.Controller.Throttle_Ramp = value

    def set_s2(self, value) -> None:
        self.Controller.Yaw_Ramp = value

    def set_s3(self, value) -> None:
        self.Controller.Pitch_Ramp = value

    def set_s4(self, value) -> None:
        self.Controller.Roll_Ramp = value

    def available_ports(self) -> list:
        ports = self.Controller.PortCheck()

        if ports:
            return ports
        return ['None']

    def check_connect(self) -> bool:
        return self.Controller.CheckConnect()

    def do_setup(self, port, bauds) -> bool:
        if port == 'None' or bauds == 'None':
            return False

        Connection = self.Controller.Connect(port, int(bauds))
        self.TargetInfo.ParsingSetup(self.Controller.ReturnSerial())

        return Connection

    def startup(self) -> None:
        self.Controller.Startup()

    def up(self) -> bool:
        self.Controller.Prev_Val = self.Controller.Ramping.PreviousValues()
        if len(self.Controller.Prev_Val) != 0:
            return self.Controller.Up()
        return False

    def down(self) -> bool:
        self.Controller.Prev_Val = self.Controller.Ramping.PreviousValues()
        if len(self.Controller.Prev_Val) != 0:
            return self.Controller.Down()
        return False

    def forward(self) -> bool:
        self.Controller.Prev_Val = self.Controller.Ramping.PreviousValues()
        if len(self.Controller.Prev_Val) != 0:
            return self.Controller.Forward()
        return False

    def backward(self) -> bool:
        self.Controller.Prev_Val = self.Controller.Ramping.PreviousValues()
        if len(self.Controller.Prev_Val) != 0:
            return self.Controller.Backward()
        return False

    def right(self) -> bool:
        self.Controller.Prev_Val = self.Controller.Ramping.PreviousValues()
        if len(self.Controller.Prev_Val) != 0:
            return self.Controller.Right()
        return False

    def left(self) -> bool:
        self.Controller.Prev_Val = self.Controller.Ramping.PreviousValues()
        if len(self.Controller.Prev_Val) != 0:
            return self.Controller.Left()
        return Falses

    def hover(self) -> bool:
        self.Controller.Prev_Val = self.Controller.Ramping.PreviousValues()
        if len(self.Controller.Prev_Val) != 0:
            return self.Controller.Hover()
        return False

    def abort(self) -> None:
        self.Controller.Abort()

    def disconnect(self) -> None:
        self.Controller.Disconnect()
        
    def do_check_latlong(self, *args) -> bool:
        return self.TargetInfo.LatLongCheck(*args)

    def test_path(self, *args) -> None:
        self.TargetInfo.TestPath()        

    def threading_read(self, *args) -> None:
        t = threading.Thread(target = self.read_gps, args = ())
        t.start()

    def read_gps(self) -> bool:
        time.sleep(2)
        return self.TargetInfo.ReadGPS()

    def find_start(self) -> None:
        self.TargetInfo.SetStart()

    def load_gif(self, *args) -> None:
        image = Image.open("images/loading.png")
        temp = image.copy()
        temp.save("Gmap/drone_path.png")

    def retrieveNumTargets(self, *args) -> int:
        try:
            nt = int(args[0])
            if nt > 0 and nt <= 10:
                return nt
            else:
                return -1
        except:
            return -1

    def setnumtargets(self, *args) -> None:
        self.TargetInfo.Setup(args[0])

    def shownumtargets(self, *args) -> None:
        return self.TargetInfo.NumTargets()

    def targets_sent(self, *args) -> None:
        self.TargetInfo.TargetsSet()

    def targets_sent_check(self, *args) -> None:
        return self.TargetInfo.targets_sent

    def switch_tab(self, *args) -> None:
        self.tp.switch_to(self.tp.default_tab)
        '''
        To change to other tabs change self.tp.default_tab to:
        self.th_drone_control
        self.th_drone_adv_control
        self.th_doc
        '''

if __name__ == '__main__':
    TabbedPanelApp().run()
