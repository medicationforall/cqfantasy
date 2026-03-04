import cadquery as cq
from cadqueryhelper import Base
from cadqueryhelper.shape import pyramid
from cqfantasy.tower import make_magnet

class PyramidRoof(Base):
    def __init__(self):
        super().__init__()
        #parameters
        self.length:float = 140
        self.width:float = 140
        self.height:float = 75
        
        self.overhang:tuple[float,float] = (0,0)
        self.wall_width:tuple[float,float,float] = (4,4,4)
        
        self.render_magnets:bool = True
        self.magnet_diameter:float = 3.4
        self.magnet_height:float = 2.2
        
        #shapes
        self.outline:cq.Workplane|None = None
        self.internal_cut:cq.Workplane|None  = None
        self.magnet:cq.Workplane|None = None
        self.magnets:cq.Workplane|None  = None
        self.roof:cq.Workplane|None = None
        
    def calculate_external_width(self):
        if self.overhang:
            return self.width + self.overhang[1]*2
        else: 
            return self.width
        
    def calculate_external_length(self):
        if self.overhang:
            return self.length + self.overhang[0]*2
        else: 
            return self.length
        
    def calculate_internal_width(self):
        if self.wall_width:
            return self.width - self.wall_width[1]*2
        else: 
            return self.width
        
    def calculate_internal_length(self):
        if self.wall_width:
            #print('calculate_internal_length')
            #print(self.overhang)
            return self.length - self.wall_width[0]*2
        else: 
            return self.length
        
    def calculate_internal_height(self):
        if self.wall_width:
            return self.height - self.wall_width[2]
        else: 
            return self.height

    def make_outline(self):
        #log('make pryamid outline')
        length = self.calculate_external_length()
        width = self.calculate_external_width()
        outline = pyramid(
            length = length, 
            width = width, 
            height = self.height
        )
        
        self.outline = outline
        
    def make_roof(self):
        #log('make pryamid make_roof')
        length = self.calculate_external_length()
        width = self.calculate_external_width()
        roof = pyramid(
            length = length, 
            width = width, 
            height = self.height
        )
        
        self.roof = roof
        
    def make_internal_cut(self):
        #log('make pryamid make_internal_cut')
        length = self.calculate_internal_length()
        width = self.calculate_internal_width()
        height = self.calculate_internal_height()
        roof = pyramid(
            length = length, 
            width = width, 
            height = height
        )
        
        self.internal_cut = roof
        
    def make_magnet(self):
        magnet = make_magnet(self.magnet_diameter, self.magnet_height)
        self.magnet = magnet
        
    def make_magnets(self):
        x_translate = self.calculate_internal_length()/2+self.magnet_diameter/2
        y_translate = self.calculate_internal_width()/2+self.magnet_diameter/2
        z_translate = self.magnet_height/2
    
        magnets = (
            cq.Workplane("XY")
            .union(self.magnet.translate((x_translate,y_translate,z_translate)))
            .union(self.magnet.translate((-x_translate,y_translate,z_translate)))
            .union(self.magnet.translate((x_translate,-y_translate,z_translate)))
            .union(self.magnet.translate((-x_translate,-y_translate,z_translate)))
        )
        self.magnets = magnets
        
    def make(self):
        super().make()
        self.make_outline()
        self.make_roof()
        self.make_internal_cut()
        self.make_magnet()
        self.make_magnets()
        
    def build_outline(self)->cq.Workplane:
        super().build()
        
        part = cq.Workplane("XY")
        
        if self.outline:
            part = part.add(self.outline)
        
        return part
        
    def build(self)->cq.Workplane:
        super().build()
        #log('build pyramid')
        
        part = cq.Workplane("XY")
        
        if self.roof:
            #log('add roof')
            part = part.add(self.roof)
            
        if self.internal_cut:
            #log('add roof')
            part = part.cut(self.internal_cut)
            
        if self.render_magnets and self.magnets:
            part = part.cut(self.magnets)
        
        return part