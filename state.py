from datetime import date
from time import time
import json
from os import path


class State:
    loaded = False
    email = ''
    password = ''
    last_checked_date = None
    last_checked_time = None
    profiles_paths = []

    def load():
        if State.loaded == True:
            return True
        stateFile = open(path.dirname(__file__) + '/state.json')
        stateFile = json.load(stateFile)
        State.email = stateFile['email']
        State.password = stateFile['password']
        State.last_checked_date = stateFile['last_checked_date']
        State.last_checked_time = stateFile['last_checked_time']
        State.profiles_paths = stateFile['profiles_paths']
        State.loaded = True
        return True

    def update():
        stateFile = open(path.dirname(__file__) + '/state.json', 'w')
        stateFile.write(json.encoder.JSONEncoder().encode({
            "email": State.email,
            "password": State.password,
            "last_checked_date": str(date.today()),
            "last_checked_time": time() - 10 * 60,
            "profiles_paths": State.profiles_paths
        }))
