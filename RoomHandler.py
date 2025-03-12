import JH, Objects as Objects

def getRoom(Folder, ID, FONT, scale) -> dict:
   jsonRead = JH.JsonReader(Folder)
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
         if table["Type"] == "Rectangular":
            Room["Tables"].append(
               Objects.Table(
                  table["Type"],
                  table["Pos"], 
                  table["Size"], 
                  table["Children"], 
                  scale["table"]
                  )
               )
   
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
      "Text" : person.text
   }
   return S

def saveRoom(Folder, ID, Room, scale):
   #Variables
   JsonWrite = JH.JsonReader(Folder)
   jRoom = {
      "Tables" : [],
      "People" : [],
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

   #People without parent table
   for person in Room["People"]:
      T = Saveperson(person, scale["person"])
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


   JH.JsonWriter(Folder, JsonWrite)
   
   return

def CreateRoom(Folder, ID) -> dict:
   json = JH.JsonReader(Folder)
   
   Room =  {
      "Tables" : [],
      "RoundTables" : [],
      "People" : [],
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
