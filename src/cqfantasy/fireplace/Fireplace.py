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
from . import Hearth, FireBox, FireTop, Chimney

class Fireplace(Base):
    def __init__(self):
        super().__init__()
        #parameters
        #self.length = 30
        #self.width = 25
        #self.height = 75
        self.interior_padding:float = 2
        
        self.render_hearth:bool = True
        
        #blueprints
        self.bp_hearth:Hearth = Hearth()
        self.bp_firebox:FireBox = FireBox()
        self.bp_firetop:FireTop = FireTop()
        self.bp_chimney:Chimney = Chimney()
        
        #shapes
        self.outline:cq.Workplane|None = None
        
        
    def make_firebox(self):
        self.bp_firebox.y_padding = self.interior_padding
        self.bp_firebox.make()
        
        
    def make_top(self):
        length = self.bp_firebox.length
        width = self.bp_firebox.width
        
        self.bp_firetop.length = length
        self.bp_firetop.width = width
        self.bp_firetop.interior_padding = self.interior_padding 
        self.bp_firetop.make()
        
    def make_chimney(self):
        length = self.bp_firetop.top_length 
        width = self.bp_firetop.top_width
        
        self.bp_chimney.interior_padding = self.interior_padding 
        self.bp_chimney.length = length
        self.bp_chimney.width = width
        self.bp_chimney.make()
        
    def make(self):
        super().make()
        self.bp_hearth.make()
        self.make_firebox()
        self.make_top()
        self.make_chimney()
        
    def build_outline(self):
        super().build()
        
        part = cq.Workplane("XY")
        
        if self.bp_hearth and self.render_hearth:
            hearth = self.bp_hearth.build_outline()
            part = part.union(hearth)
            
        if self.bp_firebox:
            firebox = self.bp_firebox.build_outline()
            z_translate = self.bp_hearth.height
            y_translate = self.bp_hearth.width/2 - self.bp_firebox.width/2
            part = (
                part.union(
                    firebox.translate((
                        0,
                        y_translate,
                        z_translate
                    ))
                )
            )
            
        if self.bp_firetop:
            firetop = self.bp_firetop.build_outline()
            z_translate = self.bp_hearth.height + self.bp_firebox.height
            y_translate = self.bp_hearth.width/2 - self.bp_firetop.width/2
            part = (
                part.union(
                    firetop.translate((
                        0,
                        y_translate,
                        z_translate
                    ))
                )
            )
            
        if self.bp_chimney:
            chimney = self.bp_chimney.build_outline()
            z_translate = self.bp_hearth.height + self.bp_firebox.height + self.bp_firetop.height
            y_translate = self.bp_hearth.width/2 - self.bp_chimney.width/2
            part = (
                part.union(
                    chimney.translate((
                        0,
                        y_translate,
                        z_translate
                    ))
                )
            )
        
        return part
        
    def build(self):
        super().build()
        
        part = cq.Workplane("XY")
            
        if self.bp_hearth and self.render_hearth:
            hearth = self.bp_hearth.build()
            part = part.union(hearth)
            
        if self.bp_firebox:
            firebox = self.bp_firebox.build()
            z_translate = self.bp_hearth.height
            y_translate = self.bp_hearth.width/2 - self.bp_firebox.width/2
            part = (
                part.union(
                    firebox.translate((
                        0,
                        y_translate,
                        z_translate
                    ))
                )
            )
            
        if self.bp_firetop:
            firetop = self.bp_firetop.build()
            z_translate = self.bp_hearth.height + self.bp_firebox.height
            y_translate = self.bp_hearth.width/2 - self.bp_firetop.width/2
            part = (
                part.union(
                    firetop.translate((
                        0,
                        y_translate,
                        z_translate
                    ))
                )
            )
            
        if self.bp_chimney:
            chimney = self.bp_chimney.build()
            z_translate = self.bp_hearth.height + self.bp_firebox.height + self.bp_firetop.height
            y_translate = self.bp_hearth.width/2 - self.bp_chimney.width/2
            part = (
                part.union(
                    chimney.translate((
                        0,
                        y_translate,
                        z_translate
                    ))
                )
            )
        
    
        return part