import cadquery as cq
from cadqueryhelper.hinge import SimpleHinge, SimpleDoor
from cqterrain.door import TiledDoor

class TowerDoor(SimpleHinge):
    def __init__(self):
        super().__init__()
        #parameters
        self.length:float = 36
        self.width:float = 5
        self.height:float = 60
        self.door_width:float = 4
        self.frame_width = 2
        self.pivot_height = self.height - 2
        self.rotate = 0
        
        #blueprints
        self.bp_door = self.init_door()
        
        #shapes
        self.outline:cq.Workplane|None = None
        
    def init_door(self):
        bp_hinged_door = SimpleDoor()
        bp_tile_door = TiledDoor()
        bp_tile_door.handle_mirrored = True
        
        bp_tile_door.handle_handle_length = 1.5
        bp_tile_door.handle_x_margin = (
            self.calculate_door_length() - 4)
        
        bp_hinged_door.bp_door = bp_tile_door
        return bp_hinged_door
        
    def build(self)->cq.Workplane:
        part = super().build()
        return part