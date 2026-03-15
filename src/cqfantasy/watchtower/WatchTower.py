import cadquery as cq
from cadqueryhelper import Base
from . import TowerBase, TowerBodyGreebled, TowerTopGreebled
from ..house import PyramidRoofShingle

class WatchTower(Base):
    def __init__(self):
        super().__init__()
        
        #blueprints
        self.bp_base = TowerBase()
        
        bp_body = TowerBodyGreebled()
        bp_body.render_doors = True
        bp_body.render_windows = True
        bp_body.render_outside_walls = True
        bp_body.render_inside_walls = True
        bp_body.render_outside_corners = True
        bp_body.render_floor_tiles = True
        self.bp_body = bp_body
        
        bp_top = TowerTopGreebled()
        bp_top.render_floor_tiles = True
        bp_top.render_inside_walls = True
        bp_top.render_outside_walls = True
        bp_top.render_windows = True
        bp_top.render_roof = False
        self.bp_top = bp_top
        
        self.bp_roof = PyramidRoofShingle()
        self.bp_roof.overhang = (10,10)

        #shapes
        self.outline:cq.Workplane|None = None
        self.top_magnets:cq.Workplane|None = None
        self.ladder_cut:cq.Workplane|None  = None
        
    def calculate_top_floor_height(self):
        if (
            self.bp_top and
            self.bp_top.bp_house and
            self.bp_top.bp_house.bp_body and 
            hasattr(self.bp_top.bp_house.bp_body,'calculate_floor_height')
        ):
            height = self.bp_top.bp_house.bp_body.calculate_floor_height()
        else:
            height = 10
        
        return height
    
    def make_ladder_cut(self):
        height = self.calculate_top_floor_height() + 2
        
        if self.bp_body and self.bp_body.calculate_ladder_translate_y:
            translate_y = self.bp_body.calculate_ladder_translate_y() - 25/2
        else:
            translate_y = 0
            
        ladder_cut = cq.Workplane("XY").box(25,25,height).translate((0,translate_y,height/2))
        self.ladder_cut = ladder_cut
        
    def make_top_magnets(self):
        if (
            self.bp_body and
            self.bp_body.bp_tower and 
            self.bp_body.bp_tower.bp_body and 
            hasattr(self.bp_body.bp_tower.bp_body,'build_magnets')
        ):
            log('found build magnets')
            magnet_height = self.bp_body.bp_tower.bp_body.magnet_height
            magnets = self.bp_body.bp_tower.bp_body.build_magnets()
            self.top_magnets = magnets.translate((0,0,magnet_height))
        
    def make(self):
        super().make()
        if self.bp_base:
            self.bp_base.make()
            
        if self.bp_body:
            self.bp_body.make()
        
        if self.bp_top:
            self.bp_top.make()
            
        if self.bp_top and self.bp_body:
            self.make_top_magnets()
            self.make_ladder_cut()
            
        if self.bp_roof:
            self.bp_roof.make()
            
    def build_tower_top(self):
        part = cq.Workplane("XY")
        if self.bp_top:
            tower_top = self.bp_top.build()
            z_translate = self.bp_base.height + self.bp_body.height
            part = part.union(tower_top.translate((0,0,0)))
            
            if self.top_magnets:
                z_translate = self.bp_body.height/2
                part = part.cut(self.top_magnets.translate((0,0,-z_translate)))
                
            if self.ladder_cut:
                part = part.cut(self.ladder_cut)

        return part

        
    def build(self)->cq.Workplane:
        super().build()
        
        part = cq.Workplane("XY")
        
        if self.bp_base:
            tower_base = self.bp_base.build()
            part = part.add(tower_base)
            
        if self.bp_body:
            tower_body = self.bp_body.build()
            z_translate = self.bp_base.height
            part = part.add(tower_body.translate((0,0,z_translate)))
            
        if self.bp_top:
            tower_top = self.build_tower_top()
            z_translate = self.bp_base.height + self.bp_body.height
            part = part.add(tower_top.translate((0,0,z_translate)))
            
        if self.bp_roof:
            tower_roof = self.bp_roof.build()
            z_translate = self.bp_base.height + self.bp_body.height + self.bp_top.height
            part = part.add(tower_roof.translate((0,0,z_translate)))
        
        return part
    
    def build_cut(self):
        length = 100
        width = 100
        height = 300
        cut_tower = cq.Workplane("XY").box(length, width,height)
        cut_tower = cut_tower.translate((length/2,width/2,height/2))
        return cut_tower
    
    def build_plate(self):
        part = cq.Workplane("XY")
        spacing = 10
        
        if self.bp_base:
            tower_base = self.bp_base.build()
            length = self.bp_base.length
            width = self.bp_base.width
            
            part = part.add(tower_base.translate((-length/2 - spacing,width/2 +spacing,0)))
            
        if self.bp_body:
            tower_body = self.bp_body.build()
            length = self.bp_body.length
            width = self.bp_body.width
            z_translate = 0
            part = part.add(tower_body.translate((length/2 + spacing, width/2 + spacing,z_translate)))

        if self.bp_top:
            tower_top = self.build_tower_top()
            length = self.bp_top.length
            width = self.bp_top.width
            z_translate = 0
            part = part.add(tower_top.translate((-length/2 - spacing,-width/2 - spacing, z_translate)))
            
            
        if self.bp_roof:
            tower_roof = self.bp_roof.build()
            length = self.bp_roof.length
            width = self.bp_roof.width
            z_translate = 0
            part = part.add(tower_roof.translate((length/2 + spacing + 10, -width/2 - spacing - 10, z_translate)))

        return part