import cadquery as cq
from cadqueryhelper import Base
from typing import Tuple

class Roof(Base):
    def __init__(self):
        super().__init__()
        #parameters
        self.length:float = 100
        self.width:float = 150
        self.height:float = 75
        
        self.overhang:Tuple[float,float,float] = (4,4,4)
        
        #shapes
        self.roof:cq.Workplane|None = None
        self.roof_cut:cq.Workplane|None = None
        
    def make_roof(self):
        pts = [(0,0),(self.length,0),((self.length/2,self.height))]
        roof = (
            cq.Workplane("XZ")
            .polyline(pts)
            .close()
            .extrude(self.width)
        ).translate((-self.length/2, self.width/2,-self.height/2))
                
        self.roof = roof
        
    def make_roof_cut(self):
        length = self.length - self.overhang[0]*2
        width = self.width - self.overhang[1]*2
        height = self.height - self.overhang[2]*2
        
        pts = [(0,0),(length,0),((length/2,height))]
        roof_cut = (
            cq.Workplane("XZ")
            .polyline(pts)
            .close()
            .extrude(width)
        ).translate((-length/2, width/2,-self.height/2))
                
        self.roof_cut = roof_cut
        
        
    def make(self, parent=None):
        super().make(parent)
        self.make_roof()
        self.make_roof_cut()
        
    def build(self) -> cq.Workplane:
        super().build()
        scene = (
            cq.Workplane("XY")
        )

        if self.roof:
            scene = scene.union(self.roof)

        if self.roof_cut:
            scene = scene.cut(self.roof_cut)
        return scene