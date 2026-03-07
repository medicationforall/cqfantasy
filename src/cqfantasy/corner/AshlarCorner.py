import cadquery as cq
from cadqueryhelper import Base
import math

class AshlarCorner(Base):
    def __init__(self):
        super().__init__()
        #parameter
        self.length:float = 30
        self.width:float = 30
        self.height:float = 75
        self.stone_height = 5
        self.chamfer:float = 1
        self.corner_cut_length:float|None = 3
        self.corner_cut_width:float|None = 3
        
        #shapes
        self.outline:cq.Workplane|None = None
        self.small_stone = None
        self.large_stone = None
        self.stones = None
        self.mirror_stones = None
        self.corner_cut = None
        
        
    def make_outline(self):
        outline = cq.Workplane("XY").box(
            self.length,
            self.width,
            self.height
        )
        
        self.outline = outline
        
    def calculate_stone_count(self):
        return math.floor(self.height / self.stone_height)
    
    def make_small_stone(self):
        length = self.length / 2
        width = self.width / 2
        height = self.stone_height
        small_stone = (
            cq.Workplane("XY")
            .box(length,width,height)
            .translate((length/2,width/2,0))
        )
        
        if self.chamfer:
            small_stone = small_stone.chamfer(self.chamfer)
            
        self.small_stone = small_stone
    
    def make_large_stone(self):
        length = self.length
        width = self.width
        height = self.stone_height
        large_stone = cq.Workplane("XY").box(length,width,height)
        
        if self.chamfer:
            large_stone = large_stone.chamfer(self.chamfer)
            
        self.large_stone = large_stone
        
    def make_corner_cut(self):
        # cut stone
        length = self.length / 2
        width = self.width / 2
        
        if self.corner_cut_length:
            length = self.length - self.corner_cut_length
        
        if self.corner_cut_width:
            width = self.width - self.corner_cut_width
        
        height = self.height
        x_translate = self.length/2 - length/2
        y_translate = self.width/2 - width/2
        
        corner_cut = (
            cq.Workplane("XY")
            .box(length,width,height)
            .translate((-x_translate,-y_translate,self.height/2))
        )
        
        self.corner_cut = corner_cut
    
    def make_stones(self):
        stones = cq.Workplane("XY")
        stone_count = self.calculate_stone_count()
        
        for i in range(stone_count):
            if i % 2 == 0:
                stones = stones.add(self.large_stone.translate((0,0,i * self.stone_height)))
            else:
                stones = stones.add(self.small_stone.translate((0,0,i * self.stone_height)))
            
        self.stones = stones
        
    def make_mirror_stones(self):
        stones = cq.Workplane("XY")
        stone_count = self.calculate_stone_count()
        small_length = self.length / 2
        
        for i in range(stone_count):
            if i % 2 == 0:
                stones = stones.add(self.large_stone.translate((0,0,i * self.stone_height)))
            else:
                stones = stones.add(self.small_stone.translate((-small_length,0,i * self.stone_height)))
            
        self.mirror_stones = stones
        
    def make(self):
        super().make()
        self.make_outline()
        self.make_small_stone()
        self.make_large_stone()
        self.make_stones()
        self.make_mirror_stones()
        self.make_corner_cut()
        
    def build_outline(self)->cq.Workplane:
        super().build()
        
        part = cq.Workplane("XY")
        
        if self.outline:
            part = part.add(self.outline.translate((0,0,self.height/2)))
        
        return part
        
    def build(self)->cq.Workplane:
        super().build()
        
        part = cq.Workplane("XY")
        
        if self.stones:
            part = part.add(self.stones.translate((0,0,self.stone_height/2)))
            
        if self.corner_cut:
            part = part.cut(self.corner_cut)
        
        return part.rotate((0,0,1),(0,0,0),180)
    
    def build_mirror(self)->cq.Workplane:
        super().build()
        
        part = cq.Workplane("XY")
        
        if self.stones:
            part = part.add(self.mirror_stones.translate((0,0,self.stone_height/2)))
            
        if self.corner_cut:
            part = part.cut(self.corner_cut.translate((self.corner_cut_length,0,0)))
        
        return part.rotate((0,0,1),(0,0,0),180)