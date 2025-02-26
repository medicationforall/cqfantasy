import cadquery as cq
from cqfantasy.house import Body

bp_body = Body()
bp_body.length = 150
bp_body.width = 150
bp_body.height = 75
bp_body.wall_width = 8
bp_body.floor_height = 4

bp_body.make()

ex_body = bp_body.build()

#show_object(ex_body)

cq.exporters.export(ex_body, "stl/house_body.stl")