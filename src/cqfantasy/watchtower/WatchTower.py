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
        self.bp_body = bp_body
        
        bp_top = TowerTopGreebled()
        bp_top.render_floor_tiles = True
        bp_top.render_inside_walls = True
        bp_top.render_outside_walls = True
        bp_top.render_windows = True
        self.bp_top = bp_top
        
        self.bp_roof = PyramidRoofShingle()
        self.bp_roof.overhang = (10,10)

        #shapes
        self.outline:cq.Workplane|None = None
        
    def make(self):
        super().make()
        if self.bp_base:
            self.bp_base.make()
            
        if self.bp_body:
            self.bp_body.make()
        
        if self.bp_top:
            self.bp_top.make()
            
        if self.bp_roof:
            self.bp_roof.make()

        
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
            tower_top = self.bp_top.build()
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