import cadquery as cq
from cqfantasy.watchtower import HillBase

bp_base = HillBase()
bp_base.length = 125
bp_base.width = 125
bp_base.height = 10
bp_base.taper = 40
bp_base.x_spacing = 6.25
bp_base.y_spacing = 6.25
bp_base.shift_x = (-2, 6, 1)
bp_base.shift_y = (-5, 2, .5)
bp_base.seed = "green"
bp_base.make()

ex_base = bp_base.build()

show_object(ex_base)

cq.exporters.export(ex_base, "stl/watch_tower_base.stl")