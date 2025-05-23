# Copyright 2025 James Adams
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
from cqterrain.material import stacked_wave_form_map, stucco_brick_blocks
import math

class WallStuccoBrick(Base):
    def __init__(self):
        super().__init__()
        
        #parameters
        self.length:float = 100
        self.width:float = 5
        self.height:float = 50
        self.seed:str = 'test'
        self.cell_types:list[str] = [
            'block',
            'block', 
            'empty',
            'block'
        ]

        self.center:bool = True
        self.spread_width:bool = True
        
        self.block_length:float = 8
        
        self.block_height:float = 3
        self.block_spacing:float = 2

        self.outline_intersect:bool = True
        
        #shapes
        self.outline:cq.Workplane|None = None
        self.wall=None
        
    def make_wall(self):
        x_count = math.floor((self.length) / (self.block_length+self.block_spacing) )
        y_count = math.floor(self.height / (self.block_height + self.block_spacing))
        
        brick_map = stacked_wave_form_map(
            (y_count, x_count),
            self.seed, 
            self.cell_types
        )
        
        block_length = self.block_length
        if self.spread_width:
            block_length = self.block_length+self.width/x_count
        self.wall = stucco_brick_blocks(
            brick_map, 
            block_length,
            self.block_height,
            self.width,
            self.block_spacing
        )

    def make_outline(self):
        outline = cq.Workplane("XY").box(
            self.length + self.width*2, 
            self.width, 
            self.height
        )
        
        self.outline  = outline
        
    def make(self, parent=None):
        super().make(parent)
        self.make_outline()
        self.make_wall()
        
    def build(self)->cq.Workplane:
        super().build()
        
        scene = cq.Workplane("XY")
        
        if self.wall:
            scene = scene.add(self.wall.rotate((1,0,0),(0,0,0),-90))

        if self.center:
            scene = scene.translate((-self.width/2,0,0))

        if self.outline_intersect and self.outline:
            scene = scene.intersect(self.outline)
            
        return scene
    
    def build_cut(self):
        return self.outline