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
from ..house_wall import tudor_wall
from . import Body

class TudorBody(Body):
    def  __init__(self):
        super().__init__()
        self.split_width:float = 3
        self.split_height:float = 3
        
        self.corner_length:float = 3
        self.corner_width:float = 3
        
        self.split_divide_height:float = 15
        self.panel_length:float = 25
        self.panel_width:float = 2.5
        self.panel_space:float = 2
        
        self.x_styles:list[str|None]|str|None = ["cross",None,None,"cross"]
        self.y_styles:list[str|None]|str|None = ["cross",None,None,"cross"]
        
        #shapes
        self.split_x:cq.Workplane|None = None
        self.split_y:cq.Workplane|None = None
        self.corner:cq.Workplane|None = None
        self.tudor_wall_x:cq.Workplane|None = None
        self.tudor_wall_y:cq.Workplane|None = None
        
    def make_split(self):
        split_x = cq.cq.Workplane("XY").box(self.length,self.split_width,self.split_height)
        self.split_x = split_x
        
        split_y = cq.cq.Workplane("XY").box(self.split_width,self.width,self.split_height)
        self.split_y = split_y
        
    def make_corner(self):
        corner = cq.Workplane("XY").box(self.corner_length,self.corner_width,self.height)
        
        self.corner = corner
        
    def calculate_panel_height(self):
        return self.height - self.split_height*2 - self.split_divide_height*2

    def make_tudor_walls(self):
        height = self.calculate_panel_height() 
        self.tudor_wall_y = tudor_wall(
            self.width,
            height, 
            self.y_styles, 
            self.panel_length, 
            self.panel_space, 
            self.panel_width
        )

        self.tudor_wall_x = tudor_wall(
            self.length,
            height, 
            self.x_styles, 
            self.panel_length, 
            self.panel_space, 
            self.panel_width
        )

    def make(self, parent=None):
        self.make_split()
        self.make_corner()
        self.make_tudor_walls()
        super().make(parent)
        
    def build(self):
        scene = cq.Workplane("XY")
        body = super().build()
        
        if body:
            scene = scene.union(body)
            
        split_translate_z_bottom = -self.height/2+self.split_height/2+self.split_divide_height
        split_translate_z_top = self.height/2-self.split_height/2-self.split_divide_height
    
        if self.split_x:
            scene = (
                scene
                .union(self.split_x.translate((0,-self.width/2-self.split_width/2,split_translate_z_bottom)))
                .union(self.split_x.translate((0,self.width/2+self.split_width/2,split_translate_z_bottom)))
                .union(self.split_x.translate((0,-self.width/2-self.split_width/2,split_translate_z_top)))
                .union(self.split_x.translate((0,self.width/2+self.split_width/2,split_translate_z_top)))

            )
            
        if self.split_y:
            scene = (
                scene
                .union(self.split_y.translate((-self.length/2-self.split_width/2,0,split_translate_z_bottom)))
                .union(self.split_y.translate((self.length/2+self.split_width/2,0,split_translate_z_bottom)))
                .union(self.split_y.translate((-self.length/2-self.split_width/2,0,split_translate_z_top)))
                .union(self.split_y.translate((self.length/2+self.split_width/2,0,split_translate_z_top)))
            )
            
        if self.corner:
            scene = (
                scene
                .union(self.corner.translate((-self.length/2-self.corner_length/2,self.width/2+self.corner_width/2,0)))
                .union(self.corner.translate((self.length/2+self.corner_length/2,self.width/2+self.corner_width/2,0)))
                .union(self.corner.translate((self.length/2+self.corner_length/2,-self.width/2-self.corner_width/2,0)))
                .union(self.corner.translate((-self.length/2-self.corner_length/2,-self.width/2-self.corner_width/2,0)))
            )
            
        if self.tudor_wall_x:
            translate_y = self.width/2+self.panel_width/2
            scene = (
                scene
                .add(self.tudor_wall_x.translate((0,translate_y,0)))
                .add(self.tudor_wall_x.rotate((0,0,1),(0,0,0),180).translate((0,-translate_y,0)))
            )
            
        if self.tudor_wall_y:
            translate_x = self.length/2+self.panel_width/2
            scene = (
                scene
                .add(self.tudor_wall_y
                     .rotate((0,0,1),(0,0,0),-90)
                     .translate((-translate_x,0,0))
                )
                .add(self.tudor_wall_y
                     .rotate((0,0,1),(0,0,0),90)
                     .translate((translate_x,0,0))
                )
            )
            
        return scene