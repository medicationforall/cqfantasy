import cadquery as cq
from cqfantasy.fence import BarGreebled

bp_bar = BarGreebled()
bp_bar.length = 75
bp_bar.width = 5
bp_bar.height = 20

bp_bar.bar_height = 3
bp_bar.bar_z_translate = None
bp_bar.spike_count = 11
bp_bar.spike_lift = 4
bp_bar.spike_diameter = 2.5

bp_bar.top_length = 3.5
bp_bar.top_width = 3.5
bp_bar.top_height = 4
bp_bar.make()

ex_bar = bp_bar.build()

#show_object(ex_bar)
cq.exporters.export(ex_bar, 'stl/fence_bar_greebled.stl')