import cadquery as cq
from cqfantasy.fireplace import HearthTiled

bp_hearth = HearthTiled()
bp_hearth.make()

ex_hearth = bp_hearth.build()

#show_object(ex_hearth)

cq.exporters.export(ex_hearth, "stl/fireplace_hearth_tiled.stl")