import cadquery as cq
from cqfantasy.fence import BasicBarDecoration


bp_spikes= BasicBarDecoration()
bp_spikes.length = 75
bp_spikes.width = 5
bp_spikes.height = 20

bp_spikes.bar_height = 3
bp_spikes.bar_z_translate = None
bp_spikes.spike_count = 7
bp_spikes.spike_lift = 4
bp_spikes.spike_diameter = 3

bp_spikes.make()

ex_spikes = bp_spikes.build()
ex_outline= bp_spikes.build_outline()

#show_object(ex_spikes)
#show_object(ex_outline.translate((0,5,0)))

cq.exporters.export(ex_spikes, 'stl/fence_basic_bar_decoration.stl')

