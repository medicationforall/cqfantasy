import cadquery as cq
from cqfantasy.house_wall import WallStuccoBrick

bp_wall = WallStuccoBrick()

bp_wall.length = 100
bp_wall.height = 50
bp_wall.seed = 'test'
bp_wall.cell_types = [
    'block',
    'block', 
    'empty',
    'block'
]

bp_wall.block_length = 8
bp_wall.width = 5
bp_wall.block_height = 3
bp_wall.block_spacing = 2

bp_wall.make()
ex_wall = bp_wall.build()

#show_object(ex_wall)
cq.exporters.export(ex_wall, "stl/house_wall_stucco_brick_class.stl")