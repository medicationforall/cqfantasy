import cadquery as cq
from cqfantasy.house_wall import WallSplit, WallTudor, WallStuccoBrick

bp_wall = WallSplit()
bp_wall.height=110
bp_wall.bp_upper_wall = WallTudor()
bp_wall.bp_lower_wall = WallStuccoBrick()
bp_wall.split_divide_height = 51.5
bp_wall.make()
ex_wall = bp_wall.build()
outline = bp_wall.build_cut()

#show_object(ex_wall)
#show_object(outline.translate((0,.5,0))) 

cq.exporters.export(ex_wall, "stl/house_wall_split_class.stl")