import cadquery as cq
from cqfantasy.fireplace import Chimney

bp_chimney = Chimney()
bp_chimney.length = 6
bp_chimney.width = 6
bp_chimney.height = 60
bp_chimney.interior_padding = 2

bp_chimney.make()
result = bp_chimney.build()

#show_object(result)
cq.exporters.export(result, "stl/fireplace_chimney.stl")