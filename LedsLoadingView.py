import machine
import utime
import _thread

"""
Example of use to not block UI
    loader = LedsLoadingView()
    print ("Show")
    _thread.start_new_thread(loader.showLoading, ())
    utime.sleep(1000)
    print("Should hide")
    loader.hideLoading()
"""
class LedsLoadingView:

    # INIT
    def __init__(self, is_loading=False, time=0.1):
        self.is_loading = is_loading
        self.time = time
        self.internal_led = machine.Pin(2, machine.Pin.OUT)
    
    # METHODS EXPOSED
    ### This method should be called with _thread, in other way, it will block dlow of program
    def showLoading(self):
        self.is_loading = True
        self.__process_loading()
    
    def hideLoading(self):
        self.is_loading = False

    # PRIVATE METHODS
    def __process_loading(self):
        while self.is_loading:
            self.internal_led.on()
            utime.sleep(self.time)
            self.internal_led.off()
            utime.sleep(self.time)

