import machine
import utime
import _thread
import uasyncio
from machine import Pin


class MutablePinComponent:

    ## INIT
    def __init__(self ):
        self.upTankPin = Pin(32, Pin.IN)
        self.downTankPin = Pin(33, Pin.IN)
        self.pumpWaterPin = Pin(25, Pin.OUT)
        self.isForceOnEnabled = False
        self.upTankPinLastValue = not self.upTankPin.value()
        self.downTankPinLastValue = not self.downTankPin.value()
    
    ## METHODS
    async def start_listening(self,
                        completion,
                        every_time):
        await uasyncio.run(self.__start_listening(completion, every_time))

    async def __start_listening(self,
                                completion,
                                every_time):
        while True:
            if self.upTankPinLastValue != self.upTankPin.value() or self.downTankPinLastValue != self.downTankPin.value():
                   self.upTankPinLastValue = self.upTankPin.value()
                   self.downTankPinLastValue = self.downTankPin.value()
                   self.setPumpWaterPinValue()
                   completion()
            await uasyncio.sleep(every_time)
    
    def upTankPinValue(self):
        return self.upTankPin.value()
    
    def downTankPinValue(self):
        return self.downTankPin.value()
    
    def pumpWaterValue(self):
        return self.pumpWaterPin.value()
    
    def shouldOnPumpBasedOnPins(self):
        return self.downTankPinValue() and self.upTankPinValue()
    
    ### Remember that the relevator only on with zero...
    def setPumpWaterPinValue(self):
        if self.isForceOnEnabled:
            self.pumpWaterPin.off()
        else:
            if self.shouldOnPumpBasedOnPins():
                self.pumpWaterPin.off()
            else:
                self.pumpWaterPin.on()