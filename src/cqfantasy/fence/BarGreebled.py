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
from cadqueryhelper import Base
from cqfantasy.fence import BasicBarDecoration
import math
from cadqueryhelper.shape import pyramid

class BarGreebled(BasicBarDecoration):
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
        self.spike_diameter:float = 2.5
        
        self.top_length:float = 3.5
        self.top_width:float = 3.5
        self.top_height:float = 4
        
        #shapes
        self.outline:cq.Workplane|None = None
        self.spike:cq.Workplane|None = None
    
    def make_spike(self):
        height = self.height-self.top_height
        spike = (
            cq.Workplane("XY")
            .rect(self.spike_diameter,self.spike_diameter)
            .twistExtrude(height, 270)
            .translate((0,0,-height/2))
        )
        
        top = pyramid(self.top_length, self.top_width, self.top_height)
        
        top = top.union(top.rotate((0,1,0),(0,0,0),180)).translate((0,0,height/2))
        self.spike = spike.add(top)
        
    def make_spikes(self):
        spike_count = self.spike_count
        spike_lift = self.spike_lift
        spike_distance = self.length / spike_count
        
        if self.spike:
            spike = self.spike
        else:
            raise Exception("Unable to resolve spike")
        
        spikes = cq.Workplane("XY")

        for i in range(math.floor(spike_count/2)):
            alt_spike = spike
            if i > 0:
                alt_spike = spike.faces("<Z").wires().toPending().workplane().twistExtrude(i*spike_lift,i*90)

            spikes = (
                spikes
                .union(alt_spike.translate((spike_distance*i,0,i*spike_lift)))
                .union(alt_spike.translate((self.length-(spike_distance*i)-spike_distance,0,i*spike_lift)))
            )
            
        spikes = spikes.translate((-(self.length/2)+spike_distance/2,0,))
        
        if spike_count % 2 == 1:
            index = math.ceil(spike_count/2)
            alt_spike = spike.faces("<Z").wires().toPending().workplane().twistExtrude(index*spike_lift,(index-1)*90)
            spikes = spikes.union(alt_spike.translate((0,0,index*spike_lift)))
            
        
        height = self.height-self.top_height
        self.spikes = spikes.translate((0,0,height/2))
        
    def make(self):
        self.make_called = True
        self.make_outline()
        self.make_crossbar()
        self.make_spike()
        self.make_spikes()
        
    def build(self)->cq.Workplane:
        if self.make_called == False:
            raise Exception('Make has not been called')
        
        part = cq.Workplane("XY")
        
        if self.crossbar:
            part = part.union(self.crossbar)
            
        if self.spikes:
            part = part.union(self.spikes)
        
        return part