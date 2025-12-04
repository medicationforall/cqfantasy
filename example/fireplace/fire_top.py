import cadquery as cq
from cqfantasy.fireplace import FireTop

bp_firetop = FireTop()
bp_firetop.length = 30
bp_firetop.width = 25
bp_firetop.height = 15
bp_firetop.top_height = 2
bp_firetop.top_length = 10
bp_firetop.top_width = 10 
bp_firetop.interior_padding = 2

bp_firetop.make()
result = bp_firetop.build()

#show_object(result)
cq.exporters.export(result, "stl/fireplace_firetop.stl")