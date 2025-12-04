import cadquery as cq
from cadqueryhelper import Base

class Hearth(Base):
    def __init__(self):
        super().__init__()
        #parameters
        self.length:float = 35
        self.width:float = 35
        self.height:float = 3

        #shapes
        self.outline:cq.Workplane|None = None
        self.hearth:cq.Workplane|None = None
        
    def make_outline(self):
        outline = cq.Workplane("XY").box(
            self.length,
            self.width,
            self.height
        )
        
        self.outline = outline
        
    def make_hearth(self):
        hearth = cq.Workplane("XY").box(
            self.length,
            self.width,
            self.height
        )
        
        self.hearth = hearth
        
    def make(self):
        super().make()
        self.make_outline()
        self.make_hearth()
        
    def build_outline(self)->cq.Workplane:
        super().build()
        
        part = cq.Workplane("XY")
        
        if self.outline:
            part.add(self.outline.translate((0,0,self.height/2)))
        
        return part
        
    def build(self)->cq.Workplane:
        super().build()
        
        part = cq.Workplane("XY")
        
        if self.hearth:
            part.add(self.hearth.translate((0,0,self.height/2)))
        
        return part