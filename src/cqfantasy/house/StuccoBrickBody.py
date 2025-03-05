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
from cqterrain.material import stacked_wave_form_map, stucco_brick_blocks
from . import Body
import math

class StuccoBrickBody(Body):
    def __init__(self):
        super().__init__()
        
        #parameters 
        
        self.render_stones:bool = True
        
        self.seed:str = 'test'
        self.cell_types:list[str] = [
            'block',
            'block', 
            'empty',
            'block'
        ]

        self.block_length:float = 8
        self.block_width:float = 5
        self.block_height:float = 3
        self.block_spacing:float = 2
        
        #shapes
        self.split_x:cq.Workplane|None = None
        self.split_y:cq.Workplane|None = None
        self.corner:cq.Workplane|None = None
        self.stones_x_plus:cq.Workplane|None = None
        self.stones_x_minus:cq.Workplane|None = None
        self.stones_y_plus:cq.Workplane|None = None
        self.stones_y_minus:cq.Workplane|None = None

    def make_stones(self):
        #log('making stones')
        
        stones_length_x_count = math.floor(self.length / (self.block_length+self.block_spacing) )
        stones_width_x_count = math.floor(self.width / (self.block_length+self.block_spacing) )
        stones_y_count = math.floor(self.height / (self.block_height + self.block_spacing))
        
        #log(f'{stones_length_x_count=} {self.length=} ')
        map_x_plus = stacked_wave_form_map(
            (stones_y_count, stones_length_x_count),
            self.seed+'_01', 
            self.cell_types
        )
        
        map_x_minus = stacked_wave_form_map(
            (stones_y_count, stones_length_x_count),
            self.seed+'_02', 
            self.cell_types
        )
        
        map_y_plus = stacked_wave_form_map(
            (stones_y_count, stones_width_x_count),
            self.seed+'_03', 
            self.cell_types
        )
        
        map_y_minus = stacked_wave_form_map(
            (stones_y_count, stones_width_x_count),
            self.seed+'_04', 
            self.cell_types
        )
        
        self.stones_x_plus = stucco_brick_blocks(
            map_x_plus, 
            self.block_length,
            self.block_height,
            self.block_width,
            self.block_spacing
        )
        
        self.stones_x_minus = stucco_brick_blocks(
            map_x_minus, 
            self.block_length,
            self.block_height,
            self.block_width,
            self.block_spacing
        )
        
        self.stones_y_plus = stucco_brick_blocks(
            map_y_plus, 
            self.block_length,
            self.block_height,
            self.block_width,
            self.block_spacing
        )
        
        self.stones_y_minus = stucco_brick_blocks(
            map_y_minus, 
            self.block_length,
            self.block_height,
            self.block_width,
            self.block_spacing
        )
        
    def make(self):
        super().make()
        
        if self.render_stones:
            self.make_stones()
            
    def build(self):
        body = super().build()
        scene = (
            cq.Workplane("XY")
        )
        
        if self.body:
            scene = scene.add(body)
            
        if self.render_stones and self.stones_x_plus and self.stones_x_minus and self.stones_y_plus and self.stones_y_minus:
            scene = (
                scene
                .union(self.stones_x_plus
                     .rotate((1,0,0),(0,0,0),-90)
                     .translate((-self.block_width/2,-self.width/2,0))
                )
                .union(
                    self.stones_x_minus
                    .rotate((1,0,0),(0,0,0),-90)
                    .rotate((0,0,1),(0,0,0),180)
                    .translate((self.block_width/2,self.width/2,0))
                )
                .union(
                    self.stones_y_plus
                    .rotate((1,0,0),(0,0,0),-90)
                    .rotate((0,0,1),(0,0,0),-90)
                    .translate((self.length/2,-self.block_width/2,0))
                )
                .union(
                    self.stones_y_minus
                    .rotate((1,0,0),(0,0,0),-90)
                    .rotate((0,0,1),(0,0,0), 90)
                    .translate((-self.length/2,self.block_width/2,0))
                )
            )

        return scene