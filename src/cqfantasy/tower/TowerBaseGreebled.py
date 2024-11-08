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
from cqterrain.material import uneven_centered_blocks
from . import cut_cylinder, TowerBase, UnevenBlocks

class TowerBaseGreebled(UnevenBlocks,TowerBase):
    def __init__(self):
        super().__init__()

        self.init_uneven_blocks()
        self.render_base = True
        
    def make_core_block(self,margin, top_height=None, outside=True):
        uneven_core_blocks = self.make_uneven_core_block(
            margin,
            self.block_height, 
            self.block_length, 
            self.block_width,
            top_height,
            outside
        )
        
        return uneven_core_blocks
        
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
            (self.base_diameter-8.5, add_block),#3
            (self.base_diameter-10.5, add_block_2),#4
            (self.base_diameter-12.5, add_block_2),#5
            (self.base_diameter-15, add_block_3),#6
            (self.base_diameter-17, add_block_3),#7
            (self.base_diameter-19, add_block_4),#8
            (self.base_diameter-21, add_block_4),#9
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
                .add(
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
        return self.make_uneven_inside_blocks(
            self.diameter,
            self.height,
            self.wall_width,
            self.block_height,
            self.block_length,
            self.block_width,
            self.even_ring_rotate,
            self.make_block_ring
        )
          
    def make_blocks(self):
        if self.render_outside_blocks and self.render_inside_blocks:
            blocks_combined_outside = self.make_outside_blocks()
            blocks_combined_inside = self.make_inside_blocks()

            base_out = (
                self.base
                .add(blocks_combined_outside)
            )

            base_in = self.base_in = (
                self.base
                .add(blocks_combined_inside)
            )

            self.base = base_out.union(base_in)
        elif self.render_outside_blocks:
            blocks_combined = self.make_outside_blocks()
            self.base = self.base.union(blocks_combined)

        elif self.render_inside_blocks:
            blocks_combined = self.make_inside_blocks()
            self.base = self.base.union(blocks_combined)

        else:
            raise Exception('unable to create blocks')
            
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
        
    def make(self, parent=None):
        self.make_uneven_blocks(self.block_height, self.block_width, self.block_length)
        super().make(parent)