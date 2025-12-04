import cadquery as cq
from cqfantasy.fireplace import FireBox

bp_firebox = FireBox()
bp_firebox.length = 35
bp_firebox.width = 25
bp_firebox.height = 30
bp_firebox.x_padding = 5
bp_firebox.y_padding = 5
bp_firebox.interior_width = 10

bp_firebox.make()
result = bp_firebox.build()

#show_object(result)
cq.exporters.export(result, "stl/fireplace_firebox.stl")