import JH, Old.OldObjects as OldObjects

def getRoom(Folder, ID, FONT, scale) -> dict:
   jsonRead = JH.JsonReader(Folder)
   Room = {
      "Tables" : [],
      "RoundTables" : [],
      "Seats" : [],
      "Tavla" : None
   }
   if jsonRead == []:
      print("Room Json file empty")
      return None
   
   tables = jsonRead[ID]["Tables"]
   seats = jsonRead[ID]["Seats"]
   tavla = jsonRead[ID]["Tavla"]

   if tables != []: 
      for table in tables:
         if table["Type"] == "Rectangular":
            Room["Tables"].append(
               OldObjects.ClassTable(
                  table["Type"],
                  table["Pos"], 
                  table["Size"], 
                  table["Children"], 
                  scale["table"]
                  )
               )
         elif table["Type"] == "Round":
            Room["RoundTables"].append(
               OldObjects.ClassRoundTable(
                  table["Type"],
                  table["Pos"], 
                  table["Size"], 
                  table["Children"], 
                  scale["table"]
                  )
               )
   if seats != []:
      for seat in seats:
         Room["Seats"].append(OldObjects.ClassSeat(seat["Pos"], FONT["Seat"], scale=scale))
   if tavla:
      Room["Tavla"] = OldObjects.ClassTavla(tavla["Pos"], tavla["Size"], FONT["Tavla"], scale["table"])
   else:
      Room["Tavla"] = OldObjects.ClassTavla((0, 0), (200, 25), FONT["Tavla"], scale["table"])

   return Room

def SaveSeat(seat, scale):
   S = {
      "Pos" : [
         seat.rect.centerx/scale, 
         seat.rect.centery/scale
         ],
      "Text" : seat.text
   }
   return S

def saveRoom(Folder, ID, Room, scale):
   #Variables
   JsonWrite = JH.JsonReader(Folder)
   jRoom = {
      "Tables" : [],
      "Seats" : [],
      "Tavla" : None  
   }

   #Tables
   for table in Room["Tables"]:
      match table.Type:

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
               "Children" : table.children
               }
            jRoom["Tables"].append(T)
         
         case "Round":
            T = { 
               "Type" : "Round",
               "Pos": 
               [
                  table.rect.x/scale["table"], 
                  table.rect.y/scale["table"] 
               ],
               "Size" : table.diameter/scale["table"],
               "Children" : table.children
            }

      jRoom["Tables"].append(T)


   JsonWrite[ID]["Tables"] = jRoom["Tables"]

   #seats without parent table
   for seat in Room["Seats"]:
      T = SaveSeat(seat, scale["seat"])
      jRoom["Seats"].append(T)

   JsonWrite[ID]["Seats"] = jRoom["Seats"]
   
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


   JH.JsonWriter(Folder, JsonWrite)
   
   return

def CreateRoom(Folder, ID) -> dict:
   json = JH.JsonReader(Folder)
   
   Room =  {
      "Tables" : [],
      "RoundTables" : [],
      "Seats" : [],
      "Tavla" : None
   }
   json[ID] = Room
   JH.JsonWriter(Folder, json)
   return Room
def RemoveRoom(Folder, ID):
   
   json = JH.JsonReader(Folder)
   json.pop(ID)
   JH.JsonWriter(Folder, json)

def RenameRoom(Folder, ID, Name):
   json = JH.JsonReader(Folder)
   json2 = JH.JsonReader(Folder)
   json.pop(ID)
   json[Name] = json2[ID]
   JH.JsonWriter(Folder, json)
