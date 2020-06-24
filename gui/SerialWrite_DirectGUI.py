from serial import SerialTimeoutException
import time

'''Writing to Arduino Nano EEPROM for each signal'''
##############################################################
class DirectControl():
    def __init__(self):
        self.ser = None

    def Setup(self, ser: 'serial.serialwin32.Serial'):
        self.ser = ser
        
    def ESC_Turn_On(self, Option: int) -> bool:
        if Option in [0, 1]:
            try:
                self.ser.write(b'8')
            except SerialTimeoutException:
                print("Failed to write!\n")
                return False
        
            try:
                self.ser.write(bytes([Option]))
            except SerialTimeoutException:
                print("Failed to write!\n")
                return False
            except:
                pass
            return True
        return False        

    def ESC_ABORT(self) -> bool:
        try:
            self.ser.write(b'8')
        except SerialTimeoutException:
            print("Failed to write!\n")
            return False

        try:
            self.ser.write(bytes(b'0'))
        except SerialTimeoutException:
            print("Failed to write!\n")
            return False
        except:
            pass
        return True

    def WriteCalibration(self, Calibration: int) -> bool:
        if Calibration in [0, 1]:
            try:
                self.ser.write(b'7')
            except SerialTimeoutException:
                print("Failed to write!\n")
                return False
        
            try:
                self.ser.write(bytes([Calibration]))
            except SerialTimeoutException:
                print("Failed to write!\n")
                return False
            except:
                pass
            return True
        return False

    def WriteThrottle(self, Throttle: int) -> bool:
        try:
            self.ser.write(b'1')
        except SerialTimeoutException:
            print("Failed to write!\n")
            return False
        
        try:
            self.ser.write(bytes([Throttle]))
        except SerialTimeoutException:
            print("Failed to write!\n")
            return False
        except:
            pass
        return True

    def WriteYaw(self, Yaw: int) -> bool:
        try:
            self.ser.write(b'2')
        except SerialTimeOutException:
            print("Failed to write!\n")
            return False
        
        try:
            self.ser.write(bytes([Yaw]))
        except SerialTimeoutException:
            print("Failed to write!\n")
            return False
        return True

    def WritePitch(self, Pitch: int) -> bool:
        try:
            self.ser.write(b'3')
        except SerialTimeoutException:
            print("Failed to write!\n")
            return False
        
        try:
            self.ser.write(bytes([Pitch]))
        except SerialTimeoutException:
            print("Failed to write!\n")
            return False
        return True

    def WriteRoll(self, Roll: int) -> bool:
        try:
            self.ser.write(b'4')
        except SerialTimeoutException:
            print("Failed to write!\n")
            return False
        
        try:
            self.ser.write(bytes([Roll]))
        except SerialTimeoutException:
            print("Failed to write!\n")
            return False
        return True

    def WriteAUX1(self, AUX1: int) -> bool:
        try:
            self.ser.write(b'5')
        except SerialTimeOutException:
            print("Failed to write!\n")
            return False
        
        try:
            self.ser.write(bytes([AUX1]))
        except SerialTimeOutException:
            print("Failed to write!\n")
            return False
        return True

    def WriteAUX2(self, AUX2: int) -> bool:
        try:
            self.ser.write(b'6')
        except SerialTimeOutException:
            print("Failed to write!\n")
            return False
        
        try:
            self.ser.write(bytes([AUX2]))
        except SerialTimeOutException:
            print("Failed to write!\n")
            return False
        return True
        
    def WriteToBoard(self, Throttle: int, Yaw: int, Pitch: int, Roll: int, \
                     AUX1: int, AUX2: int) -> bool:
        
        if self.WriteThrottle(Throttle) and self.WriteYaw(Yaw) \
           and self.WritePitch(Pitch) and self.WriteRoll(Roll) \
           and self.WriteAUX1(AUX1) and self.WriteAUX2(AUX2):
            return True
        return False
