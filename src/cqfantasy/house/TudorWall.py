import cadquery as cq
import math

def __angle(
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

def __crossing(
        length:float, 
        width:float, 
        height:float, 
        r_angle:float
    ) -> cq.Workplane:
    beam = (
        cq.Workplane("XY")
        .box(length,width,height)
        .rotate((0,1,0),(0,0,0),r_angle)
    )
    
    beam_2 = (
        cq.Workplane("XY")
        .box(length,width,height)
        .rotate((0,1,0),(0,0,0),-r_angle)
    )
    
    return beam.union(beam_2)

def __left_detail(
        length:float, 
        width:float, 
        height:float, 
        r_angle:float
    )->cq.Workplane:
    beam_2 = (
        cq.Workplane("XY")
        .box(length, width, height)
        .rotate((0,1,0),(0,0,0), -r_angle)
    )
    return beam_2

def __right_detail(
        length:float, 
        width:float, 
        height:float, 
        r_angle:float
    )->cq.Workplane:
    beam_2 = (
        cq.Workplane("XY")
        .box(length, width, height)
        .rotate((0,1,0),(0,0,0), r_angle)
    )
    return beam_2

def __make_detail(
        style:str|None, 
        length:float, 
        width:float, 
        height:float, 
        r_angle:float
    ):
    detail = cq.Workplane("XY")
    if style and style=="cross":                    
        detail = __crossing(length, width, height, r_angle)
    elif style and style == "left":
        detail = __left_detail(length, width, height, r_angle)
    elif style and style == "right":
        detail = __right_detail(length, width, height, r_angle)

    return detail

def __panel_wall(
        length:float, 
        height:float, 
        panel_length:float, 
        panel_width:float, 
        panel_space:float
    ):
    x_count = math.floor(length / panel_length)
    outline = cq.Workplane("XY").box(length,panel_width,height)
    panel = cq.Workplane("XY").box(panel_length-panel_space,panel_width,height)
    
    def add_panel(loc:cq.Location)->cq.Shape:
        return panel.val().located(loc) #type:ignore
    
    panels = (
        cq.Workplane("XY")
        .rarray(
            xSpacing = panel_length, 
            ySpacing = panel_width,
            xCount = x_count, 
            yCount= 1, 
            center = True)
        .eachpoint(callback = add_panel)
    )
    
    return outline, panels

def __tudor_styled_wall(
        length:float, 
        height:float, 
        styles:list[str|None]|str|None, 
        panel_length:float, 
        panel_space:float, 
        panel_width:float
    ):
        styled_panes = cq.Workplane("XY")
        
        if styles:
            if isinstance(styles, list):
                hyp = math.hypot(panel_length, height)
                r_angle = __angle(height,panel_length)
                        
                for index,style in enumerate(styles):
                    detail = __make_detail(style,panel_space,panel_width,hyp,r_angle)
                    styled_panes = styled_panes.add(detail.translate((length/2-panel_length/2-panel_length*index,0,0)))
            else:
                count = math.floor(length / panel_length)
                hyp = math.hypot(panel_length, height)
                r_angle = __angle(height,panel_length)

                detail = __make_detail(styles,panel_space,panel_width,hyp,r_angle)

                for index in range(count):
                    styled_panes = styled_panes.add(detail.translate((length/2-panel_length/2-panel_length*index,0,0)))

            return styled_panes
        
def tudor_wall(
        length:float = 100, 
        height:float = 75, 
        styles:list[str|None]|str|None = [None,"cross","left","right"], 
        panel_length:float = 25, 
        panel_space:float = 3, 
        panel_width:float = 3
    ):
    outline, panels = __panel_wall(length, height, panel_length, panel_width, panel_space)
    details = __tudor_styled_wall(length, height, styles, panel_length, panel_space, panel_width)
    return outline.cut(panels).union(details)