import cadquery as cq
from cadqueryhelper import Base
from cqterrain.door import TiledDoor

class TowerDoor(Base):
    def __init__(self):
        super().__init__()
        # properties
        self.length:float = 25
        self.width:float = 2
        self.height:float = 30

        self.frame_width:float = 4
        
        self.diameter:float = 130
        
        # shapes
        self.outline:cq.Workplane|None = None
        self.cut:cq.Workplane|None = None

        # blueprints
        self.bp_door = TiledDoor()

    def make_outline(self):
        outline = (
            cq.Workplane("XY")
            .cylinder(self.height, self.diameter/2)
            .cylinder(self.height, self.diameter/2-self.width, combine="cut")
        )
        
        self.outline = outline

    def make_door(self):
        self.bp_door.length = self.length
        self.bp_door.width = self.frame_width
        self.bp_door.height = self.height
        self.bp_door.make()

    def make_cut(self):
        cut_width = self.diameter /2
        
        cut = cq.Workplane("XY").box(
          length = self.length,
          width = cut_width,
          height = self.height
        )
        
        scene = (
            cq.Workplane("XY")
            .union(self.outline)
            .intersect(cut.translate((0,(self.diameter/2-self.width/2)-self.width/4,0)))
        )
        
        self.cut = scene

    def make(self, parent=None):
        self.parent = parent
        self.make_called = True

        self.make_outline()
        self.make_cut()
        self.make_door()

    def build_cut(self):
        scene = cq.Workplane("XY").union(self.cut)
        
        #if self.render_outline and self.outline:
        #    scene = scene.add(self.outline)   
        return scene
    
    def build(self):
        super().build()
        scene = (
            cq.Workplane("XY")
        )

        door = self.bp_door.build()

        if door:
            scene = scene.union(door.translate((0,(self.diameter/2-self.width/2)-self.width/4,0)))
        
        return scene