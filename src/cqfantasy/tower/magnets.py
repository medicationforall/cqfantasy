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

def make_magnet(diameter:float=3.2, height:float=2.4)->cq.Workplane:
    cut = cq.Workplane("XY").cylinder(height,diameter/2)
    return cut

def make_magnets(magnet:cq.Workplane, count:int=4, diameter:float=130):
    magnets = cq.Workplane("XY")
    degrees = 360 / count

    for i in range(count):
        magnets = magnets.union(magnet.translate((0,diameter/2,0)).rotate((0,0,1),(0,0,0),degrees*i))

    return magnets