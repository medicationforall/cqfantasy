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

def arch(
        length:float = 30, 
        width:float = 5, 
        height:float = 75
    ) -> cq.Workplane:
    if length > height:
        raise Exception(f'{length=} is greater than {height=}')
    cylinder = cq.Workplane("XZ").cylinder(width, length/2)
    base = cq.Workplane("XY").box(length, width, height-length/2)
    
    combined_arch = (
        base
        .union(cylinder.translate((0,0,height/2-length/4)))
        .translate((0,0,-length/4))
    )
    return combined_arch