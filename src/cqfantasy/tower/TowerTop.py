# Copyright 2024 James Adams
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import cadquery as cq
from cadqueryhelper import Base
from cqterrain.stairs.round import outline as make_outline
from . import cut_cylinder, TileGenerator
from .magnets import make_magnet, make_magnets
from . import RoundBlockGenerator, BaseSection

try:
    log #type:ignore
except NameError:
    log = print

class TowerTop(BaseSection):
    def __init__(self):
        super().__init__()
        
        # properties
        self.diameter:float = 130
        self.height:float = 30
        
        self.top_diameter:float = 150
        
        self.battlement_width:float = 20
        self.battlement_height:float = 17
        self.battlement_padding:float = 2.5
        self.battlement_count:int = 5

        self.render_floor_cut = True
        self.floor_cut_rotate = 270

        # Shapes
        self.top:cq.Workplane|None = None
        self.battlement:cq.Workplane|None = None
        self.battlements:cq.Workplane|None = None
        self.block_battlement:cq.Workplane|None = None
        self.block_battlements:cq.Workplane|None = None

        # Init values
        if self.bp_block_gen_outside:
            self.bp_block_gen_outside.block_length = 2.5
            self.bp_block_gen_outside.row_count = 3
            self.bp_block_gen_outside.margin = (.5,.5)
            self.bp_block_gen_outside.modulus_even = 1

        if self.bp_block_gen_inside:
            self.bp_block_gen_inside.block_length = 2.5
            self.bp_block_gen_inside.row_count = 3
            self.bp_block_gen_inside.margin = (.5,.5)
            self.bp_block_gen_inside.modulus_even = 1

    def make_battlement(self):
        log('make_battlement')
        battlement = cq.Workplane("XY").box(self.top_diameter+self.battlement_padding+2,self.battlement_width, self.battlement_height)
        self.battlement = battlement
        
        block_battlement = cq.Workplane("XY").box(self.top_diameter+self.battlement_padding+2+2,self.battlement_width-1.5, self.battlement_height-1)
        self.block_battlement = block_battlement
        
    def make_battlements(self):
        log('make_battlements')
        battlement_degrees = 360 / (self.battlement_count*2 )
        battlements = cq.Workplane("XY")
        block_battlements = cq.Workplane("XY")
        
        if self.battlement and self.block_battlement:
            for i in range(self.battlement_count):
                battlements = battlements.union(self.battlement.rotate((0,0,1),(0,0,0),battlement_degrees*i))
                block_battlements = block_battlements.union(self.block_battlement.rotate((0,0,1),(0,0,0),battlement_degrees*i))

        self.battlements = battlements
        self.block_battlements = block_battlements

    def make_top(self):
        log('make_top')
        top = cq.Workplane("XY").cylinder(self.height,self.top_diameter/2)

        if self.render_floor_tile:
            cut_cylinder_height = self.calculate_inner_height() + self.tile_height
        else:
            cut_cylinder_height = self.calculate_inner_height()
            
        top = cut_cylinder(top, self.diameter, cut_cylinder_height)
        self.top = top

    def make_blocks(self):
        log('make_blocks')
        if self.bp_block_gen_outside:
            log('make_blocks_outside')
            self.bp_block_gen_outside.top_diameter = self.top_diameter
            self.bp_block_gen_outside.base_diameter = self.top_diameter
            self.bp_block_gen_outside.height = self.height
            self.bp_block_gen_outside.make()
            
        if self.bp_block_gen_inside:
            log('make_blocks_inside')
            self.bp_block_gen_inside.top_diameter = self.diameter
            self.bp_block_gen_inside.base_diameter = self.diameter
            self.bp_block_gen_inside.height = self.height
            self.bp_block_gen_inside.make()
   
    def make(self, parent=None):
        log('make')
        super().make(parent)
        
        self.make_battlement()
        self.make_battlements()
        self.make_top()

        if self.render_magnets:
            self.make_magnets()

        if self.render_floor_tile and self.bp_tile_gen:
            self.bp_tile_gen.diameter = self.diameter
            self.bp_tile_gen.tile_height = self.tile_height
            self.bp_tile_gen.make()

        if self.render_blocks:
            self.make_blocks()
        
        if self.render_floor_cut:
            self.make_floor_cut()
        
    def build(self) -> cq.Workplane:
        log('build')
        super().build()
        
        scene = cq.Workplane("XY")

        if self.top:
            log('union top')
            scene = scene.add(self.top.translate((0,0,self.height/2)))
            
        if self.battlements:
            scene = (
                scene
                .cut(self.battlements.translate((0,0,self.height-self.battlement_height/2)))
            )

        if self.render_blocks and self.bp_block_gen_outside:
            log('build outside blocks')
            blocks_outside = self.bp_block_gen_outside.build()
            scene = scene.union(blocks_outside)

        if self.render_blocks and self.bp_block_gen_inside:
            log('build inside blocks')
            blocks_inside = self.bp_block_gen_inside.build()
            scene = scene.union(blocks_inside)

        if self.render_blocks and self.block_battlements:   
            scene = (
                scene
                .cut(self.block_battlements.translate((0,0,self.height-self.battlement_height/2+.5)))
            )

        if self.magnets:
            log('cut magnets')
            scene = (
                scene
                .cut(self.magnets.translate((0,0,self.magnet_height)))
            )

        if self.render_floor_tile and self.bp_tile_gen:
            log('union tiles')
            tiles = self.bp_tile_gen.build()
            offset_height = self.floor_height
            scene = scene.union(tiles.translate((0,0,offset_height-self.tile_height/2)))
            
        if self.floor_cut:
            log('cut floor_cut')
            scene = scene.cut(self.floor_cut)

        return scene