import SerialWrite_DirectGUI as Direct
import time

'''Writing to Arduino Nano EEPROM for each signal'''
##############################################################
class Ramping():
    def __init__(self):
        self.ser = None
        self.Direct = None
        
    def Setup(self, ser: 'serial.serialwin32.Serial', Direct: 'class SerialWrite_DirectGUI.DirectControl'):
        self.ser = ser
        self.Direct = Direct
        
    def PreviousValues(self) -> list:
        flag = False

        data_list = []
        
        try:
            self.ser.write(b'9')
        except SerialTimeOutException:
            print("Failed to write!\n")
            return data_list

        while True:
            data = self.ser.readline()
            try:
                if data != b'':
                    line = data.decode("utf-8").strip()
                    if line[:8] == 'Throttle':
                        flag = True
                    if line[:11] == 'Calibration':
                        return data_list
                    if flag:
                        data_list.append(int(line.split(" ")[1]))
                    continue
            except:
                pass
        return data_list

    def Throttle_Ramp(self, desired_throttle: int, curr_val: list, option: str) -> bool:
        if (option == "Up"):
            curr_throttle = curr_val[0]
            step = int((desired_throttle - curr_throttle)/3)
            remainder = ((desired_throttle - curr_throttle) % 3)
            new_throttle = curr_throttle
        elif (option == "Down"):
            curr_throttle = curr_val[0]
            step = int((curr_throttle - desired_throttle)/3)
            remainder = ((curr_throttle - desired_throttle) % 3)
            new_throttle = curr_throttle
        else:
            return False
            
        for i in range(step):
            if option == "Up":
                new_throttle += 3
            if option == "Down":
                new_throttle -= 3
            self.Direct.WriteThrottle(new_throttle)
            
            time.sleep(0.5)
            
        self.Direct.WriteThrottle(desired_throttle)
        
        time.sleep(0.5)
        
        return True

    def Yaw_Ramp(self, desired_yaw: int, curr_val: list, option: str) -> bool:
        if (option == "Up"):
            curr_yaw = curr_val[1]
            step = int((desired_yaw - curr_yaw)/3)
            remainder = ((desired_yaw - curr_yaw) % 3)
            new_yaw = curr_yaw
        elif (option == "Down"):
            curr_yaw = curr_val[1]
            step = int((curr_yaw - desired_yaw)/3)
            remainder = ((curr_yaw - desired_yaw) % 3)
            new_yaw = curr_yaw
        else:
            return False
            
        for i in range(step):
            if option == "Up":
                new_yaw += 3
            if option == "Down":
                new_yaw -= 3
            self.Direct.WriteYaw(new_yaw)
            
            time.sleep(0.5)
            
        self.Direct.WriteYaw(desired_yaw)
        
        time.sleep(0.5)
        
        return True

    def Pitch_Ramp(self, desired_pitch: int, curr_val: list, option: str) -> bool:
        if (option == "Up"):
            curr_pitch = curr_val[2]
            step = int((desired_pitch - curr_pitch)/3)
            remainder = ((desired_pitch - curr_pitch) % 3)
            new_pitch = curr_pitch
        elif (option == "Down"):
            curr_pitch = curr_val[2]
            step = int((curr_pitch - desired_pitch)/3)
            remainder = ((curr_pitch - desired_pitch) % 3)
            new_pitch = curr_pitch
        else:
            return False
            
        for i in range(step):
            if option == "Up":
                new_pitch += 3
            if option == "Down":
                new_pitch -= 3
            self.Direct.WritePitch(new_pitch)
            
            time.sleep(0.5)
            
        self.Direct.WritePitch(desired_pitch)
        
        time.sleep(0.5)
        
        return True

    def Roll_Ramp(self, desired_roll: int, curr_val: list, option: str) -> bool:
        if (option == "Up"):
            curr_roll = curr_val[3]
            step = int((desired_roll - curr_roll)/3)
            remainder = ((desired_roll - curr_roll) % 3)
            new_roll = curr_roll
        elif (option == "Down"):
            curr_roll = curr_val[3]
            step = int((curr_roll - desired_roll)/3)
            remainder = ((curr_roll - desired_roll) % 3)
            new_roll = curr_roll
        else:
            return False
            
        for i in range(step):
            if option == "Up":
                new_roll += 3
            if option == "Down":
                new_roll -= 3
            self.Direct.WriteRoll(new_roll)
            
            time.sleep(0.5)
            
        self.Direct.WriteRoll(desired_roll)
        
        time.sleep(0.5)
        
        return True
