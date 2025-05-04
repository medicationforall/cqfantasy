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
from . import RoundBlockGenerator, BaseSection

try:
    log #type:ignore
except NameError:
    log = print


class TowerBase(BaseSection):
    def __init__(self):
        super().__init__()
        # properties
        self.door_padding:float = 6
        self.door_count:int = 1

        self.render_window:bool = True
        self.window_padding:float = 6
        self.window_count:int = 2

        self.render_door:bool = True
        self.door_padding:float = 6
        self.door_count:int = 1

        self.stair_rotate = 0

        # Init values
        if self.bp_block_gen_outside:
            self.bp_block_gen_outside.block_length = 2.5
            self.bp_block_gen_outside.row_count = 9
            self.bp_block_gen_outside.margin = (.5,.5)
            self.bp_block_gen_outside.modulus_even = 0

        if self.bp_block_gen_inside:
            self.bp_block_gen_inside.block_length = 2.5
            self.bp_block_gen_inside.row_count = 9
            self.bp_block_gen_inside.margin = (.5,.5)
            self.bp_block_gen_inside.modulus_even = 0

        if self.bp_window:
            self.bp_window.length = 12
            self.bp_window.height = 40

        if self.bp_door:
            self.bp_door.length = 30
            self.bp_door.height = 50

        
    def make(self, parent=None):
        super().make(parent)
        log('make')
        
        self.make_body()
        
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
      
    def build(self) -> cq.Workplane:
        log('build')
        super().build()
        
        cut_windows = self.build_cut_windows()
        windows = self.build_windows()

        cut_doors = self.build_cut_door()
        doors = self.build_doors()  
        
        scene = cq.Workplane("XY")

        if self.body:
            log('union base')
            scene = scene.union(self.body)
            
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