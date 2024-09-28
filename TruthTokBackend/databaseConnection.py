import firebase_admin
from firebase_admin import credentials, firestore, storage
import firebase_admin
from firebase_admin import credentials


class dbConnection():
    def __init__(self):
        # cred = credentials.Certificate("auth/accoai-db-firebase-adminsdk.json")
        # self.default_app = firebase_admin.initialize_app(cred)
        cred = credentials.Certificate("truthtok.json")
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()
    def getAccount(self, accID):
        doc_ref = self.db.collection('accounts').document(accID)
        snap = doc_ref.get()
        if snap.exists:
            return snap.to_dict()
        else:
            return Exception

    def getCreator(self, creatID):
        doc_ref = self.db.collection('creators').document(creatID)
        jsonData = doc_ref.get()
        if jsonData.exists:
            return jsonData.to_dict()
        else:
            newAcc = {"Correct": 0, "Incorrect": 0, "Indeterminate": 0}
            self.db.collection('creators').document(creatID).set(newAcc)
            return self.db.collection('creators').document(creatID).get().to_dict()


    def findTikTok(self, tikID):
        doc_ref = self.db.collection('creators').document(tikID)
        snap = doc_ref.get()

        if (snap.exists):
            return snap.to_dict()
        else:
            return None

    def addAccount(self, accID):
        newAcc = {"Correct": 0, "Incorrect":0, "Indeterminate":0}
        self.db.collection('accounts').document(accID).set(newAcc)


