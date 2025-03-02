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
from cqterrain.material import uneven_centered_blocks
import random
from typing import Literal, Tuple
from . import RoundBlockGenerator

try:
    log #type:ignore
except NameError:
    log = print

class RoundBlockUnevenStuccoGenerator(RoundBlockGenerator):
    def __init__(self):
        super().__init__()

        self.uneven_block_depth:float = 1
        self.seed:str|None = 'test4'
        self.facing:Literal["outside", "inside"] = "outside"

        self.cell_types = [
            'block',
            'block', 
            'empty',
            'block'
        ]
        self.wfc_data:list[list[str]]|None = None
        self.add_row_count = 0

        self.uneven_blocks:list|None = None

        self.intersect_body = None

    def wave_form_map(
        self,
        size:Tuple[int,int]=(10,10),
        seed:str|None = 'test'
    ) -> list[list[str]]:
        log("run wfc")
        if seed:
            random.seed(seed)
        
        wfc_grid = []
        for row in range(size[0]):
            cells = []
            for cell in range(size[1]):
                if row>0:
                    if wfc_grid[row-1][cell] == 'empty':
                        cells.append('empty')
                    else:
                        #random cell
                        type = random.choice(self.cell_types)
                        cells.append(type)
                else:
                    #random cell
                    type = random.choice(self.cell_types)
                    cells.append(type)
                
                
            wfc_grid.append(cells)

        return wfc_grid
    
    def make_intersect_body(self):
        if self.base_diameter is not None and self.base_diameter != self.top_diameter:
            body = cq.Solid.makeCone(
                self.base_diameter / 2 +self.block_length/2, 
                self.top_diameter / 2 +self.block_length/2, 
                self.height
            )
            
            int_body = cq.Solid.makeCone(
                self.base_diameter / 2 -self.block_length/2, 
                self.top_diameter / 2 -self.block_length/2, 
                self.height
            )
            
            body = cq.Workplane("XY").add(body).cut(int_body)
        else:
            body = (
                cq.Workplane("XY")
                .cylinder(self.height, self.top_diameter / 2+self.block_length/2)
                .translate((0,0,self.height / 2))
            )
            
            int_body = (
                cq.Workplane("XY")
                .cylinder(self.height, self.top_diameter / 2-self.block_length/2)
                .translate((0,0,self.height / 2))
            )
            
            body = cq.Workplane("XY").add(body).cut(int_body)

        self.intersect_body = body

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
        block_width = self.calculate_block_width(radius)
        block_height = self.calculate_block_height()
        block_margin_width = self.calculate_block_margin_width(radius)
        block_margin_height = self.calculate_block_margin_height()

        i_block = cq.Workplane("XY").box(self.block_length, block_margin_width, block_margin_height)

        count = 0
        row = self.add_row_count

        r_block = cq.Workplane("XY").box(self.block_length,block_width+.3, block_height)

        def add_block(loc:cq.Location) -> cq.Shape:
            nonlocal count
            nonlocal row
            nonlocal r_block
            cell = count % (self.row_count)

            if self.wfc_data:
                block_type = self.wfc_data[row][cell]

            count += 1

            if count < 1 and row == 0:
                return cq.Workplane("XY").cylinder(1,1).val().located(loc) #type:ignore
        
            if block_type is 'block':
                c_block = self.get_block().intersect(i_block)
                return c_block.val().located(loc) #type:ignore
            else:
                if self.intersect_body:
                    ir_block = r_block.intersect(self.intersect_body)
                    return ir_block.val().located(loc) #type:ignore
                else:
                    
                    return r_block.val().located(loc) #type:ignore
            
        self.add_row_count+=1
        return add_block
    
    def make(self, parent=None):
        self.wfc_data = self.wave_form_map((self.row_count,self.block_ring_count), self.seed)
        self.make_intersect_body()
        super().make()