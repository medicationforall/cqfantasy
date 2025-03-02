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

from . import Body, Roof
from cqterrain.door import TiledDoor

class House(Base):
    def __init__(self):
        super().__init__()
        #parameters
        self.length:float = 100
        self.width:float = 150
        self.height:float = 75
        
        self.roof_height:float = 50
        self.roof_overhang:Tuple[float,float] = (10,5)
        self.roof_gap_spacer:float = 0

        self.door_cut_width_padding:float = 0
        
        #shapes
        self.door_cut:cq.Workplane|None = None
        
        #blueprints
        self.bp_body = Body()
        self.bp_roof = Roof()
        self.bp_door = TiledDoor()
        
    def make_body(self):
        self.bp_body.length = self.length
        self.bp_body.width = self.width
        self.bp_body.height = self.height
        self.bp_body.make()
        
    def make_roof(self):
        self.bp_roof.length = self.length+self.roof_overhang[0]*2
        self.bp_roof.width = self.width+self.roof_overhang[1]*2
        self.bp_roof.height = self.roof_height
        #bp_roof.overhang = (bp_house.roof_overhang[0],bp_house.roof_overhang[1], 4)

        self.bp_roof.overhang = (
            self.roof_overhang[0]+self.bp_body.wall_width,
            self.roof_overhang[1]+self.bp_body.wall_width, 
            4
        )
        self.bp_roof.make()
        
    def make_door(self):
        self.bp_door.make()
        
    def make_door_cut(self):
        self.door_cut = (
            cq.Workplane("XY")
            .box(self.bp_door.length,self.bp_body.wall_width+self.door_cut_width_padding,self.bp_door.height)
        )

    def make(self, parent=None):
        super().make(parent)
        self.make_body()
        self.make_roof()
        self.make_door()
        self.make_door_cut()
        
    def build(self) -> cq.Workplane:
        #log("build")
        super().build()
        body = self.bp_body.build()
        roof = self.bp_roof.build()
        door = self.bp_door.build()
        door_cut = self.door_cut
        
        scene = (
            cq.Workplane("XY")
        )

        if body:
            scene = scene.union(body.translate((0,0,self.bp_body.height/2)))

        if door_cut:
            scene = scene.cut(door_cut.translate((0,-self.width/2+self.bp_body.wall_width/2,self.bp_door.height/2+self.bp_body.floor_height)))

        if door:
            scene = scene.union(door.translate((0,-self.width/2+self.bp_body.wall_width/2,self.bp_door.height/2+self.bp_body.floor_height)))

        if roof:
            scene = scene.add(roof.translate((0,0,self.bp_body.height+self.bp_roof.height/2+self.roof_gap_spacer)))


        return scene
    
    
    def build_plate(self):
        #log("build_plate")
        body = self.bp_body.build()
        roof = self.bp_roof.build()
        door = self.bp_door.build()
        door_cut = self.door_cut
        
        scene = (
            cq.Workplane("XY")
        )


        if body:
            scene = scene.union(body.translate((0,0,self.bp_body.height/2)))
        if door_cut:
            scene = scene.cut(door_cut.translate((0,-self.width/2+self.bp_body.wall_width/2,self.bp_door.height/2+self.bp_body.floor_height)))

        if door:
            scene = scene.union(door.translate((0,-self.width/2+self.bp_body.wall_width/2,self.bp_door.height/2+self.bp_body.floor_height)))

        if roof:
            scene = scene.add(roof.translate((self.bp_body.length/2+self.bp_roof.length/2+10,0,self.bp_roof.height/2)))
        return scene
    
    def build_cut_away(self):
        #log("build_cut_away")
        house = self.build()
        length = self.length + self.roof_overhang[0]*2
        width = self.width + self.roof_overhang[1]*2
        height = self.height+self.roof_height+50
        cut_away = cq.Workplane("XY").box(length,width,height)
        scene = (
            cq.Workplane("XY")
            .add(house)
            .cut(cut_away.translate((-length/2,0,height/2)))
            .cut(cut_away.translate((0,width/2,height/2)))

        )
        
        return scene