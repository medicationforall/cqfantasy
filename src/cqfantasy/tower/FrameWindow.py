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
from cadqueryhelper import shape
from . import TowerWindow

class FrameWindow(TowerWindow):
    def __init__(self):
        super().__init__()
        # properties
        self.frame_width:float = 2
        self.frame_margin:float = 2
        
        # parts
        self.frame_outline:cq.Workplane|None = None
        self.frame:cq.Workplane|None = None
        
    def make_frame(self):
        inner_height = self.height - self.inner_height_margin
        
        frame = shape.arch_pointed(
          length = self.length,
          width = self.frame_width,
          height = self.height,
          inner_height = inner_height
        )
        
        inside_frame = shape.arch_pointed(
          length = self.length - self.frame_margin * 2,
          width = self.frame_width,
          height = self.height - self.frame_margin * 2,
          inner_height = inner_height - self.frame_margin
        )
        self.frame_outline = frame
        self.frame = frame.cut(inside_frame)
        
    def make(self, parent=None):
        super().make(parent)
        self.make_frame()
        
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