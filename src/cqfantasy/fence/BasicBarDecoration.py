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
import math
from cadqueryhelper import Base

class BasicBarDecoration(Base):
    def __init__(self):
        super().__init__()
        #parameters
        self.length:float = 75
        self.width:float = 5
        self.height:float = 20
        
        self.bar_height:float = 3
        self.bar_z_translate:float|None = None
        self.spike_count:int = 11
        self.spike_lift:float = 4
        self.spike_diameter:float = 3
        
        #shapes
        self.outline:cq.Workplane|None = None
        self.spikes:cq.Workplane|None = None
        self.crossbar:cq.Workplane|None = None
        
    def calculate_height(self):
        #index = math.floor(self.spike_count/2)
        if self.spike_count % 2 == 0:
            index = math.ceil(self.spike_count/2)-1
        else:
            index = math.ceil(self.spike_count/2)
            
        spike_lift = self.spike_lift
        lifted_height = index*spike_lift
        height = self.height + lifted_height
        #log(f'max_height is {height} {index}')
        return height
        
    def make_outline(self):
        height = self.calculate_height()
        outline = cq.Workplane("XY").box(
            self.length,
            self.width,
            height
        ).translate((0,0,height/2))
        
        self.outline = outline
    
    def make_crossbar(self):
        z_translate = self.height/2
        
        if self.bar_z_translate:
            z_translate =  self.bar_z_translate
        
        crossbar = cq.Workplane("XY").box(
            self.length,
            self.width,
            self.bar_height
        ).translate((0,0,z_translate))
        
        self.crossbar = crossbar
        
    def make_spikes(self):
        spike_count = self.spike_count
        spike_lift = self.spike_lift
        spike_distance = self.length / spike_count
        
        spike = cq.Workplane("XY").cylinder(self.height,self.spike_diameter/2)
        
        spikes = cq.Workplane("XY")

        for i in range(math.floor(spike_count/2)):
            alt_spike = spike
            if i > 0:
                alt_spike = spike.faces("<Z").wires().toPending().extrude(-i*spike_lift)
            #log(i*spike_lift)
            #show_object(alt_spike)
            spikes = (
                spikes
                .add(alt_spike.translate((spike_distance*i,0,i*spike_lift)))
                .add(alt_spike.translate((self.length-(spike_distance*i)-spike_distance,0,i*spike_lift)))
            )
            
        spikes = spikes.translate((-(self.length/2)+spike_distance/2,0,))
        
        if spike_count % 2 == 1:
            index = math.ceil(spike_count/2)
            alt_spike = spike.faces("<Z").wires().toPending().extrude(-index*spike_lift)
            spikes = spikes.add(alt_spike.translate((0,0,index*spike_lift)))
            
        
        self.spikes = spikes.translate((0,0,self.height/2))
    
    def make(self):
        super().make()
        self.make_outline()
        self.make_crossbar()
        self.make_spikes()
        
    def build_outline(self)->cq.Workplane:
        super().build()
        
        part = cq.Workplane("XY")
        
        if self.outline:
            part = part.add(self.outline)
        
        return part
        
    def build(self)->cq.Workplane:
        super().build()
        
        part = cq.Workplane("XY")
        
        if self.crossbar:
            part = part.add(self.crossbar)
            
        if self.spikes:
            part = part.add(self.spikes)
        
        return part