# Copyright 2024 James Adams
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
from cadqueryhelper import Base, shape

class TowerWindow(Base):
    def __init__(self):
        super().__init__()
        
        # properties
        self.length:float = 25
        self.width:float = 2
        self.height:float = 30
        self.inner_height_margin:float = 15
        
        self.diameter:float = 130
        self.render_outline:bool = False
        
        # shapes
        self.outline:cq.Workplane|None = None
        self.window:cq.Workplane|None = None
        self.cut:cq.Workplane|None = None
        
    def make_outline(self):
        outline = (
            cq.Workplane("XY")
            .cylinder(self.height, self.diameter/2)
            .cylinder(self.height, self.diameter/2-self.width, combine="cut")
        )
        
        self.outline = outline
        
    def make_cut(self):
        inner_height = self.height - self.inner_height_margin
        cut_width = self.diameter /2
        
        cut = shape.arch_pointed(
          length = self.length,
          width = cut_width,
          height = self.height,
          inner_height = inner_height
        )
        
        scene = (
            cq.Workplane("XY")
            .union(self.outline)
            .intersect(cut.translate((0,(self.diameter/2-self.width/2)-self.width/4,0)))
        )
        
        self.cut = scene#.translate((0,-((self.diameter/2-self.wall_width/2)-self.width/4),0))
        
    def make_window(self):
        inner_height = self.height - self.inner_height_margin
        
        window = shape.arch_pointed(
          length = self.length,
          width = self.width,
          height = self.height,
          inner_height = inner_height
        )
        
        self.window = window
        
    def make(self, parent=None):
        super().make(parent)
        self.make_outline()
        self.make_cut()
        self.make_window()
        
    def build(self):
        super().build()
        scene = (
            cq.Workplane("XY")
        )

        if self.window:
            scene = scene.union(self.window.translate((0,(self.diameter/2-self.width/2)-self.width/4,0)))
        
        return scene
        
        
    def build_cut(self):
        scene = cq.Workplane("XY").union(self.cut)
        
        if self.render_outline and self.outline:
            scene = scene.add(self.outline)   
        return scene