const localHost = "http://localhost:3004"
import {getAuth, getIdToken} from "firebase/auth"
import uuid from 'react-native-uuid';

export function register(data) {
    const auth = getAuth();
    const newId = uuid.v4(); 
    auth["id"]  = uuid.v4();
    
        return fetch(`${localHost}/createAccount?`, {
            method:"POST",
            body:JSON.stringify(data)
        })
}

export function validLogin(data){
    const auth = getAuth();
    email = data["email"]
    password = data["password"]
    return fetch(`${localHost}/getAccount?email=${email}&password=${password}`, {
        method:"GET",
        
    })
}

export function processLink(link){
    bd = {"link": link}
    print(bd)
    return fetch(`${localHost}/analyzeLink`, {
        method:"POST",
        body:JSON.stringify(bd)
    })
}

export function handleDeleteAccount(){
    const auth = getAuth(); 
    const user = auth.currentUser;
  
    if (user) {
        try {
        deleteUser(user);
        console.log("Account deleted successfully");
        return true;
        } catch (error) {
        console.error("Error deleting account:", error);
        throw error;
        }
    } else {
        console.error("No user is currently signed in.");
        throw new Error("No user is signed in");
    }
  };
