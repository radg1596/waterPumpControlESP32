import _thread
import ConnectWifiManager
import LedsLoadingView
import MutablePinComponent
import utime
import uasyncio
import FireStoreManager
from machine import Pin

class MainInterface:

    ## INIT
    def __init__(self):
        self.loadingViewComponent = LedsLoadingView.LedsLoadingView()
        self.ssid_name = "IZZI-3F84"
        self.ssid_pass = "9CC8FC753F84"
        self.pinsComponent = MutablePinComponent.MutablePinComponent()
        self.firebaseManager = FireStoreManager.FireStoreManager("waterpump-29206")
        self.firebaseManagerForListener = FireStoreManager.FireStoreManager("waterpump-29206")
        self.firebaseRootPath = "users/"
        self.firebaseDocumentId = "pump_document"
    
    ## METHODS
    def startFlow(self):
        self.__showLoadingLeds()
        uasyncio.run(self.__connectToInternet())
        self.__hideLoadingLeds()
        uasyncio.run(self.__startAllListeners())
    
    ## LOADING UI
    def __showLoadingLeds(self):
        _thread.start_new_thread(self.loadingViewComponent.showLoading, ())
    
    def __hideLoadingLeds(self):
        self.loadingViewComponent.hideLoading()

    ## INTERNET
    async def __connectToInternet(self):
        managerWifi = ConnectWifiManager.ConnectWifiManager()
        await uasyncio.gather(managerWifi.connectToInternet(self.ssid_name,
                                                            self.ssid_pass))

    # LISTENERS
    async def __startAllListeners(self):
        await uasyncio.gather(self.__startListeningToInputLeds(), self.__startListeningForFirebase())

    
    async def __startListeningToInputLeds(self):
        try:
            completion = lambda: self.__handleSomeLedChange()
            await self.pinsComponent.start_listening(completion, 1.0)
        except Exception as error:
            print("Next error: " + str(error))
            uasyncio.sleep(3)
            uasyncio.run(self.__startListeningToInputLeds())
        
    
    ## HANDLE LEDS CHANGE
    def __handleSomeLedChange(self):
        print("New leds change")
        self.__updateLedsValuesOnFirebase()

    ## FIREBASE
    def __updateLedsValuesOnFirebase(self):
        properties_to_insert = {"downTankIsFull/booleanValue": self.pinsComponent.downTankPinValue(),
                                "upTankIsFull/booleanValue": not self.pinsComponent.upTankPinValue(),
                                "pumpOfWaterIsOn/booleanValue": not self.pinsComponent.pumpWaterValue()}
        self.firebaseManager.set_or_replace_on_document(self.firebaseRootPath,
                                                        self.firebaseDocumentId,
                                                        properties_to_insert)
        print("Values updated on firebase...")
        print("Now is listening for new leds changes...")
    
    async def __startListeningForFirebase(self):
        print("Start listening for firebase...")
        
        try:
            completion = lambda document:self.__listenerCompletion(document)
            await self.firebaseManagerForListener.create_simulated_listener(self.firebaseRootPath,
                                                                        "force_properties",
                                                                        4,
                                                                        completion)
        except Exception as error:
            print("Firebase listener, next error: " + str(error))
            uasyncio.sleep(10)
            uasyncio.run(self.__startListeningForFirebase())

    def __listenerCompletion(self, document):
        shouldForceOnInPump = document.get("shouldForceOn")
        self.pinsComponent.isForceOnEnabled = shouldForceOnInPump
        self.pinsComponent.setPumpWaterPinValue()
        print("Force on status: " + str(shouldForceOnInPump))
        
main_interface = MainInterface()
main_interface.startFlow()