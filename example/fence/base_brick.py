import cadquery as cq
from cqfantasy.fence import BaseBrick

bp_base = BaseBrick()
bp_base.length = 75
bp_base.width = 20
bp_base.height = 25
bp_base.inner_padding = .6
bp_base.chamfer = 4

bp_base.render_magnets = True
bp_base.magnet_padding = 1
bp_base.magnet_padding_x = 2
bp_base.base_height = 5.6
bp_base.make()

ex_base = bp_base.build()

#show_object(ex_base)
cq.exporters.export(ex_base, 'stl/fence_base_brick.stl')