import cadquery as cq
import math
from . import Body

def angle(
        length:float, 
        height:float
    ) -> float:
    '''
    Finds the hypotenuse of a right triangle
    Presumed length and height are part of a right triangle
    '''
    hyp = math.hypot(length, height)
    angle = length/hyp
    angle_radians = math.acos((angle))
    angle_deg = math.degrees(angle_radians)
    return angle_deg

class TudorBody(Body):
    def  __init__(self):
        super().__init__()
        self.split_width = 3
        self.split_height = 3
        
        self.corner_length = 3
        self.corner_width = 3
        
        self.split_divide_height = 15
        self.panel_length = 25
        self.panel_width = 2.5
        self.panel_space = 2
        
        self.x_styles = ["cross",None,None,"cross"]
        self.y_styles = ["cross",None,None,"cross"]
        
        #shapes
        self.split_x = None
        self.split_y = None
        self.corner = None
        self.panels_x = None
        self.panels_y = None
        self.tudor_x_details = None
        self.tudor_y_details = None
        
    def make_split(self):
        split_x = cq.cq.Workplane("XY").box(self.length,self.split_width,self.split_height)
        self.split_x = split_x
        
        split_y = cq.cq.Workplane("XY").box(self.split_width,self.width,self.split_height)
        self.split_y = split_y
        
    def make_corner(self):
        corner = cq.Workplane("XY").box(self.corner_length,self.corner_width,self.height)
        
        self.corner = corner
        
    def calculate_panel_height(self):
        return self.height - self.split_height*2 - self.split_divide_height*2
        
    
    def make_panel_wall(self, length):
        
        #self.panel_length = 10
        #self.panel_width
        #self.panel_space = 3
        
        height = self.calculate_panel_height()
        panel_length = self.panel_length #+ self.panel_space
        x_count = math.floor(length / panel_length)
        #log(f'make_panel_all {panel_length} {x_count}')
        outline = cq.Workplane("XY").box(length,self.panel_width,height)
        panel = cq.Workplane("XY").box(self.panel_length-self.panel_space,self.panel_width,height)
        
        def add_panel(loc:cq.Location)->cq.Shape:
            return panel.val().located(loc) #type:ignore
        
        panels = result = (
            cq.Workplane("XY")
            .rarray(
                xSpacing = panel_length, 
                ySpacing = self.panel_width,
                xCount = x_count, 
                yCount= 1, 
                center = True)
            .eachpoint(callback = add_panel)
        )
        
        return outline, panels
        
    def make_panels(self):
        outline_x, panels_x = self.make_panel_wall(self.length)
        outline_y, panels_y = self.make_panel_wall(self.width)

        self.panels_x = outline_x.cut(panels_x)
        self.panels_y = outline_y.cut(panels_y)
        
    def make_x_styles(self):
        #log('make_x_styles')
        if self.x_styles:
            height = self.calculate_panel_height()
            panel_length = self.panel_length
            
            hyp = math.hypot(panel_length, height)
            r_angle = angle(height,panel_length)
                    
            x_styles = cq.Workplane("XY")
            for index,style in enumerate(self.x_styles):
                if style and style=="cross":
                    beam = (
                        cq.Workplane("XY")
                        .box(self.panel_space,self.panel_width,hyp)
                        .rotate((0,1,0),(0,0,0),r_angle)
                    )
                    
                    beam_2 = (
                        cq.Workplane("XY")
                        .box(self.panel_space,self.panel_width,hyp)
                        .rotate((0,1,0),(0,0,0),-r_angle)
                    )
                    
                    cross = beam.union(beam_2).translate((self.length/2-panel_length/2-panel_length*index,0,0))
                    
                    x_styles = x_styles.add(cross)
                elif style and style == "left":

                    beam_2 = (
                        cq.Workplane("XY")
                        .box(self.panel_space,self.panel_width,hyp)
                        .rotate((0,1,0),(0,0,0),-r_angle)
                    )
                    
                    left = beam_2.translate((self.length/2-panel_length/2-panel_length*index,0,0))
                    x_styles = x_styles.add(left)
                elif style and style == "right":

                    beam = (
                        cq.Workplane("XY")
                        .box(self.panel_space,self.panel_width,hyp)
                        .rotate((0,1,0),(0,0,0),r_angle)
                    )
                    
                    right = beam.translate((self.length/2-panel_length/2-panel_length*index,0,0))
                    x_styles = x_styles.add(right)
                    
            self.tudor_x_details = x_styles
            
    def make_y_styles(self):
        #log('make_y_styles')
        if self.y_styles:
            y_styles = cq.Workplane("XY")
            
            height = self.calculate_panel_height()
            panel_length = self.panel_length
            
            hyp = math.hypot(panel_length, height)
            r_angle = angle(height,panel_length)
            
            for index,style in enumerate(self.y_styles):
                if style and style=="cross":
                    beam = (
                        cq.Workplane("XY")
                        .box(self.panel_space,self.panel_width,hyp)
                        .rotate((0,1,0),(0,0,0),r_angle)
                    )
                    
                    beam_2 = (
                        cq.Workplane("XY")
                        .box(self.panel_space,self.panel_width,hyp)
                        .rotate((0,1,0),(0,0,0),-r_angle)
                    )
                    
                    cross = beam.union(beam_2).translate((self.width/2-panel_length/2-panel_length*index,0,0))
                    
                    y_styles = y_styles.add(cross)
                    
                elif style and style == "left":

                    beam_2 = (
                        cq.Workplane("XY")
                        .box(self.panel_space,self.panel_width,hyp)
                        .rotate((0,1,0),(0,0,0),-r_angle)
                    )
                    
                    left = beam_2.translate((self.width/2-panel_length/2-panel_length*index,0,0))
                    y_styles = y_styles.add(left)
                elif style and style == "right":
                    beam = (
                        cq.Workplane("XY")
                        .box(self.panel_space,self.panel_width,hyp)
                        .rotate((0,1,0),(0,0,0),r_angle)
                    )
                    
                    right = beam.translate((self.width/2-panel_length/2-panel_length*index,0,0))
                    y_styles = y_styles.add(right)
                    
            self.tudor_y_details = y_styles

    def make(self, parent=None):
        self.make_split()
        self.make_corner()
        self.make_panels()
        self.make_x_styles()
        self.make_y_styles()
        super().make(parent)
        
    def build(self):
        scene = cq.Workplane("XY")
        body = super().build()
        
        if body:
            scene = scene.union(body)
            
            
        split_translate_z_bottom = -self.height/2+self.split_height/2+self.split_divide_height
        split_translate_z_top = self.height/2-self.split_height/2-self.split_divide_height

    
        if self.split_x:
            scene = (
                scene
                .union(self.split_x.translate((0,-self.width/2-self.split_width/2,split_translate_z_bottom)))
                .union(self.split_x.translate((0,self.width/2+self.split_width/2,split_translate_z_bottom)))
                .union(self.split_x.translate((0,-self.width/2-self.split_width/2,split_translate_z_top)))
                .union(self.split_x.translate((0,self.width/2+self.split_width/2,split_translate_z_top)))

            )
            
        if self.split_y:
            scene = (
                scene
                .union(self.split_y.translate((-self.length/2-self.split_width/2,0,split_translate_z_bottom)))
                .union(self.split_y.translate((self.length/2+self.split_width/2,0,split_translate_z_bottom)))
                .union(self.split_y.translate((-self.length/2-self.split_width/2,0,split_translate_z_top)))
                .union(self.split_y.translate((self.length/2+self.split_width/2,0,split_translate_z_top)))
            )
            
        if self.corner:
            scene = (
                scene
                .union(self.corner.translate((-self.length/2-self.corner_length/2,self.width/2+self.corner_width/2,0)))
                .union(self.corner.translate((self.length/2+self.corner_length/2,self.width/2+self.corner_width/2,0)))
                .union(self.corner.translate((self.length/2+self.corner_length/2,-self.width/2-self.corner_width/2,0)))
                .union(self.corner.translate((-self.length/2-self.corner_length/2,-self.width/2-self.corner_width/2,0)))
            )
            
        if self.panels_x:
            translate_y = self.width/2+self.panel_width/2
            scene = (
                scene
                .add(self.panels_x.translate((0,translate_y,0)))
                .add(self.panels_x.translate((0,-translate_y,0)))
            )
            
        if self.panels_y:
            translate_x = self.length/2+self.panel_width/2
            scene = (
                scene
                .add(self.panels_y
                     .rotate((0,0,1),(0,0,0),90)
                     .translate((-translate_x,0,0))
                )
                .add(self.panels_y
                     .rotate((0,0,1),(0,0,0),90)
                     .translate((translate_x,0,0))
                )
            )
            
        if self.tudor_x_details:
            translate_y = self.width/2+self.panel_width/2
            scene = (
                scene
                .union(self.tudor_x_details.translate((0,translate_y,0)))
                .union(self.tudor_x_details.rotate((0,0,1),(0,0,0),180).translate((0,-translate_y,0)))
            )
            
        if self.tudor_y_details:
            translate_x = self.length/2+self.panel_width/2
            scene = (
                scene
                .union(
                    self.tudor_y_details
                    .rotate((0,0,1),(0,0,0),-90)
                    .translate((-translate_x,0,0))
                )
                .union(
                    self.tudor_y_details
                    .rotate((0,0,1),(0,0,0),90)
                    .translate((translate_x,0,0))
                )
                #.add(self.tudor_x_details.translate((0,-translate_y,0)))
            )
            
        return scene