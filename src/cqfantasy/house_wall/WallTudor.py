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
        
        self.render_top_bar = False
        self.render_bottom_bar = False
        self.render_side_bar = True
        self.bar_length = 3
        self.bar_height = 3
        
        #shapes
        self.outline:cq.Workplane|None = None
        self.tudor_wall:cq.Workplane|None = None
        self.bar:cq.Workplane|None = None
        self.side_bar:cq.Workplane|None = None

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
        
    def make_bar(self):
        self.bar = cq.Workplane("XY").box(self.length, self.width, self.bar_height)
        
    def make_side_bar(self):
        self.side_bar = cq.Workplane("XY").box(self.bar_length, self.width, self.height)

    def make(self, parent=None):
        super().make(parent)
        self.make_outline()
        self.make_tudor_wall()
        self.make_bar()
        self.make_side_bar()

    def build(self)->cq.Workplane:
        super().build()

        scene = cq.Workplane("XY")

        if True and self.tudor_wall:
            scene = scene.union(self.tudor_wall)

        if self.outline_intersect and self.outline:
            scene = scene.intersect(self.outline)
            
        if self.render_top_bar and self.bar:
            scene = scene.union(self.bar.translate((0,0,self.height/2-self.bar_height/2)))
            
        if self.render_bottom_bar and self.bar:
            scene = scene.union(self.bar.translate((0,0,-(self.height/2-self.bar_height/2))))
            
        if self.render_side_bar and self.side_bar:
            scene = (
                scene
                .union(self.side_bar.translate((-self.length/2-self.bar_length/2,0,0)))
                .union(self.side_bar.translate((self.length/2+self.bar_length/2,0,0)))
            )

        return scene
    
    def build_cut(self):
        return self.outline