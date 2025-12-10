import cadquery as cq
from cqfantasy.fireplace import FireplaceTiled

bp_fireplace = FireplaceTiled()
bp_fireplace.interior_padding = 2
bp_fireplace.render_hearth = True

bp_fireplace.make()
result = bp_fireplace.build()
#show_object(result)
cq.exporters.export(result, "stl/fireplace_tiled.stl")