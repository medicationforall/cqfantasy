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
from . import BasicBase, BasicBarDecoration
from . import BasicPillar

class BasicFence(Base):
    def __init__(self):
        super().__init__()
        #parameterss
        
        #blueprints
        self.bp_base:BasicBase|None = BasicBase()
        self.bp_pillar:BasicPillar|None = BasicPillar()
        self.bp_bars:BasicBarDecoration|None = BasicBarDecoration()
        
        #shapes
        
    def make_outline(self):
        length = 0
        width = 0
        height = 0
        
        if self.bp_base:
            length += self.bp_base.length
            width += self.bp_base.width
            height += self.bp_base.height
            
        if self.bp_pillar:
            length += self.bp_pillar.length * 2
            width += self.bp_pillar.width
            
        if self.bp_bars:
            height += self.bp_bars.calculate_height()
            
        outline = cq.Workplane("XY").box(
            length,
            width,
            height
        ).translate((0,0,height/2))
        
        self.outline = outline
        
    def make(self):
        super().make()

        if self.bp_base:
            self.bp_base.make()

        if self.bp_pillar:
            self.bp_pillar.make()

        if self.bp_bars:
            if self.bp_base:
                self.bp_bars.length = self.bp_base.length
            self.bp_bars.make()
        self.make_outline()
        
    def build_outline(self)->cq.Workplane:
        super().build()
        
        part = cq.Workplane("XY")
        
        if self.outline:
            part = part.add(self.outline)
        
        return part
        
    def build(self)->cq.Workplane:
        super().build()
        
        part = cq.Workplane("XY")

        base_height = 0
        base_length = 0
        
        if self.bp_base:
            base_height = self.bp_base.height
            base_length = self.bp_base.length
            fence_base = self.bp_base.build()
            part = part.union(fence_base)
            
        if self.bp_bars:
            bars = (
                self.bp_bars.build()
                .translate((0,0,base_height))
            )
            
            part = part.union(bars)
            
        if self.bp_pillar:
            x_translate = base_length/2+ self.bp_pillar.length/2
            pillar = (self.bp_pillar.build())
            part = (
                part
                .union(pillar.translate((x_translate,0,0)))
                .union(pillar.translate((-x_translate,0,0)))
            )
            
        return part