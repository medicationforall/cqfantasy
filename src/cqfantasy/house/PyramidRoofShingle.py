import cadquery as cq
from .PyramidRoof import PyramidRoof
from cqfantasy.tower import make_magnet
from cqterrain.roof import angle, tiles_alt

class PyramidRoofShingle(PyramidRoof):
    def __init__(self):
        super().__init__()
        #parameters
        self.length:float = 115
        self.width:float = 115
        self.height:float = 75
        
        self.render_shingles:bool = True
        self.tile_length:float = 10
        self.tile_width:float = 10
        self.tile_height:float = 0.8
        self.tile_rotation:float = 4
        self.tile_push:float = 2
        
        self.shingle_debug:bool = False
        
        #shapes
        self.shingle = None
        self.shingles = None
        
    def make_shingle(self):

        tile = (
            cq.Workplane("XY")
            .box(self.tile_length,self.tile_width,self.tile_height)
            .rotate((0,1,0),(0,0,0),self.tile_rotation)
        )
        
        self.shingle = tile
        
    def make_shingles(self):
        if self.shingle and self.roof:
            
            length = self.calculate_external_length()/2
            width = self.width
            height = self.height
            
            #hyp = math.hypot(x, height)
            
            t_roof = self.roof.translate((0,0,-self.height/2))
            
            face_x = t_roof.faces(">X")
            angle_x = angle(length, height)

            self.shingles = tiles_alt(
                self.shingle, 
                face_x, 
                length,
                width,
                height, 
                self.tile_length, 
                self.tile_width, 
                angle_x,  
                odd_col_push=[self.tile_push,0],
                debug = self.shingle_debug,
                intersect = True
            ).translate((0,0,self.height/2))
            
    def make(self):
        super().make()
        if self.render_shingles:
            self.make_shingle()
            self.make_shingles()
        
    def build(self):
        part = super().build()
        
        if self.render_shingles and self.shingles:
            sides = (
                cq.Workplane()
                .add(self.shingles)
                .add(self.shingles.rotate((0,0,1),(0,0,),90))
                .add(self.shingles.rotate((0,0,1),(0,0,),180))
                .add(self.shingles.rotate((0,0,1),(0,0,),270))
            )
            part = part.union(sides)
            
            #not sure which one is more optimal at the moment
            #part = (
            #    part
            #    .union(self.shingles)
            #    .union(self.shingles.rotate((0,0,1),(0,0,),90))
            #    .union(self.shingles.rotate((0,0,1),(0,0,),180))
            #    .union(self.shingles.rotate((0,0,1),(0,0,),270))
            #)
            
        
        return part