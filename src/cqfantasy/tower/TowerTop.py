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
from . import cut_cylinder
from .magnets import make_magnet, make_magnets
import math


class TowerTop(Base):
    def __init__(self):
        super().__init__()
        
        # properties
        self.diameter:float = 130
        self.height:float = 30
        
        self.wall_width:float = 4
        self.floor_height:float = 4
        self.top_diameter:float = 150
        
        self.block_length:float = 5
        self.block_width:float = 14
        self.block_height:float = 8.5
        
        self.block_ring_count:int = 30
        self.even_ring_rotate:float = 6
        
        self.render_blocks:bool = True
        self.render_floor_cut:bool = True
        
        self.battlement_width:float = 20
        self.battlement_height:float = 17
        self.battlement_padding:float = 2.5
        self.battlement_count:int = 5

        self.render_magnets:bool = True
        self.magnet_diameter:float = 3.4
        self.magnet_height:float = 2.2
        self.magnet_count:int = 4
        
        # Shapes
        self.top:cq.Workplane|None = None
        self.floor_cut:cq.Workplane|None = None
        self.battlement:cq.Workplane|None = None
        self.battlements:cq.Workplane|None = None
        self.block_battlement:cq.Workplane|None = None
        self.block_battlements:cq.Workplane|None = None
        
    def make_battlement(self):
        battlement = cq.Workplane("XY").box(self.top_diameter+self.battlement_padding+2,self.battlement_width, self.battlement_height)
        self.battlement = battlement
        
        block_battlement = cq.Workplane("XY").box(self.top_diameter+self.battlement_padding+2+2,self.battlement_width-1.5, self.battlement_height-1)
        self.block_battlement = block_battlement
        
    def make_battlements(self):
        #log(f'make_battlements')
        battlement_degrees = 360 / (self.battlement_count*2 )
        battlements = cq.Workplane("XY")
        block_battlements = cq.Workplane("XY")
        
        if self.battlement and self.block_battlement:
            for i in range(self.battlement_count):
                battlements = battlements.union(self.battlement.rotate((0,0,1),(0,0,0),battlement_degrees*i))
                block_battlements = block_battlements.union(self.block_battlement.rotate((0,0,1),(0,0,0),battlement_degrees*i))

        #log(f'battlements {battlements}')
        self.battlements = battlements
        self.block_battlements = block_battlements

    def make_magnets(self):
        magnet = make_magnet(self.magnet_diameter, self.magnet_height)
        self.magnets = (
            make_magnets(magnet, self.magnet_count, self.diameter - self.wall_width*2)
            .translate((0,0,-self.magnet_height/2))
        )
   
    def make(self, parent=None):
        super().make(parent)
        
        self.make_battlement()
        self.make_battlements()
        self.make_top()

        if self.render_magnets:
            self.make_magnets()
        
    def make_block_ring(self, diameter, add_block):
        blocks = (
            cq.Workplane("XY")
            .polarArray(
                radius = diameter / 2, 
                startAngle = 0, 
                angle = 360, 
                count = self.block_ring_count,
                fill = True,
                rotate = True
            )
            .eachpoint(callback = add_block)
        )
        
        return blocks
    
    def make_core_block(self,margin, top_height=None):
        if not top_height:
            #log('default top height')
            top_height = self.block_height
            
        #log(f'make_core_block top_height {top_height}')
            
        return cq.Workplane("XY").box(
            self.block_length,
            self.block_width-margin,
            top_height
        )
        
    def make_top(self):
        top = cq.Workplane("XY").cylinder(self.height,self.top_diameter/2)
        top = cut_cylinder(top, self.diameter, self.height - self.floor_height)

        if self.battlements:
            self.top = (
                top
                .translate((0,0,self.height/2))
                .cut(self.battlements.translate((0,0,self.height-self.battlement_height/2)))
            )
        
        if self.render_blocks and self.top and self.block_battlements:
            self.make_blocks()    
            self.top = (
                self.top
                .cut(self.block_battlements.translate((0,0,self.height-self.battlement_height/2+.5)))
            )
        
        if self.render_floor_cut:
            self.make_floor_cut()
            
    def make_blocks(self):
        block = self.make_core_block(0, self.block_height)
        block_inner = self.make_core_block(2, self.block_height)
        
        def add_block(loc:cq.Location) -> cq.Shape:
            return block.val().located(loc) #type:ignore
        
        def add_block_inner(loc:cq.Location) -> cq.Shape:
            return block_inner.val().located(loc) #type:ignore
        
        ring_param = (self.top_diameter-2.5, add_block)
        ring_param_inner = (self.diameter+1, add_block_inner)
        
        block_height = self.block_height + 1
        count = math.floor(self.height / block_height)
        
        blocks_combined = (
            cq.Workplane()
        )
        
        for i in range(count):
            rotate_deg = 0
            
            if i % 2 == 1:
                rotate_deg = self.even_ring_rotate
                
            blocks_combined = (
                blocks_combined
                .union(
                    self.make_block_ring(
                        ring_param[0], 
                        ring_param[1]
                    )
                    .translate((0,0,(self.block_height/2)+1+(self.block_height+1)*i))
                    .rotate((0,0,1),(0,0,0),rotate_deg)
                )
            )
            
        blocks_combined_inner = (
            cq.Workplane()
        )
        
        for i in range(count):
            rotate_deg = 0
            
            if i % 2 == 1:
                rotate_deg = self.even_ring_rotate
                
            blocks_combined_inner = (
                blocks_combined_inner
                .union(
                    self.make_block_ring(
                        ring_param_inner[0], 
                        ring_param_inner[1]
                    )
                    .translate((0,0,(self.block_height/2)+1+(self.block_height+1)*i))
                    .rotate((0,0,1),(0,0,0),rotate_deg)
                )
            )

        if self.top:    
            self.top = (
                self.top
                .union(blocks_combined)
                .union(blocks_combined_inner)
            )
            
    def make_floor_cut(self):
        diameter = self.diameter - self.wall_width*4
        inner_diameter = diameter - 60
        
        outline = make_outline(
            height = self.floor_height,
            inner_diameter = inner_diameter,
            diameter = diameter,
            rotate = 50
        ).rotate((0,0,1),(0,0,0),270)
        
        self.floor_cut = outline
        
    def build(self):
        super().build()
        
        scene = (
            cq.Workplane("XY")
            ##.add(self.top)
            ##.cut(self.floor_cut)
            #.add(self.battlements.translate((0,0,self.height-self.battlement_height/2)))
            #.add(self.block_battlements.translate((0,0,self.height-self.battlement_height/2+1)))
        )

        if self.top:
            scene = scene.add(self.top)

        if self.floor_cut:
            scene = scene.cut(self.floor_cut)

        if self.magnets:
            scene = (
                scene
                .cut(self.magnets.translate((0,0,self.magnet_height)))
            )

        return scene