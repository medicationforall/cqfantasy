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
from cadqueryhelper import shape
from cqfantasy.tower import TowerWindow
from cqterrain.window import casement

class CasementWindow(TowerWindow):
    def __init__(self):
        super().__init__()
        # properties
        self.frame_width:float = 2
        self.frame_margin:float = 2
        self.frame_columns:int = 2 
        self.frame_rows:int = 3
        self.grill_width:float = 1 
        self.grill_height:float = 1
        
        # parts
        self.frame_outline:cq.Workplane|None = None
        self.frame:cq.Workplane|None = None
        
    def make_frame(self):
        inner_height = self.height - self.inner_height_margin
        
        
        frame = casement(
            length = self.length, 
            width = self.width, 
            height = self.height, 
            colums = self.frame_columns, 
            rows = self.frame_rows, 
            frame_width = self.frame_width, 
            grill_width = self.grill_width, 
            grill_height = self.grill_width
        )
        
        self.frame_outline = frame
        self.frame = frame#.cut(inside_frame)

    def make_cut(self):
        inner_height = self.height - self.inner_height_margin
        cut_width = self.calculate_difference()/1.5
        
        cut = cq.Workplane("XY").box(
          length = self.length,
          width = cut_width,
          height = self.height
        )
        
        scene = (
            cq.Workplane("XY")
            .union(self.outline)
            .intersect(cut.translate((
                0,
                self.outside_diameter/2-cut_width/2,
                0)
            ))
        )
        
        self.cut = scene
        
    def make(self, parent=None):
        super().make(parent)
        self.make_frame()


    def build_cut(self):
        if self.render_cylinder and self.cut:
            scene = cq.Workplane("XY").union(self.cut)
        else:
            #this is a hack
            cut_width = self.calculate_difference()/1.5
            scene = cq.Workplane("XY").box(
                length = self.length,
                width = cut_width,
                height = self.height
            ) 
        return scene
        
    def build(self):
        super().build()
        scene = (
            cq.Workplane("XY")
        )

        if self.render_cylinder:
            difference = self.calculate_difference()
            y_offset = self.outside_diameter/2 - difference/4
        else:
            y_offset = 0

        if self.frame:
            scene = scene.union(self.frame).translate((0,y_offset,0))
        
        return scene