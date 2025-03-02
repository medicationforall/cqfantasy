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
from . import RoundBlockGenerator
from cqterrain.material import uneven_centered_blocks
import random
from typing import Literal

class RoundBlockUnevenGenerator(RoundBlockGenerator):
    def __init__(self):
        super().__init__()

        self.uneven_block_depth:float = 1
        self.seed:str|None = 'test4'
        self.facing:Literal["outside", "inside"] = "outside"

        self.uneven_blocks:list|None = None

    def make_block(self):
        block_height = self.calculate_block_height()
        diameter = self.calculate_largest_diameter()

        block_width = self.calculate_block_width(diameter/2)

        blocks = uneven_centered_blocks(
            tile_length = block_height,
            tile_width = block_width,
            tile_height= self.block_length,
            rows = 6, 
            columns = 6, 
            margin = 2,
            uneven_depth = self.uneven_block_depth,
            seed=self.seed,
            segments = 10,
            peak_count = (14,15)
        )

        rotated_blocks = []
        for block in blocks:
            if self.facing is "outside":
                block = block.rotate((0,1,0),(0,0,0),-90)
            else:
                block = block.rotate((0,1,0),(0,0,0),90)
            rotated_blocks.append(block)
        
        self.uneven_blocks = rotated_blocks

    def get_block(self) -> cq.Workplane:
        if self.uneven_blocks:
            chosen_block = random.choice(self.uneven_blocks)
            return chosen_block
        else:
            raise Exception("Could not resolve block")
        

    def resolve_add_block(self, radius):
        block_margin_width = self.calculate_block_margin_width(radius)
        block_margin_height = self.calculate_block_margin_height()

        i_block = cq.Workplane("XY").box(self.block_length, block_margin_width, block_margin_height)
        
        def add_block(loc:cq.Location) -> cq.Shape:
            c_block = self.get_block().intersect(i_block)
            return c_block.val().located(loc) #type:ignore
        
        return add_block