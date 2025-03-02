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
import math
from cqterrain.material import stacked_wave_form_map, stucco_brick_blocks
from . import Body

class TudorSplitBody(Body):
    def __init__(self):
        super().__init__()
        
        #parameters 
        self.split_width = 3
        self.split_height = 3
        
        self.corner_length = 3
        self.corner_width = 3
        
        self.split_divide_height = 25
        self.render_stones = True
        
        self.seed = 'test'
        self.cell_types = [
            'block',
            'block', 
            'empty',
            'block'
        ]
        self.y_count = 9
        self.x_count = 15
        self.block_length = 8
        self.block_width = 5
        self.block_height = 5
        self.block_spacing = 2
        
        # blueprints
        self.stones_generator = None
        
        #shapes
        self.split_x = None
        self.split_y = None
        self.corner = None
        self.stones_x_plus = None
        self.stones_x_minus = None
        self.stones_y_plus = None
        self.stones_y_minus = None
        
    def make_split(self):
        split_x = cq.cq.Workplane("XY").box(self.length,self.split_width,self.split_height)
        self.split_x = split_x
        
        split_y = cq.cq.Workplane("XY").box(self.split_width,self.width,self.split_height)
        self.split_y = split_y
        
    def make_corner(self):
        corner = cq.Workplane("XY").box(self.corner_length,self.corner_width,self.height)
        
        self.corner = corner


    def make_stones(self):
        #log('making stones')
        
        stones_length_x_count = math.floor(self.length / (self.block_length+self.block_spacing) )
        stones_width_x_count = math.floor(self.width / (self.block_length+self.block_spacing) )
        stones_y_count = math.floor(self.split_divide_height / (self.block_height + self.block_spacing))
        
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
        self.make_split()
        self.make_corner()
        
        if self.render_stones:
            self.make_stones()
        
    def build(self):
        body = super().build()
        scene = (
            cq.Workplane("XY")
        )
        
        if self.body:
            scene = scene.add(body)
            
        split_translate_z = -self.height/2+self.split_height/2+self.split_divide_height
        
        if self.split_x:
            scene = (
                scene
                .union(self.split_x.translate((0,-self.width/2-self.split_width/2,split_translate_z)))
                .union(self.split_x.translate((0,self.width/2+self.split_width/2,split_translate_z)))
            )
            
        if self.split_y:
            scene = (
                scene
                .union(self.split_y.translate((-self.length/2-self.split_width/2,0,split_translate_z)))
                .union(self.split_y.translate((self.length/2+self.split_width/2,0,split_translate_z)))
            )
            
        if self.corner:
            scene = (
                scene
                .union(self.corner.translate((-self.length/2-self.corner_length/2,self.width/2+self.corner_width/2,0)))
                .union(self.corner.translate((self.length/2+self.corner_length/2,self.width/2+self.corner_width/2,0)))
                .union(self.corner.translate((self.length/2+self.corner_length/2,-self.width/2-self.corner_width/2,0)))
                .union(self.corner.translate((-self.length/2-self.corner_length/2,-self.width/2-self.corner_width/2,0)))
            )

        if self.render_stones and self.stones_x_plus and self.stones_x_minus and self.stones_y_plus and self.stones_y_minus:
            scene = (
                scene
                .union(self.stones_x_plus
                    .rotate((1,0,0),(0,0,0),-90)
                    .translate((-self.block_width/2,-self.width/2,-self.height/2+self.split_divide_height/2))
                )
                .union(
                    self.stones_x_minus
                    .rotate((1,0,0),(0,0,0),-90)
                    .rotate((0,0,1),(0,0,0),180)
                    .translate((self.block_width/2,self.width/2,-self.height/2+self.split_divide_height/2))
                )
                .union(
                    self.stones_y_plus
                    .rotate((1,0,0),(0,0,0),-90)
                    .rotate((0,0,1),(0,0,0),-90)
                    .translate((self.length/2,-self.block_width/2,-self.height/2+self.split_divide_height/2))
                )
                .union(
                    self.stones_y_minus
                    .rotate((1,0,0),(0,0,0),-90)
                    .rotate((0,0,1),(0,0,0), 90)
                    .translate((-self.length/2,self.block_width/2,-self.height/2+self.split_divide_height/2))
                )
            )

        return scene