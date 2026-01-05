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

class Hearth(Base):
    def __init__(self):
        super().__init__()
        #parameters
        self.length:float = 35
        self.width:float = 35
        self.height:float = 3

        #shapes
        self.outline:cq.Workplane|None = None
        self.hearth:cq.Workplane|None = None
        
    def make_outline(self):
        outline = cq.Workplane("XY").box(
            self.length,
            self.width,
            self.height
        )
        
        self.outline = outline
        
    def make_hearth(self):
        hearth = cq.Workplane("XY").box(
            self.length,
            self.width,
            self.height
        )
        
        self.hearth = hearth
        
    def make(self):
        super().make()
        self.make_outline()
        self.make_hearth()
        
    def build_outline(self)->cq.Workplane:
        super().build()
        
        part = cq.Workplane("XY")
        
        if self.outline:
            part.add(self.outline.translate((0,0,self.height/2)))
        
        return part
        
    def build(self)->cq.Workplane:
        super().build()
        
        part = cq.Workplane("XY")
        
        if self.hearth:
            part.add(self.hearth.translate((0,0,self.height/2)))
        
        return part