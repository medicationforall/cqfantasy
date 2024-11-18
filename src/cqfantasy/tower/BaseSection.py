import cadquery as cq
from cadqueryhelper import Base
from cqterrain.stairs.round import ramp as make_ramp, greebled_stairs as make_greebled_stairs, outline as make_outline
from . import TowerWindow, FrameWindow, TowerDoor, cut_cylinder, TileGenerator
from .magnets import make_magnet, make_magnets
from . import RoundBlockGenerator

try:
    log #type:ignore
except NameError:
    log = print

class BaseSection(Base):
    def __init__(self):
        super().__init__()

        # properties
        self.diameter:float = 130
        self.base_diameter:float|None = 150
        self.height:float = 100
        
        self.wall_width:float = 4
        self.floor_height:float = 4

        self.render_stairs:bool = True
        self.stair_count:int = 12
        self.stair_width = 30
        self.stair_rotate = -90
        self.floor_cut_rotate = 7

        self.render_window:bool = False
        self.window_padding:float = 6
        self.window_count:int = 2

        self.render_door:bool = False
        self.door_padding:float = 6
        self.door_count:int = 1

        self.render_magnets:bool = True
        self.magnet_diameter:float = 3.4
        self.magnet_height:float = 2.2
        self.magnet_count:int = 4

        self.render_floor_tile:bool = True
        self.tile_height:float = 2
        
        self.render_blocks = True

        #blueprints
        self.bp_window:TowerWindow|None = FrameWindow()
        self.bp_door:TowerDoor|None = TowerDoor()
        self.bp_tile_gen:TileGenerator|None = TileGenerator()
        self.bp_block_gen_outside:RoundBlockGenerator|None = RoundBlockGenerator()
        self.bp_block_gen_inside:RoundBlockGenerator|None = RoundBlockGenerator()

        # shapes
        self.body:cq.Workplane|None = None
        self.stairs:cq.Workplane|None = None
        self.magnets:cq.Workplane|None = None
        self.floor_cut:cq.Workplane|None = None
        

    def calculate_inner_height(self):
        return self.height - self.floor_height
    
    def make_body(self):
        log('make_body')

        if self.base_diameter is not None and self.base_diameter != self.diameter:
            body = cq.Solid.makeCone(
                self.base_diameter / 2, 
                self.diameter / 2, 
                self.height
            )
            
            body = cq.Workplane("XY").add(body)
        else:
            body = (
                cq.Workplane("XY")
                .cylinder(self.height, self.diameter / 2)
                .translate((0,0,self.height / 2))
            )
        
        if self.render_floor_tile:
            cut_cylinder_height = self.calculate_inner_height() + self.tile_height
        else:
            cut_cylinder_height = self.calculate_inner_height()

        small_diameter = self.calculate_smallest_diameter()
            
        body = cut_cylinder(body, small_diameter - self.wall_width*4, cut_cylinder_height)
        self.body = body

    def calculate_smallest_diameter(self):
        diameter = self.diameter
        if self.base_diameter is not None and self.base_diameter < self.diameter:
            diameter = self.base_diameter
        return diameter

    def calculate_largest_diameter(self):
        diameter = self.diameter
        if self.base_diameter is not None and self.base_diameter > self.diameter:
            diameter = self.base_diameter
        return diameter
    

    def make_window(self):
        if self.bp_window:
            log('make_window')
            outside_block_length = 0
            inside_block_length =  0

            if self.render_blocks and self.bp_block_gen_outside:
                outside_block_length = self.bp_block_gen_outside.block_length*1.5

            if self.render_blocks and self.bp_block_gen_inside:
                inside_block_length = self.bp_block_gen_inside.block_length*1.5

            self.bp_window.outside_diameter = self.calculate_largest_diameter() + outside_block_length
            self.bp_window.inside_diameter = self.calculate_smallest_diameter() - self.wall_width*4 - inside_block_length
            self.bp_window.make()

    def make_door(self):
        if self.bp_door:
            log('make_door')
            outside_block_length = 0
            inside_block_length =  0

            if self.render_blocks and self.bp_block_gen_outside:
                outside_block_length = self.bp_block_gen_outside.block_length*1.5

            if self.render_blocks and self.bp_block_gen_inside:
                inside_block_length = self.bp_block_gen_inside.block_length*1.5

            self.bp_door.outside_diameter = self.calculate_largest_diameter() + outside_block_length
            self.bp_door.inside_diameter = self.calculate_smallest_diameter() - self.wall_width*4 - inside_block_length
            self.bp_door.make()

    def make_magnets(self):
        log('make_magnets')
        magnet = make_magnet(self.magnet_diameter, self.magnet_height)
        self.magnets = (
            make_magnets(magnet, self.magnet_count, self.calculate_smallest_diameter() - self.wall_width*2)
            .translate((0,0,-self.magnet_height/2))
        )


    def make_stairs(self):
        log('make_stairs')
        diameter = self.calculate_smallest_diameter() - self.wall_width * 4
        inner_diameter = diameter - self.stair_width * 2
        height = self.calculate_inner_height()
        
        ramp = make_ramp(
            stair_count = self.stair_count,
            height = height,
            inner_diameter = inner_diameter,
            diameter = diameter,
            distance_overlap = 0.5,
            debug = False
        ).translate((0,0,height/2+self.floor_height))
        
        stairs = make_greebled_stairs(
            stair_count = self.stair_count,
            height = height,
            inner_diameter = inner_diameter,
            diameter = diameter, 
            debug=False
        ).translate((0,0,height/2+self.floor_height))
        
        self.stairs = stairs.cut(ramp.rotate((0,0,1),(0,0,0),-8))
        self.stairs = self.stairs.rotate((0,0,1), (0,0,0), self.stair_rotate)

    def make_blocks(self):
        log('make_blocks')
        if self.bp_block_gen_outside:
            log('make_blocks_outside')
            self.bp_block_gen_outside.top_diameter = self.diameter
            self.bp_block_gen_outside.base_diameter = self.base_diameter
            self.bp_block_gen_outside.height = self.height
            self.bp_block_gen_outside.make()
            
        if self.bp_block_gen_inside:
            log('make_blocks_inside')
            inner_diameter = self.calculate_smallest_diameter() - (self.wall_width * 4)
            self.bp_block_gen_inside.top_diameter = inner_diameter
            self.bp_block_gen_inside.base_diameter = inner_diameter
            self.bp_block_gen_inside.height = self.height
            self.bp_block_gen_inside.make()


    def make_floor_cut(self):
        log('make_floor_cut')
        diameter = self.diameter - self.wall_width * 4
        inner_diameter = diameter - self.stair_width * 2
        
        outline = make_outline(
            height = self.floor_height,
            inner_diameter = inner_diameter,
            diameter = diameter,
            rotate = 50
        ).rotate((0,0,1),(0,0,0),self.floor_cut_rotate)
        
        self.floor_cut = outline


    def build_cut_windows(self):
        if self.bp_window:
            log('build_cut_windows')
            window_cut = (
                self.bp_window.build_cut()
                .translate((0,0,self.height/2))
            ).rotate((0,0,1),(0,0,0),-90)
            
            window_cuts = cq.Workplane("XY")
            window_degrees = 360 / self.window_count
            for i in range(self.window_count):
                window_cuts = (
                    window_cuts
                    .union(window_cut.rotate((0,0,1),(0,0,0),window_degrees*i))
                )

            return window_cuts
    
    def build_windows(self):
        if self.bp_window:
            log('build_windows')
            window = (
                self.bp_window.build()
                .translate((0,0,self.height/2))
            ).rotate((0,0,1),(0,0,0),-90)
            
            windows = cq.Workplane("XY")
            window_degrees = 360 / self.window_count
            for i in range(self.window_count):
                windows = (
                    windows
                    .union(window.rotate((0,0,1),(0,0,0),window_degrees*i))
                )

            return windows
    
    def build_cut_door(self):
        if self.bp_door:
            log('build_cut_door')
            door_cut = (
                self.bp_door.build_cut()
                .translate((0,0,self.bp_door.height/2+self.floor_height))
            ).rotate((0,0,1),(0,0,0),-180)
            
            door_cuts = cq.Workplane("XY")
            door_degrees = 360 / self.door_count
            for i in range(self.door_count):
                door_cuts = (
                    door_cuts
                    .union(door_cut.rotate((0,0,1),(0,0,0),door_degrees*i))
                )
            return door_cuts
    
    def build_doors(self):
        if self.bp_door:
            log('build_doors')
            door = (
                self.bp_door.build()
                .translate((0,0,self.bp_door.height/2+self.floor_height))
            ).rotate((0,0,1),(0,0,0),-180)
            
            doors = cq.Workplane("XY")
            door_degrees = 360 / self.door_count
            for i in range(self.door_count):
                #log(f' add door {i=}')
                doors = (
                    doors
                    .union(door.rotate((0,0,1),(0,0,0),door_degrees*i))
                )
            return doors