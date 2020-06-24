from serial import Serial, SerialException
from serial.tools import list_ports

'''Connection to Arduino Nano Device Setup'''
##############################################################
class SerialConnection():
    def __init__(self):
        self.ser = None
        self.port = None
        self.baudrate = None

    def Setup(self, port: str, bauds: int) -> bool:
        self.port = port
        self.baudrate = bauds
        return True

    def SerialPorts(self) -> bool:
        '''Checks to see if the port you choose is available
        The line of code below this line will take >5 seconds
        to run if bluetooth is enabled -- DISABLE BLUETOOTH'''
        ports = [port.device for port in list_ports.comports()]
        return ports
            
    def StartConnection(self) -> bool:
        '''Connects to the desired device'''

        self.ser = None

        try:
            self.ser = Serial(self.port, self.baudrate, timeout = 0)
        except SerialException:
            return None
        except TypeError:
            return None
        else:
            pass
        finally:
            return self.ser
        
    def EndConnection(self) -> None:
        '''Closes the connection'''
        self.ser.close()
##############################################################
