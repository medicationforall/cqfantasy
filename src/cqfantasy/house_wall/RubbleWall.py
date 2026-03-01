import cadquery as cq
from cadqueryhelper import Base
from cqterrain.floor import ModPattern

class RubbleWall(Base):
    def __init__(self):
        super().__init__()
        #parameters
        self.length:float = 30
        self.width:float|tuple[float,float,float] = 3
        self.height:float = 60
        self.x_padding:float|None = None
        self.seed:str = 'test2'
        
        bp_wall:Base = ModPattern()
        bp_wall.x_spacing = [10,20]
        bp_wall.y_spacing = [10]
        bp_wall.row_x_mod = [0,1]
        bp_wall.row_x_offset = [0,-10/2]
        
        bp_wall.randomize_points = True
        bp_wall.shift_x = (-5,5,1)
        bp_wall.shift_y = (-5,0,1)
        
        bp_wall.x_stretch = 1
        bp_wall.y_stretch = 1
        
        bp_wall.taper = 10
        bp_wall.offset = -.25
        bp_wall.render_points = False
        
        bp_wall.debug = False
        bp_wall.column_pad = 2
        bp_wall.row_pad = 3
        bp_wall.enforce_even_columns = True
        bp_wall.enforce_even_rows = True
        bp_wall.grid_offset_x = -1.25 - 4
        bp_wall.grid_offset_y = 12
        
        bp_wall.interlock_cells = True
        bp_wall.start = 1
        bp_wall.top_end_index = 3
        bp_wall.bottom_start_index = 2
        bp_wall.top_cap_index = 3
        
        self.bp_wall:Base|None = bp_wall
        
        #shapes
        self.outline:cq.Workplane|None = None

    def calculate_length(self):
        if self.x_padding:
            return self.length + self.x_padding
        else:
            return self.length

    def calculate_width(self):
        if type(self.width) is tuple:
            return self.width[1]
        else:
            return self.width
        
    def make_outline(self):
        length = self.calculate_length()
        width = self.calculate_width()
        outline = cq.Workplane("XY").box(
            length,
            width,
            self.height
        )
        
        self.outline = outline
        
    def make_wall(self):
        length = self.calculate_length()
        width = self.width
        height = self.height
        seed = self.seed
        bp_wall = self.bp_wall
        
        if bp_wall:
            bp_wall.length = length
            bp_wall.width = height
            bp_wall.height = self.width
            bp_wall.seed = seed
            bp_wall.make()
        
    def make(self):
        super().make()
        self.make_wall()
        self.make_outline()
        
    def build_outline(self)->cq.Workplane:
        super().build()
        
        part = cq.Workplane("XY")
        
        if self.outline:
            part = part.add(self.outline)
        
        return part
        
    def build(self)->cq.Workplane:
        super().build()
        
        part = cq.Workplane("XY")
        
        if self.bp_wall:
            width = self.calculate_width()
            ex_wall = self.bp_wall.build()
            ex_wall = (
                ex_wall
                .translate((0,0,-width/2))
                .rotate((1,0,0),(0,0,0),-90)
            )
            part = part.add(ex_wall)
        
        return part