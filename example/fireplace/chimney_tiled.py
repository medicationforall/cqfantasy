import cadquery as cq
from cqfantasy.fireplace import ChimneyTiled

bp_chimney = ChimneyTiled()
bp_chimney.length = 6
bp_chimney.width = 6
bp_chimney.height = 60
bp_chimney.interior_padding = 2
bp_chimney.length = 10
bp_chimney.width = 6
bp_chimney.height = 60
bp_chimney.interior_padding = 2

bp_chimney.rows = 2
bp_chimney.columns = 2
bp_chimney.layers = 16
bp_chimney.spacing = .5
bp_chimney.tile_padding = 1.5

bp_chimney.make()
result = bp_chimney.build()

#show_object(result)
cq.exporters.export(result, "stl/fireplace_chimney_tiled.stl")