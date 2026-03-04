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
from cqfantasy.house import Roof
from cqterrain.roof import angle, tiles_alt
from cqterrain.damage import uneven_plane, uneven_spline_plane
import math

class SnowyRoof(Roof):
    def __init__(self):
        super().__init__()
        
        #properties
        self.render_shingles:bool = True
        self.tile_length:float = 10
        self.tile_width:float = 10
        self.tile_height:float = 0.8
        self.tile_rotation:float = 4
        self.tile_push:float = 2
        self.seed_one:str = 'test'
        self.seed_two:str = 'test_four'
        self.snow_height:float = 7
        self.snow_peak_count:int = 5
        self.snow_segments:int = 3
        self.snow_z_translate:float = 0
        
        
        #shapes
        self.shingle = None
        self.shingles = None
        self.snow = None
        
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
        
    def make_snow(self):
        length = self.length/2
        height = self.height
        hyp = math.hypot(length, height)
        angle_x = angle(length, height)
        
        u_plane_safe = uneven_spline_plane(
            length=hyp+4, 
            width=self.width,
            height=self.snow_height,
            #peak_count=(3,5), - risky
            peak_count=self.snow_peak_count,
            min_height=1,
            segments=self.snow_segments,
            seed=self.seed_one,
            render_plate=True,
            plate_height = 0.1
        ).rotate((0,0,1),(0,0,0),180).rotate((0,1,0),(0,0,0),angle_x).translate((-length/2-0,0,2))
        
        u_plane_safe_2 = uneven_spline_plane(
            length=hyp+4, 
            width=self.width,
            height=self.snow_height,
            #peak_count=(3,5), - risky
            peak_count=self.snow_peak_count,
            min_height=1,
        
            segments=self.snow_segments,
            seed=self.seed_two,
            render_plate=True,
            plate_height = 0.1
        ).rotate((0,1,0),(0,0,0),-angle_x).translate((length/2-0,0,2))
        
        combined = (
            cq.Workplane("XY")
            .union(u_plane_safe)
            .union(u_plane_safe_2,tol=0.1)
        )
        
        #show_object(combined)
        
        self.snow = combined
        
    def make(self, parent=None):
        super().make(parent)
        
        if self.render_shingles:
            self.make_shingle()
            self.make_shingles()
            
        self.make_snow()
        
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
            
        if self.snow:
            if self.snow_z_translate:
                scene = scene.union(self.snow.translate((0,0,self.snow_z_translate)))
            else:
                scene = scene.union(self.snow)
                

        flat = cq.Workplane("XY").box(self.length+10,self.width, self.height).translate((0,0,-self.height))
        
        scene = scene.cut(flat)
            
        return scene