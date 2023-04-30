
import firebase_admin
import firebase_auth.firebase_auth
from firebase_admin import credentials
from firebase_admin import db


"""
update = ref.update({})
set = ref.set({})
"""

api_key="AIzaSyBgd59afUVZ-1YRpucWC7LCqieOjQr5Lko"
cred = credentials.Certificate('firebase_sdk.json')
auth = firebase_auth.firebase_auth.Auth(api_key,98,cred)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://car-parking-dee89-default-rtdb.firebaseio.com/'
})

ref_locations = '/Car Parking/Locations'
ref_data = '/Car Parking/Data'
ref_admin = '/Car Parking/User'
currentLocation = None
UserName=str()

def login(username:str,password:str):
    try:
        json1 = auth.sign_in_with_email_and_password(username,password)
        if json1 is not None:
            return 1
        else:
            return 0
    except Exception as e:
        return 0

def addLocation(username:str,location:str,address:str):
    db.reference(ref_locations).push({
            'location':location,
            'address':address
    })
    db.reference(ref_admin).push({
        'username':username,
        'location':location
    })

def addData(location:str,total:int,space:int):
    db.reference(ref_data).update({
        location:{
            'Total':total,
            'Available':space
        }
    })

def getLocations():
    d=db.reference(ref_locations).get()
    return dict(d)

def getUsers():
    d=db.reference(ref_admin).get()
    return dict(d)

def getData():
    d=db.reference(ref_data).get()
    return dict(d)

def getLocationsList():
    locationsDictionary = getLocations()
    locationsList=list()
    for key in locationsDictionary.keys():
        dic = locationsDictionary[key]
        locationsList.append(dic['location']+'->('+dic['address']+')')
    return locationsList

def _getUsersList():
    usersDictionary=getUsers()
    usersList=list()
    for key in usersDictionary.keys():
        dic = usersDictionary[key]
        usersList.append(dic['username']+'->'+dic['location'])
    return usersList

def getUsersLocation(username:str):
    usersDictionary = getUsers()
    for key in usersDictionary.keys():
        dic = usersDictionary[key]
        if dic['username']==username:
            return dic['location']
    return None

def getUsersLocationAddress(location:str):
    locationsDictionary = getLocations()
    for key in locationsDictionary.keys():
        dic = locationsDictionary[key]
        if dic['location']==location:
            return dic['address']
    return None


print(_getUsersList())