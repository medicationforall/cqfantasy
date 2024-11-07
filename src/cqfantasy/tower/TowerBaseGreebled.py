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
import random
import math
from cqfantasy.tower import TowerBase
from cqterrain.material import uneven_centered_blocks
from . import cut_cylinder

class TowerBaseGreebled(TowerBase):
    def __init__(self):
        super().__init__()
        
        # parameters
        self.uneven_block_depth:float = 1.5
        self.seed:str = 'test4'
        self.render_base:bool = True
        self.render_outside_blocks:bool = False
        self.render_inside_blocks:bool = False
        
        
        # shapes
        self.uneven_blocks = None
        
    def make_uneven_blocks(self):
        blocks = uneven_centered_blocks(
            tile_length = self.block_height,
            tile_width = self.block_width,
            tile_height= self.block_length,
            rows = 6, 
            columns = 6, 
            margin = 2,
            uneven_depth = self.uneven_block_depth,
            seed=self.seed,
            segments = 10,
            peak_count = (14,15)
        )
        
        self.uneven_blocks = blocks
        
    def make_core_block(self,margin, top_height=None, outside=True):
        if not top_height:
            top_height = self.block_height
            
        
        core_block = cq.Workplane("XY").box(
            self.block_length,
            self.block_width-margin,
            top_height
        )
        
        uneven_core_blocks = []
        
        if self.uneven_blocks:
            for b in self.uneven_blocks:
                if outside:
                    b = b.rotate((0,1,0),(0,0,0),-90).intersect(core_block)
                else:
                    b = b.rotate((0,1,0),(0,0,0),90).intersect(core_block)
                uneven_core_blocks.append(b)
            
        return uneven_core_blocks
        #return uneven_core_blocks[0]
        
    def make_outside_blocks(self):
        block_defs = []
        
        block_defs.append(self.make_core_block(0))
        block_defs.append(self.make_core_block(0.5))
        block_defs.append(self.make_core_block(1))
        block_defs.append(self.make_core_block(1.5))
        
        def add_block(loc:cq.Location):
            chosen_block = random.choice(block_defs[0])
            return chosen_block.val().located(loc)
        
        def add_block_2(loc:cq.Location):
            chosen_block = random.choice(block_defs[1])
            return chosen_block.val().located(loc)
        
        def add_block_3(loc:cq.Location):
            chosen_block = random.choice(block_defs[2])
            return chosen_block.val().located(loc)
        
        def add_block_4(loc:cq.Location):
            chosen_block = random.choice(block_defs[3])
            return chosen_block.val().located(loc)
        
        ring_params = [
            (self.base_diameter-3.5, add_block),#1
            (self.base_diameter-6.5, add_block),#2
            #(self.base_diameter-8.5, add_block),#3
            #(self.base_diameter-10.5, add_block_2),#4
            #(self.base_diameter-12.5, add_block_2),#5
            #(self.base_diameter-15, add_block_3),#6
            #(self.base_diameter-17, add_block_3),#7
            #(self.base_diameter-19, add_block_4),#8
            #(self.base_diameter-21, add_block_4),#9
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
            
        return blocks_combined
        
        
    def make_inside_blocks(self):
        # inner
        block_inner = self.make_core_block(3, outside=False)
        
        def add_block_inner(loc:cq.Location):
            chosen_block = random.choice(block_inner)
            return chosen_block.val().located(loc)
        
        ring_param_inner = (self.diameter-(self.wall_width*4)+2.5, add_block_inner)
        
        block_height = self.block_height + 1
        count = math.floor(self.height / block_height)
        
        blocks_combined_inner = (
            cq.Workplane()
        )
        
        #for i in range(count):
        for i in range(1):
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
            
        return blocks_combined_inner
        
        
    def make_blocks(self):
        if self.render_outside_blocks:
            blocks_combined = self.make_outside_blocks()
    
            self.base = (
                self.base
                .union(blocks_combined)
            )

        if self.render_inside_blocks:
            blocks_combined_inner = self.make_inside_blocks()
        
            self.base = (
                self.base
                .union(blocks_combined_inner)
            )
            
        
    def make_base(self):
        if self.render_base:
            base = cq.Solid.makeCone(
                self.base_diameter/2, 
                self.diameter/2, 
                self.height
            )
            
            base = cq.Workplane("XY").add(base)
            base = cut_cylinder(base, self.diameter - self.wall_width*4, self.calculate_inner_height())
            self.base = base
        else:
            self.base = cq.Workplane("XY")
        
        if self.render_blocks:
            self.make_blocks()
            
        if self.render_stairs:
            self.make_stairs()
        
    def make(self, parent=None):
        self.make_uneven_blocks()
        super().make(parent)
        
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


        return scene