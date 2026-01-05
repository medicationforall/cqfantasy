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
from cadqueryhelper.shape import trapezoid

class FireBoxTiled(Base):
    def __init__(self):
        super().__init__()
        #parameters
        self.length:float = 35
        self.width:float = 25
        self.height:float = 30
        self.x_padding:float = 5
        self.y_padding:float = 5
        self.interior_width:float = 10
        
        self.rows:int = 4
        self.columns:int = 3
        self.layers:int = 5
        self.spacing:float = .7
        self.spacing_z:float = 0
        self.tile_padding:float = 2

        #shapes
        self.outline:cq.Workplane|None = None
        self.firebox:cq.Workplane|None = None
        self.internal_firebox:cq.Workplane|None = None
        self.tiles:cq.Workplane|None = None
                
    def make_outline(self):
        outline = cq.Workplane("XY").box(
            self.length,
            self.width,
            self.height
        )
        
        self.outline = outline.translate((0,0,self.height/2))
        
    def make_firebox(self):
        box = cq.Workplane("XY").box(
            self.length,
            self.width,
            self.height
        )
        
        interior_length = self.length - self.x_padding*2
        interior_width = self.width - self.y_padding
        interior = trapezoid(
            length = self.height,
            width = interior_length,
            height = interior_width,
            top_width = self.interior_width
        ).rotate((1,0,0),(0,0,0),90).translate((0,-self.y_padding/2,0))
        
        self.firebox = box.cut(interior)
        
    def make_internal_firebox(self):
        box = cq.Workplane("XY").box(
            self.length-self.spacing,
            self.width-self.spacing,
            self.height - self.spacing_z
        )
        
        interior_length = self.length - self.x_padding*2
        interior_width = self.width - self.y_padding
        interior = trapezoid(
            length = self.height+self.spacing,
            width = interior_length+self.spacing,
            height = interior_width,
            top_width = self.interior_width+self.spacing
        ).rotate((1,0,0),(0,0,0),90).translate((0,-self.y_padding/2,0))
        
        self.internal_firebox = box.cut(interior)
        
        
    def make_tiles(self):
        
        x_spacing = (self.length+self.tile_padding)/self.columns
        y_spacing = (self.width+self.tile_padding)/self.rows
        z_spacing = (self.height+self.tile_padding)/self.layers
        length = x_spacing - self.spacing
        width = y_spacing - self.spacing
        height = z_spacing - self.spacing
        tile = cq.Workplane("XY").box(length, width, height)
        
        def add_tile(loc:cq.Location) ->cq.Shape:
            return tile.val().located(loc) #type:ignore
        
        tiles = (
            cq.Workplane("XY")
            .rarray(
                xSpacing = x_spacing, 
                ySpacing = y_spacing,
                xCount = self.columns+1, 
                yCount= self.rows+1, 
                center = True)
            .eachpoint(add_tile)
        )
        
        tile_layers = cq.Workplane("XY")
        
        for i in range(self.layers):
            x_translate = x_spacing/2 * (i%2==0)
            y_translate = y_spacing/2 * (i%2==0)
            tile_layers = tile_layers.union(tiles.translate((
                x_translate,
                y_translate,
                z_spacing*i
            )))
        
        tile_layers = tile_layers.translate((0,0,height/2))#-(self.height+self.tile_padding)))
        
        if self.firebox:
            #log('found outline')
            #self.tiles = self.outline.intersect(tile_layers)#.intersect()
            self.tiles = tile_layers.intersect(self.firebox.translate((0,0,self.height/2)))

    def make(self):
        super().make()
        self.make_outline()
        self.make_firebox()
        self.make_internal_firebox()
        self.make_tiles()
        
    def build_outline(self)->cq.Workplane:
        super().build()
        
        part = cq.Workplane("XY")
        
        if self.outline:
            part = part.add(self.outline)
        
        return part
        
    def build(self)->cq.Workplane:
        super().build()
        
        part = cq.Workplane("XY")
        
        if self.internal_firebox:
            part = part.union(self.internal_firebox.translate((0,0,self.height/2)))
            
        if self.tiles:
            part = part.union(self.tiles)
        
        return part