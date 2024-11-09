import cadquery as cq
from . import cut_cylinder, TowerMid, UnevenBlocks

class TowerMidGreebled(UnevenBlocks, TowerMid):
    def __init__(self):
        super().__init__()
        self.init_uneven_blocks()
        self.render_mid:bool = True

    def make(self, parent=None):
        self.make_uneven_blocks(self.block_height, self.block_width, self.block_length)
        super().make(parent)
    
    def make_outside_blocks(self):
        return self.make_uneven_outside_blocks(
            self.diameter,
            self.height,
            self.block_height,
            self.block_length,
            self.block_width,
            self.even_ring_rotate,
            self.make_block_ring
        )
    
    def make_inside_blocks(self):
        return self.make_uneven_inside_blocks(
            self.diameter,
            self.height,
            self.wall_width,
            self.block_height,
            self.block_length,
            self.block_width,
            self.even_ring_rotate,
            self.make_block_ring
        )
    
    def make_mid(self):
        if self.render_mid:
            mid = cq.Workplane("XY").cylinder(self.height, self.diameter/2)

            if self.render_floor_tile:
                cut_cylinder_height = self.calculate_inner_height() + self.tile_height
            else:
                cut_cylinder_height = self.calculate_inner_height()
                
            mid = cut_cylinder(mid, self.diameter - (self.wall_width*4), cut_cylinder_height)
            self.mid = mid.translate((0,0,self.height/2))
        else:
            self.base = cq.Workplane("XY")
        
        if self.render_blocks:
            self.make_blocks()
            
        if self.render_stairs:
            self.make_stairs()
            self.make_floor_cut()

    
    def make_blocks(self):
        if self.render_outside_blocks and self.render_inside_blocks:
            blocks_combined_outside = self.make_outside_blocks()
            blocks_combined_inside = self.make_inside_blocks()
            base_out = (
                self.mid
                .add(blocks_combined_outside) # type: ignore
            )

            base_in = self.base_in = (
                self.mid
                .add(blocks_combined_inside) # type: ignore
            )

            self.mid = base_out.union(base_in)
        elif self.render_outside_blocks:
            blocks_combined = self.make_outside_blocks()
            self.base = self.mid.union(blocks_combined) # type: ignore

        elif self.render_inside_blocks:
            blocks_combined = self.make_inside_blocks()
            self.base = self.mid.union(blocks_combined) # type: ignore

        else:
            raise Exception('unable to create blocks')
    
