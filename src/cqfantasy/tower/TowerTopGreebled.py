import cadquery as cq
from . import cut_cylinder, TowerTop, UnevenBlocks
import math
import random

class TowerTopGreebled(UnevenBlocks, TowerTop):
    def __init__(self):
        super().__init__()
        self.init_uneven_blocks()
        self.render_top:bool = True

    def make(self, parent=None):
        self.make_uneven_blocks(self.block_height, self.block_width, self.block_length)
        super().make(parent)
    
    def make_outside_blocks(self):
        return self.make_uneven_outside_blocks(
            self.top_diameter,
            self.height,
            self.block_height,
            self.block_length,
            self.block_width,
            self.even_ring_rotate,
            self.make_block_ring
        )
    
    def make_inside_blocks(self):
        return self.make_uneven_inside_blocks(
            self.diameter - 3.5,
            self.height,
            0,
            self.block_height,
            self.block_length,
            self.block_width,
            self.even_ring_rotate,
            self.make_block_ring
        )

    def make_top(self):
        if self.render_top:
            top = cq.Workplane("XY").cylinder(self.height,self.top_diameter/2)
            top = cut_cylinder(top, self.diameter, self.height - self.floor_height)
        else:
            self.base = cq.Workplane("XY")

        if self.battlements:
            self.top = (
                top
                .translate((0,0,self.height/2))
                .cut(self.battlements.translate((0,0,self.height-self.battlement_height/2)))
            )
        
        if self.render_blocks and self.top and self.block_battlements:
            self.make_blocks()    
            self.top = (
                self.top
                .cut(self.block_battlements.translate((0,0,self.height-self.battlement_height/2+.5)))
            )
        
        if self.render_floor_cut:
            self.make_floor_cut()
    
    def make_blocks(self):
        if self.render_outside_blocks and self.render_inside_blocks:
            blocks_combined_outside = self.make_outside_blocks()
            blocks_combined_inside = self.make_inside_blocks()
            base_out = (
                self.top
                .add(blocks_combined_outside) # type: ignore
            )

            base_in = self.base_in = (
                self.top
                .add(blocks_combined_inside) # type: ignore
            )

            self.top = base_out.union(base_in)
        elif self.render_outside_blocks:
            blocks_combined = self.make_outside_blocks()
            self.base = self.top.union(blocks_combined) # type: ignore

        elif self.render_inside_blocks:
            blocks_combined = self.make_inside_blocks()
            self.base = self.top.union(blocks_combined) # type: ignore
        else:
            raise Exception('unable to create blocks')
        

    def make_uneven_outside_blocks(
            self,
            diameter,
            height,
            block_height,
            block_length,
            block_width,
            even_ring_rotate,
            make_block_ring
    ):
        block_outer = self.make_uneven_core_block(0, block_height, block_length, block_width, outside=True)
        def add_block(loc:cq.Location) -> cq.Shape:
            chosen_block = random.choice(block_outer)
            return chosen_block.val().located(loc)
        
        ring_param = (diameter-2.5, add_block)

        mod_block_height = block_height + 1
        count = math.floor(height / mod_block_height)

        blocks_combined = (
            cq.Workplane()
        )

        for i in range(count):
            rotate_deg = 0
            
            if i % 2 == 0:
                rotate_deg = even_ring_rotate
                
            blocks_combined = (
                blocks_combined
                .add(
                    make_block_ring(
                        ring_param[0], 
                        ring_param[1]
                    )
                    .translate((0,0,(block_height/2)+1+(block_height+1)*i))
                    .rotate((0,0,1),(0,0,0),rotate_deg)
                )
            )

        return blocks_combined
        
    
    def make_uneven_inside_blocks(
            self,
            diameter, 
            height, 
            wall_width, 
            block_height, 
            block_length, 
            block_width, 
            even_ring_rotate,
            make_block_ring
        ):
        # inner
        block_inner = self.make_uneven_core_block(2, block_height, block_length, block_width, outside=False)
        
        def add_block_inner(loc:cq.Location) -> cq.Shape:
            chosen_block = random.choice(block_inner)
            return chosen_block.val().located(loc)
        
        ring_param_inner = (diameter-(wall_width*4)+2.5, add_block_inner)
        
        mod_block_height = block_height + 1
        count = math.floor(height / mod_block_height)
        print(f'make_uneven_inside_blocks {count=}, {mod_block_height=}, {block_height=}, {height=}')
        
        blocks_combined_inner = (
            cq.Workplane()
        )
        
        for i in range(count):
            rotate_deg = 0
            
            if i % 2 == 1:
                rotate_deg = even_ring_rotate
                
            blocks_combined_inner = (
                blocks_combined_inner
                .add(
                    make_block_ring(
                        ring_param_inner[0], 
                        ring_param_inner[1]
                    )
                    .translate((0,0,(block_height/2)+1+(block_height+1)*i))
                    .rotate((0,0,1),(0,0,0),rotate_deg)
                )
            )
            
        return blocks_combined_inner