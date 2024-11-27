import JH, Objects
JH = JH.JsonHandler()

def GetJson(Folder):
   return JH.JsonReader(Folder)

def ReadRoom(Folder, ID, FONT, scale):
   jsonRead = JH.JsonReader(Folder)
   Room = {
      "Tables" : [],
      "RoundTables" : [],
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
         if seat[2][1] == 0: 
            Room["Seats"].append(Objects.ClassSeat(seat[0]*scale["table"], seat[1]*scale["table"], FONT["Seat"], Room["Tables"][seat[2][0]], seat[3], scale))
         if seat[2][1] == 1: 
            Room["Seats"].append(Objects.ClassSeat(seat[0]*scale["table"], seat[1]*scale["table"], FONT["Seat"], Room["RoundTables"][seat[2][0]], seat[3], scale))
         if seat[2][1] == -1:
            Room["Seats"].append(Objects.ClassSeat(seat[0]*scale["seat"], seat[1]*scale["seat"], FONT["Seat"], None, seat[3], scale))


   if jsonRead[ID]["Tavla"]:  
      Room["Tavla"] = Objects.ClassTavla(jsonRead[ID]["Tavla"][0], jsonRead[ID]["Tavla"][1], jsonRead[ID]["Tavla"][2], jsonRead[ID]["Tavla"][3], FONT["Table"], scale["table"])
   else:
      Room["Tavla"] = Objects.ClassTavla(100, 100, 500, 50, FONT, scale["table"])

   return Room

def WriteRoom(Folder, ID, Room, scale):
   jsonWrite = JH.JsonReader(Folder)
   tables = []
   roundTables = []
   seats = []
   for table in Room["Tables"]:
      tables.append([table.rect.x/scale["table"], table.rect.y/scale["table"], table.rect.w/scale["table"], table.rect.h/scale["table"]])
   for table in Room["RoundTables"]:
      roundTables.append([table.rect.x/scale["table"], table.rect.y/scale["table"], table.diameter/scale["table"]])
   for seat in Room["Seats"]:
      if type(seat.parent) == Objects.ClassTable:
         seats.append([seat.rect.centerx/scale["table"], seat.rect.centery/scale["table"], [Room["Tables"].index(seat.parent), 0], seat.text])
      elif type(seat.parent) == Objects.ClassRoundTable:
         seats.append([seat.rect.centerx/scale["table"], seat.rect.centery/scale["table"], [Room["RoundTables"].index(seat.parent), 1], seat.text])
      elif seat.parent == None:
         seats.append([seat.rect.centerx/scale["seat"], seat.rect.centery/scale["seat"], [0, -1], seat.text])
   tavla = [Room["Tavla"].rect.x/scale["table"], Room["Tavla"].rect.y/scale["table"], Room["Tavla"].rect.w/scale["table"], Room["Tavla"].rect.h/scale["table"]]
   jsonWrite[ID]["Tables"] = tables
   jsonWrite[ID]["RoundTables"] = roundTables
   jsonWrite[ID]["Seats"] = seats
   jsonWrite[ID]["Tavla"] = tavla
   JH.JsonWriter(Folder, jsonWrite)

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