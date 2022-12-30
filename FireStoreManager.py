import ufirestore
import FirebaseJson
import utime
import uasyncio
import ConnectWifiManager
import FirebaseJson
import _thread

"""
Success write for a firebase document, or gets a simulated listener

EXAMPLE:

    ## Connect to internet
    ssid_name = "IZZI-3F84_EXT"
    ssid_pass = "9CC8FC753F84"
    async def main():
        managerWifi = ConnectWifiManager.ConnectWifiManager()
        await uasyncio.gather(managerWifi.connectToInternet(ssid_name, ssid_pass))
    uasyncio.run(main())


    path = "users/"
    firestoreManager = FireStoreManager("waterpump-29206")

    ## Example of writing...
    properties_to_insert = {"downTankIsFull/booleanValue": False,
                            "upTankIsFull/booleanValue": True,
                            "pumpIsOn/booleanValue": True}
    firestoreManager.set_or_replace_on_document(path,
                                               "myDocumentCustomId",
                                                properties_to_insert)

    ## Example of listener...
    def completion(document):
        print("downTankIsFull: " + str(document.get("downTankIsFull")))
        print("pumpIsOn: " + str(document.get("pumpIsOn")))
        print("upTankIsFull: " + str(document.get("upTankIsFull")))

    _thread.start_new_thread(firestoreManager.create_simulated_listener(path,
                                                                        "myDocumentCustomId",
                                                                        5,
                                                                        lambda document:completion(document)), ())

"""
class FireStoreManager:
    
    ## INIT
    def __init__(self, project_id):
        ufirestore.set_project_id(project_id)
    
    ## METHODS
    def set_or_replace_on_document(self, path, documentId, properties={}):
        print("Start updapting firebase document...")
        doc = FirebaseJson.FirebaseJson()
        for key in properties:
            doc.set(key, properties[key])
        try: 
            path_for_get_delete = path + documentId
            print("Deleting document...")
            ufirestore.delete(path_for_get_delete, bg=False)
            print("Reinserting document...")
            path_for_insert = path + "?documentId=" + documentId
            response = ufirestore.patch(path_for_insert,
                                        doc,
                                        bg=False)
            print("Finish updating document in firebase")
            print(response)
        except ufirestore.FirestoreException as error:
            path_for_insert = path + "?documentId=" + documentId
            print("Inserting document at first time")
            response = ufirestore.patch(path_for_insert,
                                        doc,
                                        bg=True)
            print("Finish updating document in firebase")
    
    async def create_simulated_listener(self, path, documentId, time, completion):
        await uasyncio.run(self.__create_simulated_listener(path, documentId, time, completion))

    async def __create_simulated_listener(self, path, documentId, time, completion):
        while True:
            path_for_get = path + documentId
            currentDocumentRaw = ufirestore.get(path_for_get)
            currentDocument = FirebaseJson.FirebaseJson.from_raw(currentDocumentRaw)
            completion(currentDocument["fields"])
            await uasyncio.sleep(time)
        