import cadquery as cq
from cadqueryhelper import Base
from cqterrain import support

class FireTop(Base):
    def __init__(self):
        super().__init__()
        #parameters
        self.length:float = 30
        self.width:float = 25
        self.height:float = 15
        
        self.top_height:float = 2
        self.top_length:float = 10
        self.top_width:float = 10 
        self.interior_padding:float = 2
        
        #shapes
        self.outline:cq.Workplane|None = None
        self.top:cq.Workplane|None = None
        
    def make_outline(self):
        length = self.length
        width = self.width
        height  = self.height
        
        outline = support(
            length = length, 
            width = width, 
            height = height, 
            inner_height = self.top_height, 
            inner_length = self.top_length, 
            inner_width = self.top_width, 
            top_offset = 0
        )
        
        self.outline = outline
        
    def make_top(self):
        length = self.length
        width = self.width
        height  = self.height
        
        top = support(
            length = length, 
            width = width, 
            height = height, 
            inner_height = self.top_height, 
            inner_length = self.top_length, 
            inner_width = self.top_width, 
            top_offset = 0
        )
        
        top = (
            top.faces("<Z")
            .shell(-self.interior_padding)
        )
        
        top = (
            top.faces(">Z")
            .edges()
            .toPending()
            .offset2D(-self.interior_padding)
            .extrude(-self.interior_padding,combine="cut")
        )
        #show_object(top)
        
        self.top = top
        
    def make(self):
        super().make()
        self.make_outline()
        self.make_top()
        
    def build_outline(self)->cq.Workplane:
        super().build()
        
        part = cq.Workplane("XY")
        
        if self.outline:
            part = part.add(self.outline.translate((0,0,self.height/2)))
        
        return part
        
    def build(self)->cq.Workplane:
        super().build()
        
        part = cq.Workplane("XY")

        if self.top:
            #part = part.add(self.top)
            part = part.add(self.top.translate((0,0,self.height/2)))
        
        return part