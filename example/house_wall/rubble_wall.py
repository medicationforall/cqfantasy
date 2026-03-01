import cadquery as cq
from cqfantasy.house_wall import RubbleWall

bp_wall = RubbleWall()
bp_wall.length = 100
bp_wall.width = 3
bp_wall.height = 75
bp_wall.x_padding = None
bp_wall.seed = 'test2'

bp_wall.make()
ex_wall = bp_wall.build()

#show_object(ex_wall)
cq.exporters.export(ex_wall, 'stl/house_rubble_wall.stl')