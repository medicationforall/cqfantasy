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

from . import Body, Roof#, TileGenerator
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
        self.roof_overhang:Tuple[float,float,float] = (10,5,4)
        self.roof_gap_spacer:float = 0

        self.door_cut_width_padding:float = 0
        
        self.render_windows = True
        self.window_space:float|tuple[float,float] = 25
        self.window_length:float = 20
        self.window_width:float = 5
        self.window_offset:float = 0
        
        self.render_doors:bool = True
        
        self.window_x_style:list[None|str]|Tuple = ['window',None]
        self.window_y_style:list[None|str]|Tuple = []
        
        #shapes
        self.door_cut:cq.Workplane|None = None
        self.windows_x:list = []
        self.windows_y:list = []
        
        self.windows_x_cut:list = []
        self.windows_y_cut:list = []

        #blueprints
        self.bp_body = Body()
        self.bp_roof = Roof()
        self.bp_door = TiledDoor()
        self.bp_window:TowerWindow|None = FrameWindow()
        #self.bp_tile_generator:TileGenerator|None = TileGenerator()
        
    def make_body(self):
        self.bp_body.length = self.length
        self.bp_body.width = self.width
        self.bp_body.height = self.height
        self.bp_body.make()
        
    def make_roof(self):
        self.bp_roof.length = self.length+self.roof_overhang[0]*2
        self.bp_roof.width = self.width+self.roof_overhang[1]*2
        self.bp_roof.height = self.roof_height
        #bp_roof.overhang = (bp_house.roof_overhang[0],bp_house.roof_overhang[1], 4)

        self.bp_roof.overhang = (
            self.roof_overhang[0]+self.bp_body.wall_width,
            self.roof_overhang[1]+self.bp_body.wall_width, 
            self.roof_overhang[2]
        )
        self.bp_roof.make()
        
    def make_door(self):
        self.bp_door.make()
        
    def make_door_cut(self):
        self.door_cut = (
            cq.Workplane("XY")
            .box(self.bp_door.length,self.bp_body.wall_width+self.door_cut_width_padding,self.bp_door.height)
        )

    def _calulate_x_window_space(self)->float:
        if isinstance(self.window_space, tuple):
            x_window_space = self.window_space[0]
        else:
            x_window_space = self.window_space
        return x_window_space
    
    def _calulate_y_window_space(self)->float:
        if isinstance(self.window_space, tuple):
            y_window_space = self.window_space[1]
        else:
            y_window_space = self.window_space
        return y_window_space
    
    def make_x_windows(self, window, window_style):
        x_window_space = self._calulate_x_window_space()
        x_window_count = math.floor(self.bp_body.length / x_window_space)
        x_windows = cq.Workplane("XY")

        for index in range(x_window_count):
            if index < len(window_style):
                if window_style[index]:
                    x_windows = x_windows.union(window.translate((x_window_space*index,0,0)))
                else:
                    continue
            else:
                x_windows = x_windows.union(window.translate((x_window_space*index,0,0)))
        return x_windows
    
    def make_y_windows(self, window, window_style):
        y_window_space = self._calulate_y_window_space()
        y_window_count = math.floor(self.bp_body.width / y_window_space)
        y_windows = cq.Workplane("XY")
        for index in range(y_window_count):
            if index < len(window_style):
                if window_style[index]:
                    y_windows = y_windows.union(window.translate((y_window_space*index,0,0)))
                else:
                    continue
            else:
                y_windows = y_windows.union(window.translate((y_window_space*index,0,0)))

        return y_windows
        
    def make_windows(self):
        if self.bp_window:
            self.bp_window.render_cylinder = False
            self.bp_window.length = self.window_length
            if hasattr(self.bp_window, 'frame_width'):
                self.bp_window.frame_width = self.window_width #type:ignore
            #self.bp_window.width = 10
            self.bp_window.make()
            window = self.bp_window.build()

            #('make_windows')

            # x_windows
            if isinstance(self.window_x_style, tuple):
                #print('window_x_style is tuple hit')
                x_window_space = self._calulate_x_window_space()
                #print(self.window_x_style[0])

                if self.window_x_style[0]:
                    x_windows = self.make_x_windows(window, self.window_x_style[0])
                    x_windows = x_windows.translate((-self.bp_body.length/2+x_window_space/2,0,0))
                    self.windows_x.append(x_windows)
                else:
                     self.windows_x.append(None)

                if self.window_x_style[1]:
                    x_windows_two = self.make_x_windows(window, self.window_x_style[1])
                    x_windows_two = x_windows_two.translate((-self.bp_body.length/2+x_window_space/2,0,0))
                    self.windows_x.append(x_windows_two)
                else:
                    self.windows_x.append(None)
            else: 
                x_window_space = self._calulate_x_window_space()
                x_windows = self.make_x_windows(window, self.window_x_style)
                x_windows = x_windows.translate((-self.bp_body.length/2+x_window_space/2,0,0))
                self.windows_x.append(x_windows)

            # y_windows
            if isinstance(self.window_y_style, tuple):
                #print('window_y_style is tuple hit')

                if self.window_y_style[0]:
                    y_window_space = self._calulate_y_window_space()
                    y_windows = self.make_y_windows(window, self.window_y_style[0])
                    y_windows = y_windows.translate((-self.bp_body.width/2+y_window_space/2,0,0))
                    self.windows_y.append(y_windows)
                else:
                    self.windows_y.append(None)

                if self.window_y_style[1]:
                    y_windows_two = self.make_y_windows(window, self.window_y_style[1])
                    y_windows_two = y_windows_two.translate((-self.bp_body.width/2+y_window_space/2,0,0))
                    self.windows_y.append(y_windows_two)
                else:
                    self.windows_y.append(None)
            else: 
                y_window_space = self._calulate_y_window_space()
                y_windows = self.make_y_windows(window, self.window_y_style)
                y_windows = y_windows.translate((-self.bp_body.width/2+y_window_space/2,0,0))
                self.windows_y.append(y_windows)   
        
    def make_windows_cut(self):
        if self.bp_window:
            window_cut = self.bp_window.build_cut()
            #('make_windows_cut')
       
            # x_windows
            if isinstance(self.window_x_style, tuple):
                #print('window_x_style is tuple hit')
                if self.window_x_style[0]:
                    x_window_space = self._calulate_x_window_space()
                    x_windows = self.make_x_windows(window_cut, self.window_x_style[0])
                    x_windows = x_windows.translate((-self.bp_body.length/2+x_window_space/2,0,0))
                    self.windows_x_cut.append(x_windows)
                else:
                    self.windows_x_cut.append(None)

                if self.window_x_style[1]:
                    x_windows_two = self.make_x_windows(window_cut, self.window_x_style[1])
                    x_windows_two = x_windows_two.translate((-self.bp_body.length/2+x_window_space/2,0,0))
                    self.windows_x_cut.append(x_windows_two)
                else:
                    self.windows_x_cut.append(None)
            else: 
                x_window_space = self._calulate_x_window_space()
                x_windows = self.make_x_windows(window_cut, self.window_x_style)
                x_windows = x_windows.translate((-self.bp_body.length/2+x_window_space/2,0,0))
                self.windows_x_cut.append(x_windows)

            # y_windows
            if isinstance(self.window_y_style, tuple):
                #('window_y_style is tuple hit')
                if self.window_y_style[0]:
                    y_window_space = self._calulate_y_window_space()
                    y_windows = self.make_y_windows(window_cut, self.window_y_style[0])
                    y_windows = y_windows.translate((-self.bp_body.width/2+y_window_space/2,0,0))
                    self.windows_y_cut.append(y_windows)
                else:
                    self.windows_y_cut.append(None)

                if self.window_y_style[0]:
                    y_windows_two = self.make_y_windows(window_cut, self.window_y_style[1])
                    y_windows_two = y_windows_two.translate((-self.bp_body.width/2+y_window_space/2,0,0))
                    self.windows_y_cut.append(y_windows_two)
                else:
                    self.windows_y_cut.append(None)
            else: 
                y_window_space = self._calulate_y_window_space()
                y_windows = self.make_y_windows(window_cut, self.window_y_style)
                y_windows = y_windows.translate((-self.bp_body.width/2+y_window_space/2,0,0))
                self.windows_y_cut.append(y_windows)

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


    def build_cut_windows(self):
        scene = cq.Workplane("XY")

        if self.windows_x_cut:
            #print('found windows x_cut')
            if len(self.windows_x_cut) == 1:
                windows_x_cut_plus = self.windows_x_cut[0]
                windows_x_cut_minus = self.windows_x_cut[0]
            else:
                windows_x_cut_plus = self.windows_x_cut[0]
                windows_x_cut_minus = self.windows_x_cut[1]

            y_translate = self.bp_body.width/2-self.bp_body.wall_width/2

            print('try to cut x windows')
            if windows_x_cut_plus:
                scene = scene.union(windows_x_cut_plus.translate((0,-y_translate,self.bp_body.height/2+self.window_offset)))

            if windows_x_cut_minus:
                scene = scene.union(windows_x_cut_minus.rotate((0,0,1),(0,0,0),-180).translate((0,y_translate,self.bp_body.height/2+self.window_offset)))

        if self.windows_y_cut:
            #print('found windows y_cut')
            if len(self.windows_y_cut) == 1:
                windows_y_cut_plus = self.windows_y_cut[0]
                windows_y_cut_minus = self.windows_y_cut[0]
            else:
                windows_y_cut_plus = self.windows_y_cut[0]
                windows_y_cut_minus = self.windows_y_cut[1]

            print('try to cut y windows')
            if windows_y_cut_plus:
                scene = scene.union(
                    windows_y_cut_plus.translate((0,0,self.bp_body.height/2+self.window_offset))
                    .rotate((0,0,1),(0,0,0),-90)
                    .translate((self.length/2-self.bp_body.wall_width/2,0,0))
                )

            if windows_y_cut_minus:
                scene = scene.union(
                    windows_y_cut_minus.translate((0,0,self.bp_body.height/2+self.window_offset))
                    .rotate((0,0,1),(0,0,0),90)
                    .translate((-self.length/2+self.bp_body.wall_width/2,0,0))
                )

        return scene

    def build_windows(self):
        scene = cq.Workplane("XY")

        if self.windows_x:
            if len(self.windows_x) == 1:
                windows_x_plus = self.windows_x[0]
                windows_x_minus = self.windows_x[0]
            else:
                windows_x_plus = self.windows_x[0]
                windows_x_minus = self.windows_x[1]

            y_translate = self.bp_body.width/2-self.bp_body.wall_width/2

            if windows_x_plus:
                scene = scene.union(windows_x_plus.translate((0,-y_translate,self.bp_body.height/2+self.window_offset)))
            
            if windows_x_minus:
                scene = scene.union(windows_x_minus.rotate((0,0,1),(0,0,0),-180).translate((0,y_translate,self.bp_body.height/2+self.window_offset)))
            
        if self.windows_y:
            if len(self.windows_y) == 1:
                windows_y_plus = self.windows_y[0]
                windows_y_minus = self.windows_y[0]
            else:
                windows_y_plus = self.windows_y[0]
                windows_y_minus = self.windows_y[1]

            if windows_y_plus:
                scene = scene.union(
                    windows_y_plus.translate((0,0,self.bp_body.height/2+self.window_offset))
                    .rotate((0,0,1),(0,0,0),-90)
                    .translate((self.length/2-self.bp_body.wall_width/2,0,0))
                )

            if windows_y_minus:
                scene = scene.union(
                    windows_y_minus.translate((0,0,self.bp_body.height/2+self.window_offset))
                    .rotate((0,0,1),(0,0,0),90)
                    .translate((-self.length/2+self.bp_body.wall_width/2,0,0)) 
                )

        return scene


    def build_body(self) -> cq.Workplane:
        print('Build house body')
        body = self.bp_body.build()
        
        scene = (
            cq.Workplane("XY")
        )

        if body:
            scene = scene.add(body.translate((0,0,self.bp_body.height/2)))

        print('build house doors')
        if self.render_doors and self.door_cut:
            print('build house doors cuts')
            door_cut = self.door_cut
            scene = scene.cut(door_cut.translate((0,-self.width/2+self.bp_body.wall_width/2,self.bp_door.height/2+self.bp_body.calculate_floor_height())))

        if self.render_doors:
            door = self.bp_door.build()
            print('build house doors add doors')
            scene = scene.union(door.translate((0,-self.width/2+self.bp_body.wall_width/2,self.bp_door.height/2+self.bp_body.calculate_floor_height())))

        print('build house windows')
        if self.render_windows:
            cut_windows = self.build_cut_windows()
            windows = self.build_windows()

            scene = (
                scene
                .cut(cut_windows)
                .union(windows)
            )

        return scene
    
    def build_roof(self):
        roof = self.bp_roof.build()
        return roof

    def build(self) -> cq.Workplane:
        #log("build")
        
        body = self.build_body()
        
        scene = (
            cq.Workplane("XY")
        )

        if body:
            scene = scene.union(body)

        if self.render_roof:
            roof = self.bp_roof.build()
            scene = scene.add(roof.translate((0,0,self.bp_body.height+self.bp_roof.height/2+self.roof_gap_spacer)))
                 
        return scene
    
    
    def build_plate(self):
        body = self.build_body()
        
        scene = (
            cq.Workplane("XY")
        )

        if body:
            scene = scene.union(body)
        
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