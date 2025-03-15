import cadquery as cq
from cqfantasy.house import WallTudor

bp_wall = WallTudor()

bp_wall.length = 100
bp_wall.height = 75 
bp_wall.styles = [None,"cross","left","right"]
bp_wall.panel_length = 25
bp_wall.panel_space = 3 
bp_wall.panel_width = 3

bp_wall.make()

ex_wall = bp_wall.build()

#show_object(ex_wall)
cq.exporters.export(ex_wall, "stl/house_wall_tudor_class.stl")