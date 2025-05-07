import cadquery as cq
from cadqueryhelper import Base
#from ..house_wall import WallTudor, WallStuccoBrick, WallTudorPaneling

class WallSplit(Base):
    def __init__(self):
        super().__init__()

        #parameters
        self.length:float = 100
        self.width:float = 5
        self.height:float = 75

        self.split_height:float = 3

        self.split_divide_height:float = 25

        # blueprints
        self.bp_upper_wall = None
        self.bp_lower_wall = None

        #shapes
        self.split:cq.Workplane|None = None
        self.outline:cq.Workplane|None = None

    def make_split(self):
        split = cq.cq.Workplane("XY").box(self.length, self.width, self.split_height)
        self.split = split

    def make_outline(self):
        self.outline = cq.Workplane("XY").box(self.length, self.width, self.height)
    
    def make(self, parent=None):
        super().make(parent)
        self.make_outline()
        self.make_split()

        if self.bp_upper_wall:
            self.bp_upper_wall.length = self.length
            self.bp_upper_wall.width = self.width
            self.bp_upper_wall.height = self.height - self.split_divide_height - self.split_height/2
            #log(f'{self.height=} {self.split_divide_height=} {self.bp_upper_wall.height=}')
            self.bp_upper_wall.make()

        if self.bp_lower_wall:
            self.bp_lower_wall.length = self.length
            self.bp_lower_wall.width = self.width
            self.bp_lower_wall.height = self.split_divide_height - self.split_height/2
            self.bp_lower_wall.make()

    def build(self):
        super().build()
        scene = cq.Workplane("XY")
        
        if self.bp_lower_wall:
            lower_wall = self.bp_lower_wall.build()
            scene = scene.add(lower_wall.translate((0,0,-self.height/2+self.bp_lower_wall.height/2)))
        
        if self.bp_upper_wall:
            upper_wall = self.bp_upper_wall.build()
            scene = scene.add(upper_wall.translate((0,0,self.height/2-self.bp_upper_wall.height/2)))

        if self.split:
            scene = scene.add(self.split.translate((0,0,-self.height/2+self.split_divide_height)))

        return scene
    
    def build_cut(self):
        return self.outline