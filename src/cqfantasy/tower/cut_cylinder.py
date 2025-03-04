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

def cut_cylinder(
        parent:cq.Workplane, 
        diameter:float=130-8, 
        height:float=100-4
    ) -> cq.Workplane:
    parent = (
        parent
        .faces(">Z")
        .workplane()
        .circle(diameter/2)
        .extrude(-height, combine="cut")
    )
    return parent