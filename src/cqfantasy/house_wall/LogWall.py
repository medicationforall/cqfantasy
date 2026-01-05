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

class LogWall(Base):
    def __init__(self):
        super().__init__()
        #parameters
        self.length:float = 30
        self.width:float = 5
        self.height:float = 60
        self.log_count:int = 9
        self.diameter_overlap:float =5
        self.spread_width:bool = True
        
        #shapes
        self.outline = None
        self.logs = None
        
    def make_outline(self):
        outline = cq.Workplane("XY").box(
            self.length,
            self.width,
            self.height
        )
        
        self.outline = outline
        
    def make_logs(self):
        diameter = (self.height / self.log_count)+self.diameter_overlap
        height = self.height / self.log_count
        t_log = (
            cq.Workplane("XY")
            .cylinder(self.length + self.width, diameter/2)
            .rotate((0,1,0),(0,0,0),90)
            .translate((0,self.width/2-diameter/2,0))
        )
        
        c_log = cq.Workplane("XY").box(self.length+self.width, self.width, height)
        
        combined_log = t_log.intersect(c_log)
        
        logs = cq.Workplane("XY")
        
        for i in range(self.log_count):
            translate = 0
            
            if self.spread_width:
                if i % 2 == 0:
                    translate = self.width/2
                else:
                    translate = -self.width/2
                
            logs = logs.union(combined_log.translate((translate,0,height*i)))
            
        
        self.logs = logs.translate((0,0,-self.height/2+height/2))
        
        
    def make(self):
        super().make()
        self.make_outline()
        self.make_logs()
        
    def build_outline(self):
        super().build()
        
        part = cq.Workplane("XY")
        
        if self.outline:
            part = part.add(self.outline)
        
        return part
        
    def build(self):
        super().build()
        
        part = cq.Workplane("XY")
        
        #if self.outline:
        #   part = part.add(self.outline)
            
        if self.logs:
            part = part.add(self.logs)
        
        return part.rotate((0,0,1),(0,0,0),180)