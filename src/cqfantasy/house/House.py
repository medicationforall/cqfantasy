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
import math
from cadqueryhelper import Base
from typing import Tuple

from . import Body, Roof, TileGenerator
from cqterrain.door import TiledDoor
from cqfantasy.tower import TowerWindow, FrameWindow

class House(Base):
    def __init__(self):
        super().__init__()
        #parameters
        self.length:float = 100
        self.width:float = 150
        self.height:float = 75
        
        self.render_roof = True
        self.roof_height:float = 50
        self.roof_overhang:Tuple[float,float] = (10,5)
        self.roof_gap_spacer:float = 0

        self.door_cut_width_padding:float = 0
        
        self.render_windows = True
        self.window_space = 25
        self.window_length = 20
        self.window_width = 5
        
        self.render_doors = True
        
        self.window_x_style = ['window',None]
        self.window_y_style = []
        
        self.render_floor_tiles = True
        self.floor_height = 10
        self.tile_height = 2.5
        
        
        #shapes
        self.door_cut:cq.Workplane|None = None
        self.windows_x = None
        self.windows_y = None
        
        self.windows_x_cut = None
        self.windows_y_cut = None

        
        #blueprints
        self.bp_body = Body()
        self.bp_roof = Roof()
        self.bp_door = TiledDoor()
        self.bp_window:TowerWindow|None = FrameWindow()
        self.bp_tile_generator:TileGenerator|None = TileGenerator()
        
    def make_body(self):
        self.bp_body.length = self.length
        self.bp_body.width = self.width
        self.bp_body.height = self.height
        self.bp_body.floor_height = self.floor_height - self.tile_height
        self.bp_body.make()
        
    def make_roof(self):
        self.bp_roof.length = self.length+self.roof_overhang[0]*2
        self.bp_roof.width = self.width+self.roof_overhang[1]*2
        self.bp_roof.height = self.roof_height
        #bp_roof.overhang = (bp_house.roof_overhang[0],bp_house.roof_overhang[1], 4)

        self.bp_roof.overhang = (
            self.roof_overhang[0]+self.bp_body.wall_width,
            self.roof_overhang[1]+self.bp_body.wall_width, 
            4
        )
        self.bp_roof.make()
        
    def make_door(self):
        self.bp_door.make()
        
    def make_door_cut(self):
        self.door_cut = (
            cq.Workplane("XY")
            .box(self.bp_door.length,self.bp_body.wall_width+self.door_cut_width_padding,self.bp_door.height)
        )
        
    def make_windows(self):
        if self.bp_window:
            self.bp_window.render_cylinder = False
            self.bp_window.length = self.window_length
            if hasattr(self.bp_window, 'frame_width'):
                self.bp_window.frame_width = self.window_width #type:ignore
            #self.bp_window.width = 10
            self.bp_window.make()
            
            window = self.bp_window.build()
            
            def add_window(loc:cq.Location)->cq.Shape:
                return window.val().located(loc) #type:ignore
            
            x_window_count = math.floor(self.bp_body.length / self.window_space)
            
            x_windows = cq.Workplane("XY")
            for index in range(x_window_count):
                if index < len(self.window_x_style):
                    if self.window_x_style[index]:
                        x_windows = x_windows.add(window.translate((self.window_space*index,0,0)))
                    else:
                        continue
                else:
                    x_windows = x_windows.add(window.translate((self.window_space*index,0,0)))

            
            x_windows = x_windows.translate((-self.bp_body.length/2+self.window_space/2,0,0))

            y_window_count = math.floor(self.bp_body.width / self.window_space)
            
            y_windows = cq.Workplane("XY")
            for index in range(y_window_count):
                if index < len(self.window_y_style):
                    if self.window_y_style[index]:
                        y_windows = y_windows.add(window.translate((self.window_space*index,0,0)))
                    else:
                        continue
                else:
                    y_windows = y_windows.add(window.translate((self.window_space*index,0,0)))

            y_windows = y_windows.translate((-self.bp_body.width/2+self.window_space/2,0,0))

            #log(f'{x_window_count=}')
            self.windows_x = x_windows
            self.windows_y = y_windows
        
    def make_windows_cut(self):
        if self.bp_window:
            window_cut = self.bp_window.build_cut()
            
            #window = self.bp_window.build()
            
            def add_window(loc:cq.Location)->cq.Shape:
                return window_cut.val().located(loc) #type:ignore
            
            x_window_count = math.floor(self.bp_body.length / self.window_space)
            
            x_windows = cq.Workplane("XY")
            for index in range(x_window_count):
                if index < len(self.window_x_style):
                    if self.window_x_style[index]:
                        x_windows = x_windows.add(window_cut.translate((self.window_space*index,0,0)))
                    else:
                        continue
                else:
                    x_windows = x_windows.add(window_cut.translate((self.window_space*index,0,0)))
            
            x_windows = x_windows.translate((-self.bp_body.length/2+self.window_space/2,0,0))

            y_window_count = math.floor(self.bp_body.width / self.window_space)
            
            y_windows = cq.Workplane("XY")
            for index in range(y_window_count):
                if index < len(self.window_y_style):
                    if self.window_y_style[index]:
                        y_windows = y_windows.add(window_cut.translate((self.window_space*index,0,0)))
                    else:
                        continue
                else:
                    y_windows = y_windows.add(window_cut.translate((self.window_space*index,0,0)))

            y_windows = y_windows.translate((-self.bp_body.width/2+self.window_space/2,0,0))

            self.windows_x_cut = x_windows
            self.windows_y_cut = y_windows
        
    def make_floor_tiles(self):
        if self.bp_tile_generator:
            self.bp_tile_generator.length = self.length - self.bp_body.wall_width*2
            self.bp_tile_generator.width = self.width - self.bp_body.wall_width*2
            self.bp_tile_generator.tile_height = self.tile_height
            self.bp_tile_generator.make()

    def make(self, parent=None):
        super().make(parent)
        self.make_body()
        if self.render_roof:
            self.make_roof()
            
        if self.render_doors:
            self.make_door()
            self.make_door_cut()
            
        if self.render_windows:
            self.make_windows()
            self.make_windows_cut()
            
        if self.render_floor_tiles:
            self.make_floor_tiles()
        
    def build(self) -> cq.Workplane:
        #log("build")
        super().build()
        body = self.bp_body.build()
        
        scene = (
            cq.Workplane("XY")
        )

        if body:
            scene = scene.union(body.translate((0,0,self.bp_body.height/2)))

        if self.render_doors and self.door_cut:
            door_cut = self.door_cut
            scene = scene.cut(door_cut.translate((0,-self.width/2+self.bp_body.wall_width/2,self.bp_door.height/2+self.floor_height)))

        if self.render_doors:
            door = self.bp_door.build()
            scene = scene.union(door.translate((0,-self.width/2+self.bp_body.wall_width/2,self.bp_door.height/2+self.floor_height)))

        if self.render_roof:
            roof = self.bp_roof.build()
            scene = scene.add(roof.translate((0,0,self.bp_body.height+self.bp_roof.height/2+self.roof_gap_spacer)))
            
        if self.render_windows:
            #self.windows_x = None
            #self.windows_y = None
            
            if self.windows_x_cut:
                scene = (
                    scene
                    #plus
                    .cut(self.windows_x_cut.translate((0,self.bp_body.width/2-self.bp_body.wall_width/2,self.bp_body.height/2)))
                    #minus
                    .cut(self.windows_x_cut.rotate((0,0,1),(0,0,0),-180).translate((0,-self.bp_body.width/2+self.bp_body.wall_width/2,self.bp_body.height/2)))
                )
                
            if self.windows_y_cut:
                scene = (
                    scene
                    #plus
                    .cut(
                        self.windows_y_cut.translate((0,0,self.bp_body.height/2))
                        .rotate((0,0,1),(0,0,0),-90)
                        .translate((self.length/2-self.bp_body.wall_width/2,0,0))
                    )
                    #minus
                    .cut(
                        self.windows_y_cut.translate((0,0,self.bp_body.height/2))
                        .rotate((0,0,1),(0,0,0),90)
                        .translate((-self.length/2+self.bp_body.wall_width/2,0,0))
                    )
                )
            
            if self.windows_x:
                scene = (
                    scene
                    #plus
                    .add(self.windows_x.translate((0,self.bp_body.width/2-self.bp_body.wall_width/2,self.bp_body.height/2)))
                    #minus
                    .add(self.windows_x.rotate((0,0,1),(0,0,0),-180).translate((0,-self.bp_body.width/2+self.bp_body.wall_width/2,self.bp_body.height/2)))
                )
                
            if self.windows_y:
                scene = (
                    scene
                    #plus
                    .add(
                        self.windows_y.translate((0,0,self.bp_body.height/2))
                        .rotate((0,0,1),(0,0,0),-90)
                        .translate((self.length/2-self.bp_body.wall_width/2,0,0))
                    )
                    #minus
                    .add(
                        self.windows_y.translate((0,0,self.bp_body.height/2))
                        .rotate((0,0,1),(0,0,0),90)
                        .translate((-self.length/2+self.bp_body.wall_width/2,0,0))
                    )
                )
                
            if self.render_floor_tiles and self.bp_tile_generator:
                tiles = self.bp_tile_generator.build()
                
                scene = scene.add(tiles.translate((0,0,self.tile_height/2+self.floor_height-self.tile_height)))#self.floor_height)))
                
                
        return scene
    
    
    def build_plate(self):
        #log("build_plate")
        body = self.bp_body.build()
        door = self.bp_door.build()
        door_cut = self.door_cut
        
        scene = (
            cq.Workplane("XY")
        )

        if body:
            scene = scene.union(body.translate((0,0,self.bp_body.height/2)))
        if door_cut:
            scene = scene.cut(door_cut.translate((0,-self.width/2+self.bp_body.wall_width/2,self.bp_door.height/2+self.bp_body.floor_height)))

        if door:
            scene = scene.union(door.translate((0,-self.width/2+self.bp_body.wall_width/2,self.bp_door.height/2+self.bp_body.floor_height)))

        if self.render_roof:
            roof = self.bp_roof.build()
            scene = scene.add(roof.translate((self.bp_body.length/2+self.bp_roof.length/2+10,0,self.bp_roof.height/2)))
        return scene
    
    def build_cut_away(self):
        #log("build_cut_away")
        house = self.build()
        length = self.length + self.roof_overhang[0]*2
        width = self.width + self.roof_overhang[1]*2
        height = self.height+self.roof_height+50
        cut_away = cq.Workplane("XY").box(length,width,height)
        scene = (
            cq.Workplane("XY")
            .add(house)
            .cut(cut_away.translate((-length/2,0,height/2)))
            .cut(cut_away.translate((0,width/2,height/2)))

        )
        
        return scene