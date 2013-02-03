__author__ = 'Tim Herman <tim@belg.be>'
__coauthor__ = 'Mathias Teugels <mathias@codercpf.be>'

import time
import serial

class Log365RF:
    __irModes = ('MAX', 'MIN', 'DIF', 'AVG', 'HAL', 'LAL', 'TK', 'LOG', 'EMS')
    __irUnit = ('F', 'C')
    __data = []
    __order = -1

    def __init__(self, dev='/dev/ttyUSB0'):
        self.__ser = serial.Serial(
            port=dev,
            baudrate=2400,
            parity=serial.PARITY_ODD,
            stopbits=serial.STOPBITS_TWO,
            bytesize=serial.EIGHTBITS
        )

        self.__ser.open()
        self.__ser.isOpen()

    def getData(self):
        return self.processData(self.readStream())

    def readStream(self):
        del self.__data[:]
        while True :
            char = ''

            while self.__ser.inWaiting() > 0:
                char = self.__ser.read(1)
                if char != '':
                    char = ord (char)
                    order = int((240 & char) / 16)  # First 4 bits
                    value = 15 & char		        # Last 4 bits
                    self.__data.append( value )

                    if order == 14 and len(self.__data) == 14:
                        return self.__data
                    elif order == 14:
                        del self.__data[:]

    def processData(self, Data):
        result = {}

        temp = self.__data[6] * 4096 + self.__data[7] * 256 + self.__data[4] * 16 + self.__data[5]
        temp = temp / 10.0
        sign = 1 if (self.__data[9] & 1 == 0) else -1
        temp = temp * sign
        result['temp'] = temp

        unit = 0 if (self.__data[9] & 4 == 0) else 1
        result['unit'] = self.__irUnit[unit]

        epsilon = self.__data[2] * 16 + self.__data[3]
        epsilon = epsilon / 100.0 # percent
        result['epsilon'] = epsilon

        result['mode'] = self.__irModes[self.__data[1] - 1]

        return result

if __name__ == '__main__':
    l = Log365RF()
    print l.getData()
