import cadquery as cq
from cadqueryhelper import Base
from cadqueryhelper.grid import grid_points_random, cell_stretch_points, grid_cell_basic
import math

class HillBase(Base):
    def __init__(self):
        super().__init__()
        #parameters
        self.length:float = 125
        self.width:float = 125
        self.height:float = 10
        self.taper = 30
        self.x_spacing = 5
        self.y_spacing = 5
        self.shift_x = (-2, 2, 1)
        self.shift_y = (-2, 2, .5)
        self.seed = "test9"
        
        #shapes
        self.outline:cq.Workplane|None = None
        self.base_grid = None
        
    def make_outline(self):
        outline = cq.Workplane("XY").box(
            self.length,
            self.width,
            self.height
        )
        
        self.outline = outline
        
    def make_base(self):
        outline = cq.Workplane("XY").box(
            self.length,
            self.width,
            self.height
        )
        
        columns = math.floor(self.length/self.x_spacing)
        rows = math.floor(self.width/self.y_spacing)
        
        points, stream = grid_points_random(
            columns = columns,
            rows = math.floor(self.width/self.y_spacing),
            x_spacing = self.x_spacing,
            y_spacing = self.y_spacing,
            shift_x = self.shift_x,#min max step
            shift_y = self.shift_y,#min max step
            seed = self.seed
        )
        
        cell_points = cell_stretch_points(
            points,
            x_stretch = columns-1,
            y_stretch = rows-1
        )
        
        grid = grid_cell_basic(
            cell_points,
            height=self.height,
            taper= self.taper
        )
        
        self.base_grid = grid
        
        
    def make(self):
        super().make()
        self.make_outline()
        self.make_base()
        
    def build_outline(self)->cq.Workplane:
        super().build()
        
        part = cq.Workplane("XY")
        
        if self.outline:
            part = part.add(self.outline)
        
        return part
        
    def build(self)->cq.Workplane:
        super().build()
        
        part = cq.Workplane("XY")
        
        if self.base_grid:
            part = part.add(self.base_grid.translate((-self.length/2,self.width/2,0)))
        
        return part