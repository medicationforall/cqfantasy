import cadquery as cq
from cqfantasy.house_wall import tudor_wall

ex_wall = tudor_wall(
    length = 100, 
    height = 75, 
    styles = [None,"cross","left","right"], 
    panel_length = 25, 
    panel_space = 3, 
    panel_width = 3
)
#show_object(ex_wall)

cq.exporters.export(ex_wall, 'stl/house_wall_tudor.stl')