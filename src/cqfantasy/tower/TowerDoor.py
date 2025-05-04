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
from cadqueryhelper import Base
from cqterrain.door import TiledDoor

class TowerDoor(Base):
    def __init__(self):
        super().__init__()
        # properties
        self.length:float = 30
        self.width:float = 4
        self.height:float = 50

        self.frame_width:float = 4
        
        self.outside_diameter:float = 130
        self.inside_diameter:float = 100
        self.y_offset = 0
        
        # shapes
        self.outline:cq.Workplane|None = None
        self.cut:cq.Workplane|None = None

        # blueprints
        self.bp_door = TiledDoor()

    def calculate_difference(self):
        return self.outside_diameter - self.inside_diameter
 
    def make_outline(self):
        outline = (
            cq.Workplane("XY")
            .cylinder(self.height, self.outside_diameter/2)
            .cylinder(self.height, self.inside_diameter/2, combine="cut")
        )
        
        self.outline = outline

    def make_door(self):
        self.bp_door.length = self.length
        self.bp_door.width = self.frame_width
        self.bp_door.height = self.height
        self.bp_door.make()

    def make_cut(self):
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
                0
            )))
        )
        
        self.cut = scene

    def make(self, parent=None):
        super().make(parent)
        self.make_outline()
        self.make_cut()
        self.make_door()

    def build_cut(self):
        scene = cq.Workplane("XY").union(self.cut)
        
        #if self.render_outline and self.outline:
        #    scene = scene.add(self.outline)   
        return scene
    
    def build(self) -> cq.Workplane:
        super().build()
        scene = (
            cq.Workplane("XY")
        )

        door = self.bp_door.build()

        difference = self.calculate_difference()
        y_offset = self.outside_diameter/2 - difference/4
        
        if door:
            scene = scene.union(door.translate((0,y_offset+self.y_offset,0)))
        
        return scene