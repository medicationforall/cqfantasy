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
from ..arch import StoneArch
from . import VDoor

class ArchDoor(Base):
    def __init__(self):
        super().__init__()
        
        self.length:float = 50
        self.width:float = 7
        self.height:float = 75
        self.door_inset:float = 2
        
        #blueprints
        self.bp_arch = StoneArch()
        self.bp_arch.outside_margin = 5
        self.bp_arch.outside_stone_position = 0
        self.bp_arch.stone_arch_count = 6
        self.bp_arch.stone_arch_modulus = 2
        
        self.bp_door = VDoor()
        
    def make_arch(self):
        if self.bp_arch:
            self.bp_arch.length = self.length
            self.bp_arch.width = self.width
            self.bp_arch.height = self.height
            self.bp_arch.make()
    
    def make_door(self):
        if self.bp_door:
            self.bp_door.length = self.length - self.bp_arch.inside_margin*2
            self.bp_door.width = self.width - self.door_inset
            self.bp_door.height = self.height - self.bp_arch.inside_margin
            self.bp_door.make()
        
    def make(self, parent=None):
        super().make(parent)
        self.make_arch()
        self.make_door()
        
        
    def build(self):
        super().build()
        scene = cq.Workplane("XY")
        
        if self.bp_arch:
            ex_arch = self.bp_arch.build()
            scene = scene.add(ex_arch)
            
        if self.bp_door:
            ex_door = self.bp_door.build()
            scene = scene.add(ex_door.translate((0,0,- self.bp_arch.inside_margin/2)))
            
        return scene
    
    def build_outline(self):
        return self.bp_arch.build_outline()