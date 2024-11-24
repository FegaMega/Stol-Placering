import JH, Objects
JH = JH.JsonHandler()
def ReadRoom(Folder, ID, FONT):
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
         Room["Tables"].append(Objects.ClassTable(table[0], table[1], table[2], table[3]))
   
   if roundTables != []:
      for table in roundTables:
         Room["RoundTables"].append(Objects.ClassRoundTable(table[0], table[1], table[2]))

   if seats != []: 
      for seat in seats:
         if seat[2][1] == 0: 
            Room["Seats"].append(Objects.ClassSeat(seat[0], seat[1], FONT, Room["Tables"][seat[2][0]], seat[3]))
         if seat[2][1] == 1: 
            Room["Seats"].append(Objects.ClassSeat(seat[0], seat[1], FONT, Room["RoundTables"][seat[2][0]], seat[3]))


   if jsonRead[ID]["Tavla"] != []:  
      Room["Tavla"] = Objects.ClassTavla(jsonRead[ID]["Tavla"][0], jsonRead[ID]["Tavla"][1], jsonRead[ID]["Tavla"][2], jsonRead[ID]["Tavla"][3], FONT)
   else:
      Room["Tavla"] = Objects.ClassTavla(100, 100, 500, 50, FONT)

   return Room

def WriteRoom(Folder, ID, Room):
   jsonWrite = JH.JsonReader(Folder)
   tables = []
   roundTables = []
   seats = []
   for table in Room["Tables"]:
      tables.append([table.rect.x, table.rect.y, table.rect.w, table.rect.h])
   for table in Room["RoundTables"]:
      roundTables.append([table.rect.x, table.rect.y, table.diameter])
   for seat in Room["Seats"]:

      if type(seat.parent) == Objects.ClassTable:
         seats.append([seat.rect.x, seat.rect.y[1], [Room["Tables"].index(seat.parent), 0], seat.text])
      if type(seat.parent) == Objects.ClassRoundTable:
         seats.append([seat.rect.x, seat.rect.y[1], [Room["RoundTables"].index(seat.parent), 1], seat.text])

   tavla = [Room["Tavla"].rect.x, Room["Tavla"].rect.y, Room["Tavla"].rect.w, Room["Tavla"].rect.h]
   jsonWrite[ID]["Tables"] = tables
   jsonWrite[ID]["RoundTables"] = roundTables
   jsonWrite[ID]["Seats"] = seats
   jsonWrite[ID]["Tavla"] = tavla
   JH.JsonWriter(Folder, jsonWrite)