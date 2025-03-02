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

class Body(Base):
    def __init__(self):
        super().__init__()
        #parameters
        self.length:float = 150
        self.width:float = 150
        self.height:float = 75
        self.wall_width:float = 4
        self.floor_height:float = 4
        
        #shapes
        self.body:cq.Workplane|None = None
        
    def make_body(self):
        body = (
            cq.Workplane("XY")
            .box(self.length, self.width, self.height)
        )
        
        body = (
            body
            .faces("Z")
            .rect(self.length-self.wall_width*2,self.width-self.wall_width*2)
            .extrude(-self.height+self.floor_height, combine="s")
        )
        
        self.body = body
        
    def make(self, parent=None):
        super().make(parent)
        self.make_body()
        
    def build(self) -> cq.Workplane:
        super().build()

        scene = cq.Workplane("XY")

        if self.body:
            scene = scene.union(self.body)
            
        return scene