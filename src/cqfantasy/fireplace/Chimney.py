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

class Chimney(Base):
    def __init__(self):
        super().__init__()
        #parameters
        self.length:float = 6
        self.width:float = 6
        self.height:float = 60
        self.interior_padding:float = 2
        
        #shapes
        self.outline:cq.Workplane|None = None
        self.chimney:cq.Workplane|None = None
        
    def make_outline(self):
        outline = cq.Workplane("XY").box(
            self.length,
            self.width,
            self.height
        )
        
        self.outline = outline
        
    def make_chimney(self):
        chimney = cq.Workplane("XY").box(
            self.length,
            self.width,
            self.height
        )
        
        interior = cq.Workplane("XY").box(
            self.length - self.interior_padding*2,
            self.width - self.interior_padding*2,
            self.height
        ) 
        
        self.chimney = chimney.cut(interior)
        
    def make(self):
        super().make()
        self.make_outline()
        self.make_chimney()
        
    def build_outline(self)->cq.Workplane:
        super().build()
        
        part = cq.Workplane("XY")
        
        if self.outline:
            part = part.add(self.outline.translate((0,0,self.height/2)))
        
        return part
        
    def build(self)->cq.Workplane:
        super().build()
        
        part = cq.Workplane("XY")
        
        if self.chimney:
            part = part.add(self.chimney.translate((0,0,self.height/2)))
        
        return part