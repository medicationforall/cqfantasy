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
from cqterrain.stairs.round import ramp as make_ramp, greebled_stairs as make_greebled_stairs, outline as make_outline
from . import LatticeWindow, TowerWindow, cut_cylinder, TileGenerator
from .magnets import make_magnet, make_magnets
import math

class TowerMid(Base):
    def __init__(self):
        super().__init__()
            
        # properties
        self.diameter:float = 130
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
        
        self.window_length:float = 20
        self.window_width:float = 12
        self.window_height:float = 40
        self.window_padding:float = 4
        self.window_count:int = 4

        self.render_magnets:bool = True
        self.magnet_diameter:float = 3.4
        self.magnet_height:float = 2.2
        self.magnet_count:int = 4

        self.render_floor_tile:bool = True
        self.tile_height:float = 2
        
        # blueprints
        self.bp_window:TowerWindow = LatticeWindow()
        self.bp_tile_gen:TileGenerator|None = TileGenerator()
        
        # shapes
        self.mid:cq.Workplane|None = None
        self.stairs:cq.Workplane|None = None
        self.floor_cut:cq.Workplane|None = None
        self.magnets:cq.Workplane|None = None
        
    def make_window(self):
        
        self.bp_window.diameter = self.diameter + self.window_padding
        #self.bp_window.wall_width = self.wall_width + self.window_padding
        self.bp_window.length = self.window_length
        self.bp_window.width = self.window_width
        
       # log(f'{self.bp_window.width}')
        self.bp_window.height = self.window_height
        self.bp_window.render_outline = self.render_window_outline
        self.bp_window.make()

    def make_magnets(self):
        magnet = make_magnet(self.magnet_diameter, self.magnet_height)
        self.magnets = (
            make_magnets(magnet, self.magnet_count, self.diameter - self.wall_width*2)
            .translate((0,0,-self.magnet_height/2))
        )
         
    def make(self, parent=None):
        super().make(parent)
        
        self.make_mid()
        self.make_window()

        if self.render_magnets:
            self.make_magnets()

        if self.render_floor_tile and self.bp_tile_gen:
            self.bp_tile_gen.diameter = self.diameter - self.wall_width*4
            self.bp_tile_gen.tile_height = self.tile_height
            self.bp_tile_gen.make()
        
    def make_mid(self):
        mid = cq.Workplane("XY").cylinder(self.height, self.diameter/2)

        if self.render_floor_tile:
            cut_cylinder_height = self.calculate_inner_height() + self.tile_height
        else:
            cut_cylinder_height = self.calculate_inner_height()
            
        mid = cut_cylinder(mid, self.diameter - (self.wall_width*4), cut_cylinder_height)
        self.mid = mid.translate((0,0,self.height/2))
        
        if self.render_blocks:
            self.make_blocks()
            
        if self.render_stairs:
            self.make_stairs()
            self.make_floor_cut()
            
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
        
        return blocks
    
    def make_blocks(self):
        block = self.make_core_block(1.5)
        block_inner = self.make_core_block(3)
        
        def add_block(loc:cq.Location) -> cq.Shape:
            return block.val().located(loc) #type:ignore
        
        def add_block_inner(loc:cq.Location) -> cq.Shape:
            return block_inner.val().located(loc) #type:ignore
        
        ring_param = (self.diameter-2.5, add_block)
        ring_param_inner = (self.diameter-(self.wall_width*4)+2.5, add_block_inner)
        
        block_height = self.block_height + 1
        count = math.floor(self.height / block_height)
        
        blocks_combined = (
            cq.Workplane()
        )
        
        for i in range(count):
            rotate_deg = 0
            
            if i % 2 == 0:
                rotate_deg = self.even_ring_rotate
                
            blocks_combined = (
                blocks_combined
                .union(
                    self.make_block_ring(
                        ring_param[0], 
                        ring_param[1]
                    )
                    .translate((0,0,(self.block_height/2)+1+(self.block_height+1)*i))
                    .rotate((0,0,1),(0,0,0),rotate_deg)
                )
            )
            
        blocks_combined_inner = (
            cq.Workplane()
        )
        
        for i in range(count):
            rotate_deg = 0
            
            if i % 2 == 0:
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

        if self.mid:    
            self.mid = (
                self.mid
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
        
        mid_stairs = stairs.cut(ramp.rotate((0,0,1),(0,0,0),-8))
        
        self.stairs = mid_stairs.rotate((0,0,1),(0,0,0),-90)
        
    def make_floor_cut(self):
        diameter = self.diameter - self.wall_width*4
        inner_diameter = diameter - 60
        
        outline = make_outline(
            height = self.floor_height,
            inner_diameter = inner_diameter,
            diameter = diameter,
            rotate = 50
        ).rotate((0,0,1),(0,0,0),7)
        
        self.floor_cut = outline
        
    def build_cut_windows(self):
        window_cut = (
            self.bp_window.build_cut()
            .translate((0,0,self.height/2))
        )
        
        window_cuts = cq.Workplane("XY")
        window_degrees = 360 / self.window_count
        for i in range(self.window_count):
            #log(f' add window {i=}')
            window_cuts = (
                window_cuts
                .union(window_cut.rotate((0,0,1),(0,0,0),window_degrees*i))
            )
        #windows = cq.Workplane("XY")
        
        if self.render_window_outline:
            return window_cut
    
        return window_cuts
    
    def build_windows(self):
        window = (
            self.bp_window.build()
            .translate((0,0,self.height/2))
        )
        
        windows = cq.Workplane("XY")
        window_degrees = 360 / self.window_count
        for i in range(self.window_count):
            #log(f' add window {i=}')
            windows = (
                windows
                .union(window.rotate((0,0,1),(0,0,0),window_degrees*i))
            )
        #windows = cq.Workplane("XY")
        
        #if self.render_window_outline:
        #    return window_cut
    
        return windows
        
    def build(self):
        super().build()
        
        cut_windows = self.build_cut_windows()
        windows = self.build_windows()
        
        scene = (
            cq.Workplane("XY")
            .union(self.mid)
            .union(self.stairs)
            .cut(cut_windows)
            .union(windows)
        )

        if self.magnets:
            scene = (
                scene
                .cut(self.magnets.translate((0,0,self.magnet_height)))
                .cut(self.magnets.translate((0,0,self.height)))                
            )

        if self.render_floor_tile and self.bp_tile_gen:
            tiles = self.bp_tile_gen.build()
            offset_height = self.floor_height
            scene = scene.union(tiles.translate((0,0,offset_height-self.tile_height/2)))
            
        if self.floor_cut:
            scene = scene.cut(self.floor_cut)
            
        return scene