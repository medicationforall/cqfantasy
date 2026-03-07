# Copyright 2025 James Adams
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
from . import Body, TileGenerator
from ..tower import make_magnet

class BodyGreebled(Body):
    def __init__(self):
        super().__init__()
        
        self.render_floor_tiles:bool = True
        self.render_outside_walls:bool = True
        self.render_inside_walls:bool = True
        self.render_outside_corners:bool = True
        self.render_magnets:bool = True
        self.floor_height:float = 10
        self.tile_height:float = 2.5

        self.magnet_diameter:float = 3.4
        self.magnet_height:float = 2.2
        
        #shapes
        self.outside_walls = None
        self.inside_walls = None
        self.magnet = None
        
        #blueprints
        self.bp_outside_walls:list[Base] = []
        self.bp_inside_walls:list[Base] = []
        self.bp_tile_generator:TileGenerator|None = TileGenerator()
        #self.bp_outside_corners:Base|list[Base]|None = None
        self.bp_outside_corners:Base|None = None
        
    def calculate_internal_height(self):
        internal_height = self.height - self.floor_height - self.tile_height
        #log(f'calculate_internal_height {internal_height}')
        return internal_height
    
    def calculate_floor_height(self):
        return self.floor_height + self.tile_height
    
    def make_outside_walls(self):
        if self.bp_outside_walls:
            self.outside_walls = []
            for index, bp_wall in enumerate(self.bp_outside_walls):
                #log(f'test outside {index}, {index % 2}')
                if index % 2  == 0:
                    #log('length wall')
                    bp_wall.length = self.length
                else:
                    #log('width wall')
                    bp_wall.length = self.width
                    
                bp_wall.height = self.height
                bp_wall.make()
                
                #log('build_wall')
                wall = bp_wall.build()
                self.outside_walls.append(wall)
                
    def make_inside_walls(self):
        if self.bp_inside_walls:
            self.inside_walls = []
            for index, bp_wall in enumerate(self.bp_inside_walls):
                if index % 2  == 0:
                    #log('length wall')
                    bp_wall.length = self.calculate_internal_length()
                else:
                    #log('width wall')
                    bp_wall.length = self.calculate_internal_width()

                bp_wall.height = self.calculate_internal_height()
                #log(f'internal wall height {bp_wall.height}')
                bp_wall.make()
                
                #log('build_wall')
                wall = bp_wall.build()
                
                self.inside_walls.append(wall)
                
    def make_floor_tiles(self):
        if self.bp_tile_generator:
            self.bp_tile_generator.length = self.length - self.wall_width*2
            self.bp_tile_generator.width = self.width - self.wall_width*2
            self.bp_tile_generator.tile_height = self.tile_height
            self.bp_tile_generator.make()

    def make_magnet(self):
        magnet = make_magnet(self.magnet_diameter, self.magnet_height)
        self.magnet = magnet
        
    def make_outside_corners(self):
        #log('make_outside_corners')
        
        if self.bp_outside_corners:
            #if isinstance(self.bp_outside_corners, list):
            #    for bp_corner in self.bp_outside_corners:
            #        bp_corner.make()
            #else:
            self.bp_outside_corners.height = self.height
            self.bp_outside_corners.make()
                
        
    def make(self, parent=None):
        super().make(parent)
        #log('make')
        if self.render_outside_walls:
            self.make_outside_walls()

        if self.render_inside_walls:
            self.make_inside_walls()
        
        if self.render_floor_tiles:
            self.make_floor_tiles()

        if self.render_magnets:
            self.make_magnet()
            
        if self.render_outside_corners and self.bp_outside_corners:
            self.make_outside_corners()

    def build_inside_walls(self):
        scene = cq.Workplane("XY")

        z_translate = self.floor_height
            
        if self.render_floor_tiles and self.bp_tile_generator:
            z_translate += self.tile_height

        for index, wall in enumerate(self.inside_walls):
            wall_width = self.bp_inside_walls[index].width

            if type(wall_width) is tuple:
                wall_width = wall_width[1]

            if index == 0:
                length_translate = self.width/2-self.wall_width-wall_width//2
                scene = scene.add(wall.rotate((0,0,1),(0,0,0),180).translate((0,-length_translate,z_translate/2)))
            elif index == 1:
                width_translate = self.length/2-self.wall_width-wall_width/2
                scene = scene.add(wall.rotate((0,0,1),(0,0,0),-90).translate((-width_translate,0,z_translate/2)))
            elif index == 2:
                length_translate = self.width/2-self.wall_width-wall_width/2
                scene = scene.add(wall.rotate((0,0,1),(0,0,0),0).translate((0,length_translate,z_translate/2)))
            elif index == 3:
                width_translate = self.length/2-self.wall_width-wall_width/2
                scene = scene.add(wall.rotate((0,0,1),(0,0,0),90).translate((width_translate,0,z_translate/2)))

        return scene

    def build_outside_walls(self):
        scene = cq.Workplane("XY")

        for index, wall in enumerate(self.outside_walls):
            #try:
            wall_width = self.bp_outside_walls[index].width

            if type(wall_width) is tuple:
                wall_width = wall_width[1]

            if index == 0:
                translate_y = self.width/2+wall_width/2
                scene = scene.union(wall.translate((0,-translate_y,0)))
            elif index == 1:
                translate_x = self.length/2+wall_width/2
                scene = scene.union(wall.rotate((0,0,1),(0,0,0),90).translate((-translate_x,0,0)))
            elif index == 2:
                translate_y = self.width/2+wall_width/2
                scene = scene.union(wall.rotate((0,0,1),(0,0,0),180).translate((0,translate_y,0)))
            elif index == 3:
                translate_x = self.length/2+wall_width/2
                scene = scene.union(wall.rotate((0,0,1),(0,0,0),-90).translate((translate_x,0,0)))
            #except Exception:
            #    print('something went wrong making outside walls')

        return scene

    def build_magnets(self):
        x_translate = self.calculate_internal_length()/2+self.magnet_diameter/2
        y_translate = self.calculate_internal_width()/2+self.magnet_diameter/2
        z_translate = self.height/2-self.magnet_height/2

        magnets = (
            cq.Workplane("XY")
            .union(self.magnet.translate((x_translate,y_translate,z_translate)))
            .union(self.magnet.translate((-x_translate,y_translate,z_translate)))
            .union(self.magnet.translate((x_translate,-y_translate,z_translate)))
            .union(self.magnet.translate((-x_translate,-y_translate,z_translate)))
        )

        return magnets

    def build_outside_corners(self):
        corners = cq.Workplane("XY")
        
        #if isinstance(self.bp_outside_corners, list):
        #    for i,bp_corner in self.bp_outside_corners:
        #        corner = bp_corner.build()
        #        corners = corners.add(corner)
        #else:
        corner = self.bp_outside_corners.build()
        mirror_corner = self.bp_outside_corners.build_mirror()
        x_translate = self.length/2-self.bp_outside_corners.length/2 + self.bp_outside_corners.corner_cut_length
        y_translate = self.width/2-self.bp_outside_corners.width/2 + self.bp_outside_corners.corner_cut_width
        coners = (
            corners
            .add(corner.translate((-x_translate,-y_translate,0)))
            .add(mirror_corner.rotate((0,0,1),(0,0,0),180).translate((-x_translate,y_translate,0)))
            .add(corner.rotate((0,0,1),(0,0,0),180).translate((x_translate,y_translate,0)))
            .add(mirror_corner.translate((x_translate,-y_translate,0)))
        )
        return corners

    def build(self):
        body =  super().build()

        scene = cq.Workplane("XY")

        if body:
            scene = scene.union(body)
            
        if self.render_inside_walls and self.inside_walls:
            inside_walls = self.build_inside_walls()
            scene = scene.union(inside_walls)


        if self.render_outside_walls and self.outside_walls:
            outside_walls = self.build_outside_walls()
            scene = scene.union(outside_walls)

                    
        if self.render_floor_tiles and self.bp_tile_generator:
            tiles = self.bp_tile_generator.build()                
            scene = scene.union(tiles.translate((0,0,-self.height/2+self.floor_height+self.tile_height/2)))

        if self.render_magnets and self.magnet:
            magnets = self.build_magnets()
            scene = scene.cut(magnets)
            
        if self.render_outside_corners and self.bp_outside_corners:
            corners = self.build_outside_corners()
            scene = scene.union(corners.translate((0,0,-self.height/2)))
            
        return scene