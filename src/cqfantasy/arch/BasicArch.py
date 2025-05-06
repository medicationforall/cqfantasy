import math
import cadquery as cq
from cadqueryhelper import Base
from . import arch


class BasicArch(Base):
    def __init__(self):
        super().__init__()

        # parameters
        self.length:float = 30
        self.width:float = 5
        self.height:float = 75
        self.outside_margin:float = 10
        self.inside_margin:float = 5
        
        # shapes
        self.outline:cq.Workplane|None = None
        self.outside_outline:cq.Workplane|None = None
        self.inside_outline:cq.Workplane|None = None
        self.column_outline:cq.Workplane|None = None
        
    def calculate_column_height(self) -> float:
        return (self.height)-self.length/2
    
    def calculate_perimeter(self) -> float:
        perimeter = 2*math.pi*self.length/2
        return perimeter
    
    def calculate_inside_perimeter(self) -> float:
        perimeter = 2*math.pi*(self.length-self.inside_margin*2)/2
        return perimeter
    
    def calculate_outside_perimeter(self) -> float:
        perimeter = 2*math.pi*(self.length+self.outside_margin*2)/2
        return perimeter
        
        
    def make_outline(self):
        self.outline = arch(
            self.length, 
            self.width, 
            self.height
        )
        
    def make_outside_outline(self):
        self.outside_outline = arch(
            self.length+self.outside_margin*2, 
            self.width, 
            self.height+self.outside_margin
        ).translate((0,0,self.outside_margin/2))
        
    def make_inside_outline(self):
        self.inside_outline = arch(
            self.length-self.inside_margin*2, 
            self.width, 
            self.height-self.inside_margin
        ).translate((0,0,-self.inside_margin/2))
        
    def make_column_outline(self):
        height = self.calculate_column_height()
        outline = (
            cq.Workplane("XY")
            .box(
                self.length+self.outside_margin*2,
                self.width,
                height
            )
            .translate((0,0,-self.height/2+height/2))
        )
        self.column_outline = outline
        
    def make(self, parent=None):
        super().make(parent)
        self.make_outline()
        self.make_outside_outline()
        self.make_inside_outline()
        self.make_column_outline()
        
    def build(self) -> cq.Workplane:
        super().build()
        scene = (
            cq.Workplane("XY")
        )

        if self.outline:
            scene = scene.add(self.outline)

        if self.outside_outline:
            scene = scene.add(self.outside_outline)

        if self.inside_outline:
            scene = scene.cut(self.inside_outline)

        return scene
    
    def build_outline(self) -> cq.Workplane:
        scene = cq.Workplane("XY")
        
        if self.outline:
            scene = scene.union(self.outline)
        return scene