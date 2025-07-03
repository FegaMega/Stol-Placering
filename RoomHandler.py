import Objects as Objects, math, pygame
from GeneralFuntions import *

def RectangleMouseCollision(pos, T):
   
   if mouseCollision(pos, T.rect):
    
      if not mouseCollision(pos, pygame.Rect(T.rect.left,T.rect.top,T.rect.width - T.EdgeSize,T.rect.height - T.EdgeSize)):   
    
         return True, "Edge"
    
      return True, "Normal"
   
   return False, ""

def getRoom(Folder, ID, FONT, scale) -> dict:
   jsonRead = JsonReader(Folder)
   Room = {
      "Tables" : [],
      "RoundTables" : [],
      "People" : [],
      "Tavla" : None
   }
   if jsonRead == []:
      print("Room Json file empty")
      return None
   
   tables = jsonRead[ID]["Tables"]
   People = jsonRead[ID]["People"]
   tavla = jsonRead[ID]["Tavla"]

   if tables != []:

      for table in tables:
      
         match table["Type"]: 
            
            case "Rectangular":
               T = Objects.Table(
                     table["Type"],
                     table["Pos"], 
                     table["Size"], 
                     table["Seats"], 
                     scale["table"]
                     )
               T.EdgeSize = 10*scale["table"]

               T.hitboxFunc = RectangleMouseCollision

               Room["Tables"].append(T)
            case _:
               print("Error! Table could not be loaded\nTable: ", table, "\nTable index: ", tables.index(table), '\nType not recogninsed!')
      
   if People != []:
      for person in People:
         Room["People"].append(Objects.Person(person["Pos"], person["Name"], FONT, scale))
   
   if tavla:
      Room["Tavla"] = Objects.Tavla(tavla["Pos"], tavla["Size"], FONT, scale["table"])
   
   else:
      Room["Tavla"] = Objects.Tavla((0, 0), (200, 25), FONT, scale["table"])

   return Room

def Saveperson(person, scale):
  
   S = {
      "Pos" : [
         person.rect.centerx/scale, 
         person.rect.centery/scale
         ],
      "Name" : person.text
   }
  
   return S

def saveRoom(Folder, ID, Room, scale):
   #Variables
   JsonWrite = JsonReader(Folder)
   jRoom = {
      "Tables" : [],
      "People" : [],
      "Tavla" : None  
   }

   #Tables
   for table in Room["Tables"]:
      match table.type:

         case "Rectangular":
            T = { 
               "Type" : "Rectangular",
               "Pos": 
               [
                  table.rect.x/scale["table"], 
                  table.rect.y/scale["table"], 
               ],
               "Size" : 
               [
                  table.rect.w/scale["table"], 
                  table.rect.h/scale["table"]
               ],
               "Seats" : table.seats
               }
         
         case "Round":
            T = { 
               "Type" : "Round",
               "Pos": 
               [
                  table.rect.x/scale["table"], 
                  table.rect.y/scale["table"] 
               ],
               "Size" : table.diameter/scale["table"],
               "Seats" : table.seats
            }

      jRoom["Tables"].append(T)


   JsonWrite[ID]["Tables"] = jRoom["Tables"]

   #People without parent table
   for person in Room["People"]:
      
      T = Saveperson(person, scale["People"])
      
      jRoom["People"].append(T)

   JsonWrite[ID]["People"] = jRoom["People"]
   
   #Whiteboard
   JsonWrite[ID]["Tavla"] = {
      "Pos" : 
      [
         Room["Tavla"].rect.x/scale["table"],
         Room["Tavla"].rect.y/scale["table"]
      ],
      "Size" : 
      [
         Room["Tavla"].rect.w/scale["table"],
         Room["Tavla"].rect.h/scale["table"]
      ]
   }


   JsonWriter(Folder, JsonWrite)
   
   return

def CreateRoom(Folder, ID) -> dict:

   json = JsonReader(Folder)
   
   Room =  {
      "Tables" : [],
      "RoundTables" : [],
      "People" : [],
      "Tavla" : None
   }

   json[ID] = Room

   JsonWriter(Folder, json)

   return Room
def RemoveRoom(Folder, ID):
   
   json = JsonReader(Folder)

   json.pop(ID)
   
   JsonWriter(Folder, json)

def RenameRoom(Folder, ID, Name):

   json = JsonReader(Folder)

   json2 = JsonReader(Folder)

   json.pop(ID)

   json[Name] = json2[ID]

   JsonWriter(Folder, json)
