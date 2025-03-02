import cadquery as cq
from cqfantasy.house import TudorSplitBody

bp_body = TudorSplitBody()

bp_body.seed = 'test2'

bp_body.height = 75
bp_body.length = 200
bp_body.width = 150

bp_body.split_divide_height = 35
bp_body.split_width = 3
bp_body.split_height = 3

bp_body.block_length = 8
bp_body.block_width = 5
bp_body.block_height = 3
bp_body.make()

ex_body = bp_body.build()

#show_object(ex_body)

cq.exporters.export(ex_body,'stl/house_body_tudor_split.stl')