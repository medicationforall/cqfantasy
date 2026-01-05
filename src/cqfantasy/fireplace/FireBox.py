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

class FireBox(Base):
    def __init__(self):
        super().__init__()
        #parameters
        self.length:float = 35
        self.width:float = 25
        self.height:float = 30
        self.x_padding:float = 5
        self.y_padding:float = 5
        self.interior_width:float = 10

        #shapes
        self.outline:cq.Workplane|None = None
        self.firebox:cq.Workplane|None = None
                
    def make_outline(self):
        outline = cq.Workplane("XY").box(
            self.length,
            self.width,
            self.height
        )
        
        self.outline = outline
        
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
        

    def make(self):
        super().make()
        self.make_outline()
        self.make_firebox()
        
    def build_outline(self)->cq.Workplane:
        super().build()
        
        part = cq.Workplane("XY")
        
        if self.outline:
            part.add(self.outline.translate((0,0,self.height/2)))
        
        return part
        
    def build(self)->cq.Workplane:
        super().build()
        
        part = cq.Workplane("XY")
        
        if self.firebox:
            #part.add(self.firebox)
            part.add(self.firebox.translate((0,0,self.height/2)))
        
        return part