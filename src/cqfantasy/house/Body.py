import cadquery as cq
from cadqueryhelper import Base

class Body(Base):
    def __init__(self):
        super().__init__()
        #parameters
        self.length:float = 150
        self.width:float = 150
        self.height:float = 75
        self.wall_width:float = 4
        self.floor_height:float = 4
        
        #shapes
        self.body:cq.Workplane|None = None
        
    def make_body(self):
        body = (
            cq.Workplane("XY")
            .box(self.length, self.width, self.height)
        )
        
        body = (
            body
            .faces("Z")
            .rect(self.length-self.wall_width*2,self.width-self.wall_width*2)
            .extrude(-self.height+self.floor_height, combine="s")
        )
        
        self.body = body
        
    def make(self, parent=None):
        super().make(parent)
        self.make_body()
        
    def build(self) -> cq.Workplane:
        super().build()

        scene = cq.Workplane("XY")

        if self.body:
            scene = scene.union(self.body)
            
        return scene