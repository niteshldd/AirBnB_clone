#!/usr/bin/python3
import json
import datetime
import os.path

class FileStorage:
    dt_format = '%Y-%m-%dT%H:%M:%S.%f'

    def __init__(self):
        self.__file_path = './file.json'
        self.__objects = {}

    def all(self):
        obj = self.reload()
        return obj

    def new(self, obj):
        key = str(obj.__class__.__name__) + '.' + str(obj.id)
        self.__objects[key] = obj

    def save(self):
        store = {}
        for i in self.__objects.keys():
            temp = self.__objects[i].to_json()
            store[i] = temp

        with open(self.__file_path, "w+") as f:
            json.dump(store, f)

    def reload(self):
        if os.path.exists(self.__file_path):
            with open(self.__file_path, 'r') as f:
                r = json.load(f)
            from models.base_model import BaseModel
            from models.user import User
            from models.state import State
            from models.city import City
            from models.place import Place
            from models.amenity import Amenity
            from models.review import Review

            for i in r.keys():
                try:
                    r[i]['created_at'] = datetime.datetime.strptime(r[i]['created_at'], self.dt_format)
                    r[i]["updated_at"] = datetime.datetime.strptime(r[i]["updated_at"], self.dt_format)
                except:
                    pass
                if r[i]["__class__"] == "BaseModel":
                    self.__objects[i] = BaseModel(**r[i])
                elif r[i]["__class__"] == "User":
                    self.__objects[i] = User(**r[i])
                elif r[i]["__class__"] == "State":
                    self.__objects[i] = State(**r[i])
                elif r[i]["__class__"] == "City":
                    self.__objects[i] = City(**r[i])
                elif r[i]["__class__"] == "Place":
                    self.__objects[i] = Place(**r[i])
                elif r[i]["__class__"] == "Amenity":
                    self.__objects[i] = Amenity(**r[i])
                elif r[i]["__class__"] == "Review":
                    self.__objects[i] = Review(**r[i])
            return self.__objects
        else:
            return {}
