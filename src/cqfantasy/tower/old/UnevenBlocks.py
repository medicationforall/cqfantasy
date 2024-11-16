import cadquery as cq
import random
import math
from cqterrain.material import uneven_centered_blocks
from .. import cut_cylinder, TowerMid

class UnevenBlocks():
    def init_uneven_blocks(self):
        print('initialize uneven blocks')

        # parameters
        self.uneven_block_depth:float = 1
        self.seed:str = 'test4'
        self.render_outside_blocks:bool = True
        self.render_inside_blocks:bool = True

        # shapes
        self.uneven_blocks = None

    def make_uneven_blocks(self, block_height, block_width, block_length):
        blocks = uneven_centered_blocks(
            tile_length = block_height,
            tile_width = block_width,
            tile_height= block_length,
            rows = 6, 
            columns = 6, 
            margin = 2,
            uneven_depth = self.uneven_block_depth,
            seed=self.seed,
            segments = 10,
            peak_count = (14,15)
        )
        
        self.uneven_blocks = blocks

    def make_uneven_core_block(self,margin, block_height, block_length, block_width, top_height=None, outside=True, ):
        if not top_height:
            top_height = block_height
            
        core_block = cq.Workplane("XY").box(
            block_length,
            block_width-margin,
            top_height
        )
        
        uneven_core_blocks = []
        
        if self.uneven_blocks:
            for b in self.uneven_blocks:
                if outside:
                    b = b.rotate((0,1,0),(0,0,0),-90).intersect(core_block)
                else:
                    b = b.rotate((0,1,0),(0,0,0),90).intersect(core_block)
                uneven_core_blocks.append(b)
            
        return uneven_core_blocks
    
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
        block_outer = self.make_uneven_core_block(1.5, block_height, block_length, block_width, outside=True)
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
        block_inner = self.make_uneven_core_block(3, block_height, block_length, block_width, outside=False)
        
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