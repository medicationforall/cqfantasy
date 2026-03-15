import cadquery as cq
from cadqueryhelper import Base
from cqterrain.floor import WoodFloor
from ..house import House, BodyGreebled
from ..house_wall import RubbleWall
from ..corner import AshlarCorner
from cqterrain import Ladder
from . import TowerDoor


class TowerBodyGreebled(Base):
    def __init__(self):
        super().__init__()
        #parameters
        self.length:float = 75
        self.width:float = 75
        self.height:float = 125
        
        self.render_doors:bool = True
        self.render_windows:bool = True
        self.render_outside_walls:bool = True
        self.render_inside_walls:bool = True
        self.render_floor_tiles:bool = True
        self.render_outside_corners:bool = True
        self.render_ladder:bool = True
        self.render_door_cross_section:bool = False
        self.seed:str = "tower_test_1"
        
        self.ladder_translate:float = 0
        self.door_height:float = 47
        self.door_pivot_height:float = 45
        self.window_offset:float = 8.25 + 15
        self.door_rotate:float = 0 
        
        # blue prints
        self.bp_tower:Base = self.init_body()
        self.bp_ladder:Base = Ladder()
        
        #shapes
        self.outline:cq.Workplane|None = None
        
    def init_body(self):
        bp_house = House()
        bp_house.length = 75
        bp_house.width = 75
        bp_house.height = 150
        bp_house.render_roof = False
        bp_house.render_doors = True
        bp_house.render_windows = True
        
        # door
        bp_house.bp_door = TowerDoor()
        bp_house.door_cut_width_padding = 7
        
        #windows
        bp_house.window_space = (75/3,75/3)
        bp_house.window_x_style = ([None,'win',None],None)
        bp_house.window_y_style = [None,'win',None]
        bp_house.windows_z_translate = 0
        
        #bp_house.bp_window = CasementWindow()
        bp_house.window_length = 15
        bp_house.window_offset = 8.25 + 15
        bp_house.window_width = 2
        bp_house.bp_window.height = 35
        bp_house.bp_window.width = 9
        #bp_house.bp_window.grill_width=1.8
        #bp_house.bp_window.grill_height=1.8
        
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
        bp_outside_walls = []
        
        for i in range(4):
            bp_rubble = RubbleWall()
            bp_wall = bp_rubble.bp_wall
            
            bp_rubble.width = 2
            bp_rubble.width = (2,3,.5)
            bp_rubble.x_padding = 0
            seed = self.seed
            bp_rubble.seed = f'{seed}_{i}'
            #log(bp_rubble.seed)
            bp_outside_walls.append(bp_rubble)
        
        bp_body.render_outside_walls = False
        bp_body.bp_outside_walls = bp_outside_walls
        
        
        bp_inside_walls = []
        
        for i in range(4):
            bp_rubble = RubbleWall()
            #bp_rubble.width = (1,3,1)
            bp_rubble.width = 2
            seed = self.seed
            bp_rubble.seed = f'{seed}_{i}'
            bp_inside_walls.append(bp_rubble)
        
        bp_body.render_inside_walls = False
        bp_body.bp_inside_walls = bp_inside_walls
        
        #corners
        bp_corner = AshlarCorner()
        bp_corner.length = 15
        bp_corner.width = 15
        bp_corner.stone_height = 125/11
        bp_corner.corner_cut_length = 4
        bp_corner.corner_cut_width = 4
        bp_body.bp_outside_corners = bp_corner
        
        bp_house.bp_body = bp_body
        
        return bp_house
        
    def make_outline(self):
        outline = cq.Workplane("XY").box(
            self.length,
            self.width,
            self.height
        )
        
        self.outline = outline
        
    def make_body(self):
        if self.bp_tower:
            self.bp_tower.length = self.length
            self.bp_tower.width = self.width
            self.bp_tower.height = self.height
            
            self.bp_tower.render_doors = self.render_doors
            self.bp_tower.render_windows = self.render_windows
            self.bp_tower.bp_body.render_outside_walls = self.render_outside_walls
            self.bp_tower.bp_body.render_inside_walls = self.render_inside_walls
            self.bp_tower.bp_body.render_outside_corners = self.render_outside_corners
            self.bp_tower.bp_body.render_floor_tiles = self.render_floor_tiles
            self.bp_tower.make()
            
    def make_ladder(self):
        height = self.bp_tower.bp_body.calculate_internal_height()
        self.bp_ladder.height = height
        self.bp_ladder.make()
        
        
    def make_door(self):
        self.bp_tower.bp_door.width = self.bp_tower.bp_body.wall_width+1
        #self.bp_tower.bp_door.door_width = self.bp_tower.bp_body.wall_width - .5
        #self.bp_tower.bp_door.pivot_diameter = 2.5
        self.bp_tower.bp_door.height = self.door_height
        self.bp_tower.bp_door.pivot_height = self.door_pivot_height
        self.bp_tower.bp_door.render_cross_section = self.render_door_cross_section
        self.bp_tower.bp_door.rotate = self.door_rotate 
        
    def make_windows(self):
        self.bp_tower.window_offset = self.window_offset
            
    def make_stones(self):
        #apply seed
        inside_walls = self.bp_tower.bp_body.bp_inside_walls
        
        for i,wall in enumerate(inside_walls):
            seed = f'{self.seed}_{i}'
            wall.seed = seed
            
        outside_walls = self.bp_tower.bp_body.bp_outside_walls
        for i,wall in enumerate(outside_walls):
            seed = f'{self.seed}_{i}'
            wall.seed = seed
        
    def make(self):
        super().make()
        self.make_outline()
        self.make_stones()
        self.make_door()
        self.make_windows()
        self.make_body()
        self.make_ladder()
        
    def build_outline(self)->cq.Workplane:
        super().build()
        
        part = cq.Workplane("XY")
        
        if self.outline:
            part = part.add(self.outline)
        
        return part

    def calculate_ladder_translate_y(self):
        translate_y = (self.width/2) - self.bp_tower.bp_body.wall_width - (self.bp_ladder.width/2) + self.ladder_translate
        return translate_y
        
    def build(self)->cq.Workplane:
        super().build()
        
        part = cq.Workplane("XY")
        
        if self.bp_tower:
            ex_body = self.bp_tower.build()
            part = part.add(ex_body)
            
        if self.render_ladder and self.bp_ladder:
            ex_ladder = self.bp_ladder.build()
            height = self.bp_tower.bp_body.calculate_internal_height() 
            adder = self.height - height
            translate_y = self.calculate_ladder_translate_y()
            part = part.union(ex_ladder.translate((0,translate_y,(height/2) + adder)))
        
        return part