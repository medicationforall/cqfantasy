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
from typing import Tuple

class Roof(Base):
    def __init__(self):
        super().__init__()
        #parameters
        self.length:float = 100
        self.width:float = 150
        self.height:float = 75
        
        self.overhang:Tuple[float,float,float] = (4,4,4)
        
        self.render_overhang_inset:bool = True
        self.overhang_inset:Tuple[float,float,float] = (4,8,4)

        # blueprints
        self.bp_outside_wall = None
        
        #shapes
        self.roof:cq.Workplane|None = None
        self.roof_cut:cq.Workplane|None = None
        self.overhang_inset_cut = None
        
    def make_roof(self):
        pts = [(0,0),(self.length,0),((self.length/2,self.height))]
        roof = (
            cq.Workplane("XZ")
            .polyline(pts)
            .close()
            .extrude(self.width)
        ).translate((-self.length/2, self.width/2,-self.height/2))
                
        self.roof = roof
        
    def make_roof_cut(self):
        length = self.length - self.overhang[0]*2
        width = self.width - self.overhang[1]*2
        height = self.height - self.overhang[2]*2
        
        pts = [(0,0),(length,0),((length/2,height))]
        roof_cut = (
            cq.Workplane("XZ")
            .polyline(pts)
            .close()
            .extrude(width)
        ).translate((-length/2, width/2,-self.height/2))
                
        self.roof_cut = roof_cut
        
    def make_overhang_inset(self):
        length = self.length - self.overhang_inset[0]*2
        width = self.overhang_inset[1]
        height = self.height - self.overhang_inset[2]*2
        
        pts = [(0,0),(length,0),((length/2,height))]
        overhang_inset_cut = (
            cq.Workplane("XZ")
            .polyline(pts)
            .close()
            .extrude(width)
        ).translate((-length/2, width/2,-self.height/2))
        
        self.overhang_inset_cut = overhang_inset_cut
        
    def make_outside_wall(self):
        if self.bp_outside_wall:
            self.bp_outside_wall.length = self.length
            self.bp_outside_wall.height = self.height
            self.bp_outside_wall.make()
        
        
    def make(self, parent=None):
        super().make(parent)
        self.make_roof()
        self.make_roof_cut()
        
        if self.render_overhang_inset:
            self.make_overhang_inset()
            
        self.make_outside_wall()
        
    def build(self) -> cq.Workplane:
        super().build()
        scene = (
            cq.Workplane("XY")
        )

        if self.roof:
            scene = scene.union(self.roof)

        if self.roof_cut:
            scene = scene.cut(self.roof_cut)
            
        if self.render_overhang_inset and self.overhang_inset_cut:
            scene = (
                scene
                .cut(self.overhang_inset_cut.translate((0,self.width/2-self.overhang_inset[1]/2,0)))
                .cut(self.overhang_inset_cut.translate((0,-self.width/2+self.overhang_inset[1]/2,0)))
            )
            
        if self.bp_outside_wall:
            outside_wall = self.bp_outside_wall.build()
            
            y_translate = self.width/2+self.bp_outside_wall.panel_width/2
            
            if self.render_overhang_inset:
                outside_wall = outside_wall.intersect(self.overhang_inset_cut)
                y_translate -= self.overhang_inset[1]
                
            else:
                outside_wall = outside_wall.intersect(self.roof)
                
                
            scene = (
                scene
                .add(outside_wall.translate((0,y_translate,0)))
                .add(outside_wall.rotate((0,0,1),(0,0,0),180).translate((0,-y_translate,0)))
            )
            
        return scene