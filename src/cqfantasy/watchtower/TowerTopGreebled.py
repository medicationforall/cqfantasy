import cadquery as cq
from cadqueryhelper import Base
from cqterrain.floor import WoodFloor
from ..house import House, BodyGreebled
from ..window import CasementWindow
from ..house_wall import LogWall


class TowerTopGreebled(Base):
    
    def __init__(self):
        super().__init__()
        #parameters
        self.length:float = 115
        self.width:float = 115
        self.height:float = 75
        self.render_floor_tiles:bool = True
        self.render_inside_walls:bool = True
        self.render_outside_walls:bool = True
        self.render_windows:bool = True
        self.render_roof:bool = True
        
        #blueprints
        self.bp_house = self.init_house()
                
        #shapes
        self.outline:cq.Workplane|None = None
        
    def init_house(self):
        #log('init_house')
        bp_house = House()
        bp_house.length = 115
        bp_house.width = 115
        bp_house.render_roof = False
        bp_house.render_doors = False
        bp_house.render_windows = True
        
        #windows
        bp_house.window_space = (115/2,115)
        bp_house.window_x_style = []
        bp_house.window_y_style = []
        
        bp_house.bp_window = CasementWindow()
        bp_house.window_length = 30
        bp_house.window_offset = 8.25
        bp_house.window_width = 2
        bp_house.bp_window.height = 25
        bp_house.bp_window.width = 5
        bp_house.bp_window.grill_width=1.8
        bp_house.bp_window.grill_height=1.8
        
        #body style
        bp_body = BodyGreebled()
        
        #floor
        bp_body.floor_height = 4
        bp_body.render_floor_tiles = True
        bp_floor = WoodFloor()
        bp_floor.board_height = 2.5
        bp_body.bp_tile_generator = bp_floor
        bp_body.bp_tile_generator.board_width = 7
        bp_body.bp_tile_generator.board_width_spacer = .25
        bp_body.bp_tile_generator.board_break_width = .4
        bp_body.bp_tile_generator.nail_diameter = .8
        bp_body.bp_tile_generator.nail_overlap_height = .2
        bp_body.bp_tile_generator.nail_x_margin = .6
        bp_body.bp_tile_generator.nail_y_margin = 0
        
        #outside walls
        bp_log_wall = LogWall()
        bp_log_wall.width = 5
        
        bp_body.render_outside_walls = True
        bp_body.bp_outside_walls = [
            bp_log_wall, 
            bp_log_wall, 
            bp_log_wall, 
            bp_log_wall
        ]
        
        bp_body.render_inside_walls = True
        bp_body.bp_inside_walls = [
            bp_log_wall, 
            bp_log_wall, 
            bp_log_wall, 
            bp_log_wall
        ]
        
        bp_house.bp_body = bp_body
        return bp_house
        
    def make_outline(self):
        outline = cq.Workplane("XY").box(
            self.length,
            self.width,
            self.height
        )
        
        self.outline = outline
        
    def make_top(self):
        self.bp_house.length = self.length
        self.bp_house.width = self.width
        self.bp_house.height = self.height
        self.bp_house.bp_body.render_floor_tiles = self.render_floor_tiles
        self.bp_house.bp_body.render_inside_walls = self.render_inside_walls
        self.bp_house.bp_body.render_outside_walls = self.render_outside_walls
        self.bp_house.render_windows = self.render_windows
        self.bp_house.render_roof = self.render_roof
        self.bp_house.make()
        
    def make(self):
        super().make()
        self.make_outline()
        self.make_top()
        
    def build_outline(self)->cq.Workplane:
        super().build()
        
        part = cq.Workplane("XY")
        
        if self.outline:
            part = part.add(self.outline)
        
        return part
        
    def build(self)->cq.Workplane:
        super().build()
        
        part = cq.Workplane("XY")
        
        if self.bp_house:
            ex_house =  self.bp_house.build()
            part = part.add(ex_house)
        
        return part