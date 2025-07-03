from GeneralFuntions import * 

def getSettings():
   try :
      settings = JsonReader("data/Settings.json")
   except FileNotFoundError:
      s = { 
            "RoomFile" : "data/Example-Room.json",
            "CurrentRoom" : 0,
            "ScreenSize" : [700, 700],
            "scale": {
               "seat" : 1,
               "table" : 1,
               "GUI" : 1,
               "Font" : {
                  "People": 1,
                  "Table": 1,
                  "GUI": 1
               }
            }
      }
      JsonWriter("data/Settings.json", s)
      settings = JsonReader("data/Settings.json")
   return settings

def saveSettings(settings : dict):
   JsonWriter("data/Settings.json", settings)