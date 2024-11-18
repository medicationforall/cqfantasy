import cadquery as cq
from cadqueryhelper import Base
from . import RoundBlockGenerator
from cqterrain.material import uneven_centered_blocks
import random
from typing import Literal
from cqterrain import tile

class RoundBlockAltGenerator(RoundBlockGenerator):
    def __init__(self):
        super().__init__()

        self.uneven_block_depth:float = 1
        self.seed:str|None = 'test4'
        self.facing:Literal["outside", "inside"] = "outside"
        self.block_modulus = 10
        self.block_remainder = 0

        self.uneven_blocks:list|None = None
        self.bolt:cq.Workplane|None = None

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

        #-----------------
        bolt = tile.bolt_panel(
            length = block_height, 
            width = block_width, 
            height = self.block_length, 
            chamfer = .5, 
            radius_outer=1,
            radius_internal=0.5,
            cut_height=0.5,
            padding = 2
        )

        if self.facing is "outside":
            bolt = bolt.rotate((0,1,0),(0,0,0),-90)
        else:
            bolt = bolt.rotate((0,1,0),(0,0,0),90)

        self.bolt = bolt
        

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
        block_count = 0
        
        def add_block(loc:cq.Location) -> cq.Shape:
            nonlocal block_count

            if block_count % self.block_modulus == self.block_remainder:
                c_block = self.bolt
            else:
                c_block = self.get_block().intersect(i_block)
            block_count += 1

            return c_block.val().located(loc) #type:ignore
        
        return add_block