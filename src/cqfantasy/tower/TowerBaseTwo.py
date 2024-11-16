# Copyright 2024 James Adams
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import cadquery as cq
from cadqueryhelper import Base
from cqterrain.stairs.round import ramp as make_ramp, greebled_stairs as make_greebled_stairs
from . import TowerWindow, FrameWindow, TowerDoor, cut_cylinder, TileGenerator
from .magnets import make_magnet, make_magnets
from . import RoundBlockGenerator

try:
    log #type:ignore
except NameError:
    log = print


class TowerBaseTwo(Base):
    def __init__(self):
        super().__init__()
        
        # properties
        self.diameter:float = 130
        self.base_diameter:float = 150
        self.height:float = 100
        
        self.wall_width:float = 4
        self.floor_height:float = 4
        
        self.render_stairs:bool = True
        self.stair_count:int = 12

        self.render_window:bool = True
        self.window_length:float = 12
        self.window_width:float = 18
        self.window_height:float = 40
        self.window_padding:float = 6
        self.window_count:int = 2
        
        self.render_door:bool = True
        self.door_length:float = 30
        self.door_width:float = 27
        self.door_height:float = 50
        self.door_padding:float = 7
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
        self.base:cq.Workplane|None = None
        self.stairs:cq.Workplane|None = None
        self.magnets:cq.Workplane|None = None
        
    def calculate_inner_height(self):
        return self.height - self.floor_height
        
    def make_base(self):
        log('make_base')
        base = cq.Solid.makeCone(
            self.base_diameter/2, 
            self.diameter/2, 
            self.height
        )
        
        base = cq.Workplane("XY").add(base)
        if self.render_floor_tile:
            cut_cylinder_height = self.calculate_inner_height() + self.tile_height
        else:
            cut_cylinder_height = self.calculate_inner_height()
            
        base = cut_cylinder(base, self.diameter - self.wall_width*4, cut_cylinder_height)
        self.base = base
        
    def make_window(self):
        if self.bp_window:
            log('make_window')
            outline_diameter = (self.base_diameter - self.diameter) / 2
            self.bp_window.diameter = self.base_diameter-outline_diameter + self.window_padding
            self.bp_window.length = self.window_length
            self.bp_window.width = self.window_width
            self.bp_window.height = self.window_height
            self.bp_window.make()
        
    def make_door(self):
        if self.bp_door:
            log('make_door')
            self.bp_door.diameter = self.base_diameter + self.door_padding
            self.bp_door.length = self.door_length
            self.bp_door.width = self.door_width
            self.bp_door.height = self.door_height
            self.bp_door.make()
        
    def make_stairs(self):
        log('make_stairs')
        diameter = self.diameter - self.wall_width*4
        inner_diameter = diameter - 60
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

    def make_magnets(self):
        log('make_magnets')
        magnet = make_magnet(self.magnet_diameter, self.magnet_height)
        self.magnets = (
            make_magnets(magnet, self.magnet_count, self.diameter - self.wall_width*2)
            .translate((0,0,-self.magnet_height/2))
        )
        
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
            inner_diameter = self.diameter-(self.wall_width*4)
            self.bp_block_gen_inside.top_diameter = inner_diameter
            self.bp_block_gen_inside.base_diameter = inner_diameter
            self.bp_block_gen_inside.height = self.height
            self.bp_block_gen_inside.make()
        
    def make(self, parent=None):
        super().make(parent)
        log('make')
        
        self.make_base()
        
        if self.render_window:
            self.make_window()
        
        if self.render_door:
            self.make_door()

        if self.render_stairs:
            self.make_stairs()

        if self.render_magnets:
            self.make_magnets()

        if self.render_floor_tile and self.bp_tile_gen:
            self.bp_tile_gen.diameter = self.diameter - self.wall_width*4
            self.bp_tile_gen.tile_height = self.tile_height
            self.bp_tile_gen.make()
            
        if self.render_blocks:
            self.make_blocks()
        
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
      
    def build(self):
        log('build')
        super().build()
        
        cut_windows = self.build_cut_windows()
        windows = self.build_windows()

        cut_doors = self.build_cut_door()
        doors = self.build_doors()  
        
        scene = cq.Workplane("XY")

        if self.base:
            log('union base')
            scene = scene.union(self.base)
            
        if self.render_blocks and self.bp_block_gen_outside:
            log('build outside blocks')
            blocks_outside = self.bp_block_gen_outside.build()
            scene = scene.union(blocks_outside)
            
        if self.render_blocks and self.bp_block_gen_inside:
            log('build inside blocks')
            blocks_inside = self.bp_block_gen_inside.build()
            scene = scene.union(blocks_inside)

        if self.stairs:
            log('union Stairs')
            scene = scene.union(self.stairs)

        if cut_windows:
            log('cut cut_windows')
            scene = scene.cut(cut_windows)

        if windows:
            log('union windows')
            scene = scene.union(windows)

        if cut_doors:
            log('cut cut_doors')
            scene = scene.cut(cut_doors)
        
        if doors:
            log('union door')
            scene = scene.union(doors)

        if self.magnets:
            log('cut magnets')
            scene = scene.cut(self.magnets.translate((0,0,self.height)))

        if self.render_floor_tile and self.bp_tile_gen:
            log('union tiles')
            tiles = self.bp_tile_gen.build()
            offset_height = self.floor_height
            scene = scene.union(tiles.translate((0,0,offset_height-self.tile_height/2)))

        return scene