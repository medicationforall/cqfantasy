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
from . import Roof
from cqterrain.roof import angle, tiles_alt

class ShingleRoof(Roof):
    def __init__(self):
        super().__init__()
        
        #properties
        self.render_shingles:bool = True
        self.tile_length:float = 10
        self.tile_width:float = 10
        self.tile_height:float = 0.8
        self.tile_rotation:float = 4
        self.tile_push:float = 2
        
        #shapes
        self.shingle = None
        self.shingles = None
        
    def make_shingle(self):

        tile = (
            cq.Workplane("XY")
            .box(self.tile_length,self.tile_width,self.tile_height)
            .rotate((0,1,0),(0,0,0),self.tile_rotation)
        )
        
        self.shingle = tile
        
        
    def make_shingles(self):
        if self.shingle and self.roof:
            length = self.length/2
            width = self.width
            height = self.height
            
            #hyp = math.hypot(x, height)
            
            face_x = self.roof.faces(">X")
            angle_x = angle(length, height)

            self.shingles = tiles_alt(
                self.shingle, 
                face_x, 
                length,
                width,
                height, 
                self.tile_length, 
                self.tile_width, 
                angle_x,  
                odd_col_push=[self.tile_push,0],
                debug = False,
                intersect = True
            )
        
    def make(self, parent=None):
        super().make(parent)
        
        if self.render_shingles:
            self.make_shingle()
            self.make_shingles()
        
    def build(self)->cq.Workplane:
        roof = super().build()
        
        scene = cq.Workplane("XY")
        
        if roof:
            scene = scene.union(roof)
            
        if self.render_shingles and self.shingles:
            scene = (
                scene
                .union(self.shingles)
                .union(self.shingles.rotate((0,0,1),(0,0,0),180))
            )
            
        return scene