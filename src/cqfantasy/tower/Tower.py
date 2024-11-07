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
from . import TowerBase, TowerMid, TowerTop

class Tower(Base):
    def __init__(self):
        super().__init__()
        
        # blueprints
        self.base_bp:TowerBase = TowerBase()
        self.mid_bp:TowerMid = TowerMid()
        self.top_bp:TowerTop = TowerTop()
        
    def make(self, parent=None):
        super().make(parent)
        
        self.base_bp.make()
        self.mid_bp.make()
        self.top_bp.make()
        
        #self.make_base()
        #self.make_mid()
        #self.make_top()
        
    def build(self):
        super().build()
        
        base = self.base_bp.build()
        mid = self.mid_bp.build()
        top = self.top_bp.build()
        
        scene = (
            cq.Workplane("XY")
            .add(base)
            .add(mid.translate((0,0,self.base_bp.height)))
            .add(top.translate((0,0,self.base_bp.height+self.mid_bp.height)))
        )
        return scene
    
    def build_plate(self):
        super().build()
        
        base = self.base_bp.build()
        mid = self.mid_bp.build()
        top = self.top_bp.build()
        
        scene = (
            cq.Workplane("XY")
            .add(base)
            .add(mid.translate((self.base_bp.base_diameter,0,0)))
            .add(top.translate((self.base_bp.base_diameter+self.top_bp.top_diameter,0,0)))
        )
        return scene