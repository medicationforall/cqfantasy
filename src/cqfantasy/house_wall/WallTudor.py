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
from . import tudor_wall
from cadqueryhelper import Base

class WallTudor(Base):
    def __init__(self):
        super().__init__()

        #parameters
        self.length:float = 100
        self.width:float = 3
        self.height:float = 75 
        self.styles:list[str|None]|str|None = [None,"cross","left","right"]
        self.panel_length:float = 25
        self.panel_space:float = 3
        self.panel_sections:int|None = None

        self.outline_intersect:bool = True
        
        #shapes
        self.outline:cq.Workplane|None = None
        self.tudor_wall:cq.Workplane|None = None

    def make_tudor_wall(self):
        panel_length = self.panel_length

        if self.panel_sections:
            panel_length = self.length / self.panel_sections

        self.tudor_wall = tudor_wall(
            length =  self.length, 
            height = self.height, 
            styles = self.styles, 
            panel_length = panel_length, 
            panel_space = self.panel_space, 
            panel_width = self.width
        )
        
    def make_outline(self):
        outline = cq.Workplane("XY").box(
            self.length, 
            self.width, 
            self.height
        )
        
        self.outline  = outline

    def make(self, parent=None):
        super().make(parent)
        self.make_outline()
        self.make_tudor_wall()

    def build(self)->cq.Workplane:
        super().build()

        scene = cq.Workplane("XY")

        if self.tudor_wall:
            scene = scene.union(self.tudor_wall)

        if self.outline_intersect and self.outline:
            scene = scene.intersect(self.outline)

        return scene
    
    def build_cut(self):
        return self.outline