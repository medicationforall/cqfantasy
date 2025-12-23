import cadquery as cq
from cqfantasy.fireplace import HearthTiled

bp_hearth = HearthTiled()
bp_hearth.length = 35
bp_hearth.width = 35
bp_hearth.height = 3
bp_hearth.tile_height = 1.5
bp_hearth.rows = 4
bp_hearth.columns = 4
bp_hearth.spacing = .5
bp_hearth.tile_padding = 2
bp_hearth.make()

ex_hearth = bp_hearth.build()

#show_object(ex_hearth)

cq.exporters.export(ex_hearth, "stl/fireplace_hearth_tiled.stl")