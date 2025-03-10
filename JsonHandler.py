import JH, Objects
JH = JH.JsonHandler()

def GetJson(Folder):
   return JH.JsonReader(Folder)

def WriteJson(Folder, info):
   JH.JsonWriter(Folder, info)

def ReadRoom(Folder, ID, FONT, scale):
   jsonRead = JH.JsonReader(Folder)
   Room = {
      "Tables" : [],
      "Round Tables" : [],
      "Seats" : [],
      "Tavla" : None
   }
   if jsonRead == []:
      return None
   
   tables = jsonRead[ID]["Tables"]
   roundTables = jsonRead[ID]["RoundTables"]
   seats = jsonRead[ID]["Seats"]

   if tables != []: 
      for table in tables:
         Room["Tables"].append(Objects.ClassTable(table[0], table[1], table[2], table[3], scale["table"]))
   
   if roundTables != []:
      for table in roundTables:
         Room["RoundTables"].append(Objects.ClassRoundTable(table[0], table[1], table[2], scale["table"]))
   if seats != []:
      for seat in seats:
         Room["Seats"]. append(Objects.ClassSeat(seat))

def SaveSeat(seat, scale):
   S = {
      "Pos" : [seat.rect.centerx/scale["table"], seat.rect.centery/scale["table"]],
      "Text" : seat.text
   }
   return S

def WriteRoom(Folder, ID, Room, scale):
   JsonWrite = {
      "Tables" : [],
      "RoundTables" : [],
      "Seats" : [],
      "Tavla" : None  
   }

   for table in Room["Tables"]:
      T = { 
         "Pos": 
         [
            table.rect.x/scale["table"], 
            table.rect.y/scale["table"], 
         ],
         "Size" : 
         [
            table.rect.w/scale["table"], 
            table.rect.h/scale["table"],
         ],
         "Children" : []
         }
      
      for child in table:
         C = SaveSeat(child, scale)
         T["Children"].append(C)
      
      JsonWrite["Tables"].append(T)

   for table in Room["RoundTables"]:
      T = { 
         "Pos": 
         [
            table.rect.x/scale["table"], 
            table.rect.y/scale["table"], 
         ],
         "Size" : 
         [
            table.rect.diameter/scale["table"],
         ],
         "Children" : []
      }
      
      for child in table:
         C = SaveSeat(child, scale)
         T["Children"].append(C)
      
      JsonWrite["RoundTables"].append(T)

   for seat in Room["Seats"]:
      T = SaveSeat(seat, scale["seat"])
      JsonWrite["Seats"].append(T)
   
   JsonWrite["Tavla"] = {
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

def CreateRoom(Folder, ID):
   json = JH.JsonReader(Folder)
   
   Room =  {
      "Tables" : [],
      "RoundTables" : [],
      "Seats" : [],
      "Tavla" : None
   }
   json[ID] = Room
   JH.JsonWriter(Folder, json)

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
