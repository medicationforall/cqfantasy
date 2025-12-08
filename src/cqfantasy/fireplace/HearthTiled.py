import cadquery as cq
from cadqueryhelper import Base

class HearthTiled(Base):
    def __init__(self):
        super().__init__()
        #parameters
        self.length:float = 35
        self.width:float = 35
        self.height:float = 3

        self.tile_height:float = 1.5
        self.rows:int = 4
        self.columns:int = 4
        self.spacing:float = .5
        self.tile_padding:float = 2

        #shapes
        self.outline:cq.Workplane|None = None
        self.hearth:cq.Workplane|None = None
        self.tiles:cq.Workplane|None = None
        
    def make_outline(self):
        outline = cq.Workplane("XY").box(
            self.length,
            self.width,
            self.height
        )
        
        self.outline = outline
        
    def make_hearth(self):
        height = self.height - self.tile_height
        hearth = cq.Workplane("XY").box(
            self.length,
            self.width,
            height
        )
        
        self.hearth = hearth
        
    def make_tiles(self):
        
        x_spacing = (self.length+self.tile_padding)/self.columns
        y_spacing = (self.width+self.tile_padding)/self.rows
        length = x_spacing - self.spacing
        width = y_spacing - self.spacing
        height = self.tile_height
        tile = cq.Workplane("XY").box(length, width, height)
        
        def add_tile(loc:cq.Location) ->cq.Shape:
            return tile.val().located(loc) #type:ignore
        
        tiles = (
            cq.Workplane("XY")
            .rarray(
                xSpacing = x_spacing, 
                ySpacing = y_spacing,
                xCount = self.columns, 
                yCount= self.rows, 
                center = True)
            .eachpoint(add_tile)
        )
        
        if self.outline:
            self.tiles = tiles.intersect(self.outline)
        
    def make(self):
        super().make()
        self.make_outline()
        self.make_hearth()
        self.make_tiles()
        
    def build_outline(self)->cq.Workplane:
        super().build()
        
        part = cq.Workplane("XY")
        
        if self.outline:
            part = part.add(self.outline.translate((0,0,self.height/2)))
        
        return part
        
    def build(self)->cq.Workplane:
        super().build()
        
        part = cq.Workplane("XY")
        
        if self.hearth:
            height = self.height - self.tile_height
            part = part.add(self.hearth.translate((0,0,height/2)))
            
        if self.tiles:
            height = self.height - self.tile_height
            part = part.union(self.tiles.translate((0,0,self.tile_height/2+height)))
        
        return part