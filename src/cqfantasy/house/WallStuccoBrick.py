import cadquery as cq 
from cadqueryhelper import Base
from cqterrain.material import stacked_wave_form_map, stucco_brick_blocks
import math

class WallStuccoBrick(Base):
    def __init__(self):
        super().__init__()
        
        #parameters
        self.length:float = 100
        self.height:float = 50
        self.seed:str = 'test'
        self.cell_types:list[str] = [
            'block',
            'block', 
            'empty',
            'block'
        ]
        
        self.block_length:float = 8
        self.block_width:float = 5
        self.block_height:float = 3
        self.block_spacing:float = 2
        
        #shapes
        self.wall=None
        
    def make_wall(self):
        x_count = math.floor(self.length / (self.block_length+self.block_spacing) )
        y_count = math.floor(self.height / (self.block_height + self.block_spacing))
        
        brick_map = stacked_wave_form_map(
            (y_count, x_count),
            self.seed, 
            self.cell_types
        )
        
        self.wall = stucco_brick_blocks(
            brick_map, 
            self.block_length,
            self.block_height,
            self.block_width,
            self.block_spacing
        )
        
    def make(self, parent=None):
        super().make(parent)
        self.make_wall()
        
    def build(self)->cq.Workplane:
        super().build()
        
        scene = cq.Workplane("XY")
        
        if self.wall:
            scene = scene.add(self.wall.rotate((1,0,0),(0,0,0),-90))
            
        return scene