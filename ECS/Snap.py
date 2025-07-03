from Component import *
from ECS.GeneralFuntions import *

def handleSnap(EntID):

   #Get Snap Component
   Snap : SnapComponent = manager.getComponent(EntID, SnapComponent)

   #Get Transform of EntID
   Transform : TransformComponent = manager.getComponent(EntID, TransformComponent)

   #If the EntID has VertexComponent we have to grab that and the Vertices (ViewportRelative)
   if manager.hasComponent(EntID, VertexComponent):
      
      VertexComp : VertexComponent= manager.getComponent(EntID, VertexComponent)
      
      VerticesViewport = VertexComp.getViewportRelativeVertices(Transform.getScale(), Transform.rect)
      
   if Snap.ID[0] == None:
      
      if manager.hasComponent(mouseHolding[0], VertexComponent) and manager.hasComponent(mouseHolding[0], SeatComponent):
               
         Snap.ID = SnappToVertex(mouseHolding[0])

         return 
      
      SnappToSeat(mouseHolding[0])
   else:
      
      print(Snap.ID)

      if type(Snap.ID[1]) == int:

         #Get the Snapped to objects rect and seats
         SnappedTransform : TransformComponent = manager.getComponent(Snap.ID[0], TransformComponent)
         
         #Get the seat that EntID is snapped to (ViewportRelative)
         SeatComp : SeatComponent = manager.getComponent(Snap.ID[0], SeatComponent)

         Seats = SeatComp.getViewportRelativeSeats(SnappedTransform.getScale(), SnappedTransform.rect)

         #If not touching the seat anymore
         if not pointCollision(Seats[Snap.ID[1]]["Pos"], Transform.rect):

            #Leave seat both for EntID and for the seat
            Seats[Snap.ID[1]]["Occupied"] = -1
            
            Snap.ID = (None, -1)

         else:

            Transform.rect.center = Seats[Snap.ID[1]]["Pos"]

            Seats[Snap.ID[1]]["Occupied"] = mouseHolding[0]
            
         SeatComp.returnViewportRelativeSeats(SnappedTransform.getScale(), SnappedTransform.rect, Seats)

         return

      if type(Snap.ID[1]) == tuple:
         
         SnappedTransform : TransformComponent = manager.getComponent(Snap.ID[0], TransformComponent)

         SnappedVertexComp : VertexComponent = manager.getComponent(Snap.ID[0], VertexComponent)

         SnappedVerticesViewport = SnappedVertexComp.getViewportRelativeVertices(SnappedTransform.getScale(), SnappedTransform.rect)

         SnappedVertexViewport = SnappedVerticesViewport[Snap.ID[1][0]]                  
         VertexViewport = VerticesViewport[Snap.ID[1][1]]

         if pointCircleCollision(VertexViewport, SnappedVertexViewport, 25):

            VertexScaled = VertexComp.getScaledVertices(Transform.getScale())[Snap.ID[1][1]]
            pos = pygame.Vector2(0, 0)

            pos.x = SnappedVertexViewport.x - VertexScaled.y
            pos.y = SnappedVertexViewport.x - VertexScaled.y

            Transform.rect.topleft = pos
            
         else:

            Snap.ID = (None, -1)


def SnappToSeat(heldEnt:int):

   TransformComp : TransformComponent = manager.getComponent(heldEnt, TransformComponent)
   SnapComp : SnapComponent = manager.getComponent(heldEnt, SnapComponent)

   for table in Room["Tables"]:
      
      if not manager.hasComponent(table, SeatComponent):
         continue
         
      TableTransform : TransformComponent = manager.getComponent(table, TransformComponent)
      SeatComp : SeatComponent = manager.getComponent(table, SeatComponent)
      seats : list = SeatComp.getViewportRelativeSeats(TableTransform.getScale(), TableTransform.rect)
      
      for x in range(0, len(seats)):

         if pointCollision(seats[x]["Pos"], TransformComp.rect) and seats[x]["Occupied"] == -1 and mouseHolding[0] != table:

            SnapComp.ID = [table, x]

            seats[x]["Occupied"] = mouseHolding[0]

            SeatComp.returnViewportRelativeSeats(TableTransform.getScale(), TableTransform.rect, seats)

            return
         

def SnappToVertex(heldEnt:int):

   Transform : TransformComponent = manager.getComponent(heldEnt, TransformComponent)

   VertexComp : VertexComponent = manager.getComponent(heldEnt, VertexComponent)

   for table in Room["Tables"]:
      
      if mouseHolding[0] == table:
         continue

      if not manager.hasComponent(table, VertexComponent):
         continue
      
      tableTransform : TransformComponent = manager.getComponent(table, TransformComponent)

      tableVertexComp : VertexComponent = manager.getComponent(table, VertexComponent)
      tableVertices = tableVertexComp.getViewportRelativeVertices(tableTransform.getScale(), tableTransform.rect)


      Vertices = VertexComp.getViewportRelativeVertices(Transform.getScale(), Transform.rect)
      
      for Vertex in Vertices:
                        
         for tableVertex in tableVertices:

            if pointCircleCollision(Vertex, tableVertex, 25):

               return table, (tableVertices.index(tableVertex), Vertices.index(Vertex))

   return None, 0
