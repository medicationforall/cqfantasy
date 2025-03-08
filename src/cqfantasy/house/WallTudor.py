import cadquery as cq
from . import tudor_wall
from cadqueryhelper import Base
from . import tudor_wall

class WallTudor(Base):
    def __init__(self):
        super().__init__()

        #parameters
        self.length:float = 100
        self.height:float = 75 
        self.styles:list[str|None]|str|None = [None,"cross","left","right"]
        self.panel_length:float = 25
        self.panel_space:float = 3 
        self.panel_width:float = 3

        #shapes
        self.tudor_wall = None

    def make_tudor_wall(self):
        self.tudor_wall = tudor_wall(
            length =  self.length, 
            height = self.height, 
            styles = self.styles, 
            panel_length = self.panel_length, 
            panel_space = self.panel_space, 
            panel_width = self.panel_width
        )


    def make(self, parent=None):
        super().make(parent)
        self.make_tudor_wall()

    def build(self)->cq.Workplane:
        super().build()

        scene = cq.Workplane("XY")

        if self.tudor_wall:
            scene = scene.union(self.tudor_wall)

        return scene