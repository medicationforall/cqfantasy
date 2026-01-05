# Copyright 2026 James Adams
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
from cqterrain.material import BricksLayered
from cqterrain.shieldwall import Magnets
from . import BasicBase

class BaseBrick(BasicBase):
    def __init__(self):
        super().__init__()
        #parameters
        self.length:float = 75
        self.width:float = 20
        self.height:float = 25
        self.inner_padding:float = .6
        self.chamfer:float|None = 4

        self.render_magnets:bool = True
        self.magnet_padding:float = 1
        self.magnet_padding_x:float = 2
        self.base_height:float = 5.6 # used for adusting magnet placement
        
        #blueprints
        self.bp_bricks = BricksLayered()
        self.magnets_bp = Magnets()
        
        #shapes
        self.outline:cq.Workplane|None = None
        self.inner = None
        
    def make_outline(self):
        outline = cq.Workplane("XY").box(
            self.length,
            self.width,
            self.height
        )
        
        if self.chamfer:
            outline = outline.faces(">Z").edges("X").chamfer(self.chamfer)
        
        self.outline = outline
        
    def make_inner(self):
        length = self.length - self.inner_padding * 2
        width = self.width - self.inner_padding *2
        height = self.height - self.inner_padding
        
        inner = cq.Workplane("XY").box(
            length,
            width,
            height
        ).translate((0,0,height/2))
        
        if self.chamfer:
            inner = inner.faces(">Z").edges("X").chamfer(self.chamfer)
        
        self.inner = inner

    def make_magnets(self):
        self.magnets_bp.distance = self.width - self.magnets_bp.pip_radius*2 - self.magnet_padding*2 - self.magnet_padding_x
        self.magnets_bp.make()

    def make(self):
        super().make()
        self.make_outline()
        
        self.bp_bricks.length = self.length
        self.bp_bricks.width = self.width
        self.bp_bricks.height = self.height
        self.bp_bricks.make()
        self.make_inner()
        self.make_magnets()


    def build_magnets(self) -> cq.Workplane:
        magnets = self.magnets_bp.build()
        magnet_x = self.length/2 - self.magnets_bp.pip_height/2
        magnet_z = self.base_height - self.magnets_bp.pip_radius - self.magnet_padding
        scene = (
            cq.Workplane("XY")
            .union(magnets.translate((magnet_x,0,magnet_z)))
            .union(magnets.translate((-magnet_x,0,magnet_z)))
        )
        return scene
        
    def build(self)->cq.Workplane:
        super().build()
        
        part = cq.Workplane("XY")
            
        if self.bp_bricks and self.outline:
            bricks = self.bp_bricks.build()
            part = self.outline.translate((0,0,self.height/2)).intersect(bricks)
           # part = bricks
            
        if self.inner:
            part = part.union(self.inner)

        if self.render_magnets and self.magnets_bp:
            magnets = self.build_magnets()
            part = part.cut(magnets)
            
        return part