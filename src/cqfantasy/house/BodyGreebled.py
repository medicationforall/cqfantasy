import cadquery as cq
from . import Body, TileGenerator
from ..tower import make_magnet
#from ..house_wall import WallTudor, WallStuccoBrick, WallTudorPaneling

class BodyGreebled(Body):
    def __init__(self):
        super().__init__()
        
        self.render_floor_tiles = True
        self.render_outside_walls = True
        self.render_inside_walls = True
        self.render_magnets = True
        self.floor_height = 10
        self.tile_height = 2.5

        self.magnet_diameter:float = 3.4
        self.magnet_height:float = 2.2
        
        #shapes
        self.outside_walls = None
        self.inside_walls = None
        self.magnet = None
        
        #blueprints
        self.bp_outside_walls = []
        self.bp_inside_walls = []
        self.bp_tile_generator:TileGenerator|None = TileGenerator()
        
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

    def build(self):
        body =  super().build()

        scene = cq.Workplane("XY")

        if body:
            scene = scene.union(body)
            
        if self.render_inside_walls and self.inside_walls:
            z_translate = self.floor_height
            if self.render_floor_tiles and self.bp_tile_generator:
                z_translate += self.tile_height
            for index, wall in enumerate(self.inside_walls):
                if index == 0:
                    length_translate = self.width/2-self.wall_width-self.bp_inside_walls[index].width/2
                    scene = scene.add(wall.rotate((0,0,1),(0,0,0),180).translate((0,-length_translate,z_translate/2)))
                elif index == 1:
                    width_translate = self.length/2-self.wall_width-self.bp_inside_walls[index].width/2
                    scene = scene.add(wall.rotate((0,0,1),(0,0,0),-90).translate((-width_translate,0,z_translate/2)))
                elif index == 2:
                    length_translate = self.width/2-self.wall_width-self.bp_inside_walls[index].width/2
                    scene = scene.add(wall.rotate((0,0,1),(0,0,0),0).translate((0,length_translate,z_translate/2)))
                elif index == 3:
                    width_translate = self.length/2-self.wall_width-self.bp_inside_walls[index].width/2
                    scene = scene.add(wall.rotate((0,0,1),(0,0,0),90).translate((width_translate,0,z_translate/2)))

        if self.render_outside_walls and self.outside_walls:
            #log('found outside wall')
            #show_object(self.outside_walls[0])
            
            for index, wall in enumerate(self.outside_walls):
                if index == 0:
                    translate_y = self.width/2+self.bp_outside_walls[index].width/2
                    scene = scene.add(wall.translate((0,-translate_y,0)))
                elif index == 1:
                    translate_x = self.length/2+self.bp_outside_walls[index].width/2
                    scene = scene.add(wall.rotate((0,0,1),(0,0,0),90).translate((-translate_x,0,0)))
                elif index == 2:
                    translate_y = self.width/2+self.bp_outside_walls[index].width/2
                    scene = scene.add(wall.rotate((0,0,1),(0,0,0),180).translate((0,translate_y,0)))
                elif index == 3:
                    translate_x = self.length/2+self.bp_outside_walls[index].width/2
                    scene = scene.add(wall.rotate((0,0,1),(0,0,0),-90).translate((translate_x,0,0)))
                    
        if self.render_floor_tiles and self.bp_tile_generator:
            tiles = self.bp_tile_generator.build()                
            scene = scene.add(tiles.translate((0,0,-self.height/2+self.floor_height+self.tile_height/2)))#self.tile_height/2+self.floor_height-self.tile_height)))#self.floor_height)))

        if self.render_magnets and self.magnet:
            x_translate = self.calculate_internal_length()/2+self.magnet_diameter/2
            y_translate = self.calculate_internal_width()/2+self.magnet_diameter/2
            z_translate = self.height/2-self.magnet_height/2
            scene = (
                scene
                .cut(self.magnet.translate((x_translate,y_translate,z_translate)))
                .cut(self.magnet.translate((-x_translate,y_translate,z_translate)))
                .cut(self.magnet.translate((x_translate,-y_translate,z_translate)))
                .cut(self.magnet.translate((-x_translate,-y_translate,z_translate)))
            )
 
        return scene