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

class WallTudorPaneling(Base):
    def __init__(self):
        super().__init__()
        #parameters
        self.length:float = 100
        self.width:float = 2
        self.height:float = 75
        
        self.render_outline:bool = False
        
        #h_frame
        self.h_frame_height:float = 4
        
        #v_frame
        self.v_frame_length:float = 2
        
        #panels
        self.rows:int = 5
        self.columns:int = 10
        self.row_height:float = 2
        self.column_width:float = 2
 
        #shapes
        self.outline:cq.Workplane|None = None
        self.h_frame:cq.Workplane|None = None
        self.v_frame:cq.Workplane|None = None
        self.tile:cq.Workplane|None = None
        self.tiles:cq.Workplane|None = None
        
        
    def calculate_internal_length(self):
        internal_length = self.length - (self.v_frame_length*2)
        return internal_length + self.column_width
    
    def calculate_internal_height(self):
        internal_height = self.height - (self.h_frame_height*2)
        return internal_height + self.row_height
            
    def calculate_tile_length(self):
        internal_length = self.calculate_internal_length()
        length = internal_length / self.columns 
        return length
    
    def calculate_tile_height(self):
        internal_height = self.calculate_internal_height()
        height = internal_height / self.rows
        return height
        
    def make_outline(self):
        outline = cq.Workplane("XY").box(
            self.length, 
            self.width, 
            self.height
        )
        
        self.outline  = outline
        
    def make_h_frame(self):
        if self.h_frame_height and self.h_frame_height > 0:
            frame = cq.Workplane("XY").box(
                self.length,
                self.width,
                self.h_frame_height
            )
            
            self.h_frame = frame
        
    def make_v_frame(self):
        if self.v_frame_length and self.v_frame_length > 0:
            frame = cq.Workplane("XY").box(
                self.v_frame_length,
                self.width,
                self.height
            )
            
            self.v_frame = frame
            
    def make_tile(self):
        length = self.calculate_tile_length() - self.column_width
        height = self.calculate_tile_height() - self.row_height
        
        #log(f'tile length = {length} tile height = {height}')
        tile = cq.Workplane("XY").box(length,self.width,height)
        self.tile = tile.rotate((1,0,0),(0,0,0),90)
        
    def make_tiles(self):
        def add_tile(loc:cq.Location)->cq.Shape:
            return self.tile.val().located(loc) #type:ignore
        
        tile_length = self.calculate_tile_length()
        tile_height = self.calculate_tile_height()
        # I always forget the definition for rarray
        tiles = (
            cq.Workplane("XY")
            .rarray(
                xSpacing = tile_length, 
                ySpacing = tile_height,
                xCount = self.columns, 
                yCount= self.rows, 
                center = True)
            .eachpoint(callback = add_tile)
        ).rotate((1,0,0),(0,0,0),90)
        
        self.tiles = tiles
        
    def make(self, parent=None):
        super().make(parent)
        
        #will be used for potential cut operations
        self.make_outline()
        self.make_h_frame()
        self.make_v_frame()
        self.make_tile()
        self.make_tiles()
        
    def build(self):
        super().build()
        scene = cq.Workplane("XY")
        
        internal_length = self.calculate_internal_length()
        internal_height = self.calculate_internal_height()
        #log(f'{internal_length=} {internal_height=}')
        
        if self.render_outline and self.outline:
            scene = scene.add(self.outline.translate((0,.5,0)))
            
        if self.h_frame:
            scene = (
                scene
                .union(self.h_frame.translate((
                    0,
                    0,
                    self.height/2-self.h_frame_height/2
                )))
                .union(self.h_frame.translate((
                    0,
                    0,
                    -self.height/2+self.h_frame_height/2
                )))
            )
            
        if self.v_frame:
            scene = (
                scene
                .union(self.v_frame.translate((
                    self.length/2-self.v_frame_length/2,
                    0,
                    0
                )))
                .union(self.v_frame.translate((
                    -self.length/2+self.v_frame_length/2,
                    0,
                    0
                )))
            )
            
        if self.tiles and self.outline:
            internal_frame = self.outline.cut(self.tiles)
            scene = scene.union(internal_frame)
  
        return scene
    
    def build_cut(self):
        return self.outline