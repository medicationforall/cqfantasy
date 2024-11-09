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
from . import TowerWindow, cut_cylinder, TileGenerator
from .magnets import make_magnet, make_magnets
import math


class TowerBase(Base):
    def __init__(self):
        super().__init__()
        
        # properties
        self.diameter:float = 130
        self.base_diameter:float = 150
        self.height:float = 100
        
        self.wall_width:float = 4
        self.floor_height:float = 4
        
        self.block_length:float = 5
        self.block_width:float = 14
        self.block_height:float = 10
        
        self.block_ring_count:int = 30
        self.even_ring_rotate:float = 6
        
        self.render_blocks:bool = True
        self.render_stairs:bool = True
        self.render_window_outline:bool = False
        
        self.window_length:float = 12
        self.window_width:float = 18
        self.window_height:float = 40
        self.window_padding:float = 6
        self.window_count:int = 2
        
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
        self.tile_height = 2

        #blueprints
        self.bp_window:TowerWindow = TowerWindow()
        self.bp_door:TowerWindow = TowerWindow()
        self.bp_tile_gen:TileGenerator|None = TileGenerator()

        # shapes
        self.base:cq.Workplane|None = None
        self.stairs:cq.Workplane|None = None
        self.magnets:cq.Workplane|None = None
        
    def make_window(self):
        outline_diameter = (self.base_diameter - self.diameter) / 2
        self.bp_window.diameter = self.base_diameter-outline_diameter + self.window_padding
        self.bp_window.length = self.window_length
        self.bp_window.width = self.window_width
        self.bp_window.height = self.window_height
        self.bp_window.render_outline = self.render_window_outline
        self.bp_window.make()
        
    def make_door(self):
        self.bp_door.diameter = self.base_diameter + self.door_padding
        self.bp_door.length = self.door_length
        self.bp_door.width = self.door_width
        self.bp_door.height = self.door_height
        self.bp_door.make()

    def make_magnets(self):
        magnet = make_magnet(self.magnet_diameter, self.magnet_height)
        self.magnets = (
            make_magnets(magnet, self.magnet_count, self.diameter - self.wall_width*2)
            .translate((0,0,-self.magnet_height/2))
        )
        
    def make(self, parent=None):
        super().make(parent)
        
        self.make_base()
        self.make_window()
        self.make_door()

        if self.render_stairs:
            self.make_stairs()

        if self.render_magnets:
            self.make_magnets()

        if self.render_floor_tile and self.bp_tile_gen:
            self.bp_tile_gen.diameter = self.diameter - self.wall_width*4
            self.bp_tile_gen.tile_height = self.tile_height
            self.bp_tile_gen.make()

    def make_base(self):
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
        
        if self.render_blocks:
            self.make_blocks()
            
    def make_core_block(self,margin, top_height=None):
        if not top_height:
            #log('default top height')
            top_height = self.block_height
            
        #log(f'make_core_block top_height {top_height}')
            
        return cq.Workplane("XY").box(
            self.block_length,
            self.block_width-margin,
            top_height
        )
    
    def make_block_ring(self, diameter, add_block):
        blocks = (
            cq.Workplane("XY")
            .polarArray(
                radius = diameter / 2, 
                startAngle = 0, 
                angle = 360, 
                count = self.block_ring_count,
                fill = True,
                rotate = True
            )
            .eachpoint(callback = add_block)
        )
        
        ring = cq.Workplane("XY").union(blocks)
        
        return ring
            
    def make_blocks(self):
        block_defs = []
        
        block_defs.append(self.make_core_block(0))
        block_defs.append(self.make_core_block(0.5))
        block_defs.append(self.make_core_block(1))
        block_defs.append(self.make_core_block(1.5))
        
        def add_block(loc:cq.Location):
            return block_defs[0].val().located(loc)
        
        def add_block_2(loc:cq.Location):
            return block_defs[1].val().located(loc)
        
        def add_block_3(loc:cq.Location):
            return block_defs[2].val().located(loc)
        
        def add_block_4(loc:cq.Location):
            return block_defs[3].val().located(loc)
        
        ring_params = [
            (self.base_diameter-5, add_block),#1
            (self.base_diameter-7, add_block),#2
            (self.base_diameter-9, add_block),#3
            (self.base_diameter-11.5, add_block_2),#4
            (self.base_diameter-13.5, add_block_2),#5
            (self.base_diameter-16, add_block_3),#6
            (self.base_diameter-18, add_block_3),#7
            (self.base_diameter-20, add_block_4),#8
            (self.base_diameter-22, add_block_4),#9
        ]
        
        blocks_combined = (
            cq.Workplane()
        )
        
        for i in range(len(ring_params)):
            rotate_deg = 0
            
            if i % 2 == 1:
                rotate_deg = self.even_ring_rotate
                
            blocks_combined = (
                blocks_combined
                .union(
                    self.make_block_ring(
                        ring_params[i][0], 
                        ring_params[i][1]
                    )
                    .translate((0,0,(self.block_height/2)+1+(self.block_height+1)*i))
                    .rotate((0,0,1),(0,0,0),rotate_deg)
                )
            )
            
        # inner
        block_inner = self.make_core_block(3)
        
        def add_block_inner(loc:cq.Location)->cq.Shape:
            return block_inner.val().located(loc)#type:ignore
        
        ring_param_inner = (self.diameter-(self.wall_width*4)+2.5, add_block_inner)
        
        block_height = self.block_height + 1
        count = math.floor(self.height / block_height)
        
        blocks_combined_inner = (
            cq.Workplane()
        )
        
        for i in range(count):
            rotate_deg = 0
            
            if i % 2 == 1:
                rotate_deg = self.even_ring_rotate
                
            blocks_combined_inner = (
                blocks_combined_inner
                .union(
                    self.make_block_ring(
                        ring_param_inner[0], 
                        ring_param_inner[1]
                    )
                    .translate((0,0,(self.block_height/2)+1+(self.block_height+1)*i))
                    .rotate((0,0,1),(0,0,0),rotate_deg)
                )
            )
        if self.base:    
            self.base = (
                self.base
                .union(blocks_combined)
                .union(blocks_combined_inner)
            )
        
    def calculate_inner_height(self):
        return self.height - self.floor_height
    
    def make_stairs(self):
        diameter = self.diameter - self.wall_width*4
        inner_diameter = diameter - 60
        height = self.calculate_inner_height()
        
        ramp = make_ramp(
            stair_count = 12,
            height = height,
            inner_diameter = inner_diameter,
            diameter = diameter,
            distance_overlap = 0.5,
            debug = False
        ).translate((0,0,height/2+self.floor_height))
        
        stairs = make_greebled_stairs(
            stair_count = 12,
            height = height,
            inner_diameter = inner_diameter,
            diameter = diameter, 
            debug=False
        ).translate((0,0,height/2+self.floor_height))
        
        self.stairs = stairs.cut(ramp.rotate((0,0,1),(0,0,0),-8))
        
    def build_cut_windows(self):
        window_cut = (
            self.bp_window.build_cut()
            .translate((0,0,self.height/2))
        ).rotate((0,0,1),(0,0,0),-90)
        
        window_cuts = cq.Workplane("XY")
        window_degrees = 360 / self.window_count
        for i in range(self.window_count):
            #log(f' add window {i=}')
            window_cuts = (
                window_cuts
                .union(window_cut.rotate((0,0,1),(0,0,0),window_degrees*i))
            )
        #windows = cq.Workplane("XY")
        #return window_cut
        return window_cuts
    
    def build_cut_door(self):
        door_cut = (
            self.bp_door.build_cut()
            .translate((0,0,self.bp_door.height/2+self.floor_height))
        ).rotate((0,0,1),(0,0,0),-180)
        
        door_cuts = cq.Workplane("XY")
        door_degrees = 360 / self.door_count
        for i in range(self.door_count):
            #log(f' add door {i=}')
            door_cuts = (
                door_cuts
                .union(door_cut.rotate((0,0,1),(0,0,0),door_degrees*i))
            )
        return door_cuts
        
    def build(self):
        super().build()
        
        cut_windows = self.build_cut_windows()
        cut_doors = self.build_cut_door()  
        
        scene = cq.Workplane("XY")

        if self.base:
            scene = scene.add(self.base)

        if self.stairs:
            scene = scene.add(self.stairs)

        if cut_windows:
            scene = scene.cut(cut_windows)

        if cut_doors:
            scene = scene.cut(cut_doors)

        if self.magnets:
            scene = scene.cut(self.magnets.translate((0,0,self.height)))

        if self.render_floor_tile and self.bp_tile_gen:
            tiles = self.bp_tile_gen.build()
            offset_height = self.floor_height
            scene = scene.union(tiles.translate((0,0,offset_height-self.tile_height/2)))

        return scene