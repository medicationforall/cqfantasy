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

class BasicPillar(Base):
    def __init__(self):
        super().__init__()
        #parameters
        self.length:float = 30
        self.width:float = 30
        self.height:float = 45
        
        #shapes
        self.outline:cq.Workplane|None = None
        
    def make_outline(self):
        outline = cq.Workplane("XY").box(
            self.length,
            self.width,
            self.height
        )
        
        self.outline = outline
        
    def make(self):
        super().make()
        self.make_outline()
        
    def build_outline(self):
        super().build()
        
        part = cq.Workplane("XY")
        
        if self.outline:
            part = part.add(
                self.outline
                .translate((0,0,self.height/2))
            )
        
        return part
        
    def build(self):
        super().build()
        
        part = cq.Workplane("XY")
        
        if self.outline:
            part = (
                part.add(
                    self.outline
                    .translate((0,0,self.height/2))
                )
            )
        
        return part