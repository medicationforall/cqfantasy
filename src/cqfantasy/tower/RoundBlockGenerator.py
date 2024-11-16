import cadquery as cq
from cadqueryhelper import Base
import math

class RoundBlockGenerator(Base):
    def __init__(self):
        super().__init__()
        # parameters
        self.top_diameter:float = 100
        self.base_diameter:float|None = 150
        self.height:float = 100
        
        self.block_length:float = 5

        self.row_count:int = 10
        self.margin:int|tuple = 1
        self.render_blocks:bool = True
        
        self.block_ring_count:int = 30
        self.even_ring_rotate:float = 6
        self.modulus_even:int = 1 # 0 or 1
        
        #shapes
        self.cone:cq.Workplane|None = None
        self.block:cq.Workplane|None = None
        self.blocks:cq.Workplane|None = None

    def calculate_largest_diameter(self):
        diameter = self.top_diameter
        if self.base_diameter is not None and self.base_diameter > self.top_diameter:
            diameter = self.base_diameter
        return diameter
               

    def calculate_block_height(self):
            return self.height / self.row_count
    
            
    def calculate_block_margin_height(self):
        if isinstance(self.margin, tuple):
            margin = self.margin[0]
        else:
            margin = self.margin

        return (self.height / self.row_count) - margin * 2
            
    def calculate_block_width(self, radius):
        circumference = radius * 2 * math.pi
        block_width = circumference / self.block_ring_count
        return block_width
        
    def calculate_block_margin_width(self, radius):
        if isinstance(self.margin, tuple):
            margin = self.margin[1]
        else:
            margin = self.margin

        block_width = self.calculate_block_width(radius)
        return block_width - margin * 2
        
    def make_block(self):
        # gather largest diameter
        diameter = self.top_diameter
        if self.base_diameter is not None and self.top_diameter < diameter:
            diameter = self.base_diameter
        
        block_margin_width = self.calculate_block_margin_width(diameter/2)
        block_margin_height = self.calculate_block_margin_height()

        self.block  = cq.Workplane("XY").box(
            self.block_length,
            block_margin_width,
            block_margin_height
        )

    def get_block(self) -> cq.Workplane:
        if self.block:
            return self.block
        else:
            raise Exception("Could not resolve block")
        
    def resolve_add_block(self, radius):
        block_margin_width = self.calculate_block_margin_width(radius)
        block_margin_height = self.calculate_block_margin_height()

        i_block = cq.Workplane("XY").box(self.block_length, block_margin_width, block_margin_height)
        c_block = self.get_block().intersect(i_block)
        
        def add_block(loc:cq.Location) -> cq.Shape:
            return c_block.val().located(loc) #type:ignore
        
        return add_block
        
    def make_block_ring(self, radius):
        block_margin_width = self.calculate_block_margin_width(radius)
        block_margin_height = self.calculate_block_margin_height()

        i_block = cq.Workplane("XY").box(self.block_length, block_margin_width, block_margin_height)
        c_block = self.get_block().intersect(i_block)
        
        def add_block(loc:cq.Location) -> cq.Shape:
            return c_block.val().located(loc) #type:ignore
        
        add_block = self.resolve_add_block(radius)
        
        blocks = (
            cq.Workplane("XY")
            .polarArray(
                radius = radius, 
                startAngle = 0, 
                angle = 360, 
                count = self.block_ring_count,
                fill = True,
                rotate = True
            )
            .eachpoint(callback = add_block)
        )
        
        ring = cq.Workplane("XY").union(blocks)
        return ring
        
    def make_blocks(self):
        blocks = cq.Workplane("XY")
        height = self.height
        block_height = self.calculate_block_height()
        rows = math.floor(height/block_height) 

        if self.base_diameter:
            row_rate = (self.base_diameter - self.top_diameter) / rows
        else:
            row_rate = 0

        for i in range(rows):
            if self.base_diameter:
                radius = self.base_diameter/2-(i*row_rate)/2-row_rate/4
            else:
                radius = self.top_diameter/2-(i*row_rate)/2-row_rate/4

            ring = self.make_block_ring(radius)
            
            rotate_degrees = 0
            #ring_rotation
            if i % 2 == self.modulus_even:
                rotate_degrees = (360/self.block_ring_count)/2
            
            blocks = (
                blocks
                .union(
                    ring
                    .translate((
                        0,
                        0,
                        block_height/2+block_height*i)
                    )
                    .rotate((0,0,1),(0,0,0),rotate_degrees)
                )
            )
            
        self.blocks = blocks
    
    def make(self, parent=None):
        super().make(parent)
        self.make_block()
        self.make_blocks()
        
    def build(self):
        super().build()
        scene = (
            cq.Workplane("XY")
        )
        
        if self.blocks:
            scene = scene.add(self.blocks)
        return scene