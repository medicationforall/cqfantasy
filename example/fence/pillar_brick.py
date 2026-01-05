import cadquery as cq
from cqfantasy.fence import PillarBrick

bp_pillar = PillarBrick()
bp_pillar.length = 25
bp_pillar.width = 25
bp_pillar.height = 60
bp_pillar.inner_padding = 1

bp_pillar.cap_width = 27
bp_pillar.cap_length = 27
bp_pillar.cap_height = 3

bp_pillar.sphere_diameter = 23
bp_pillar.cylinder_height = 3
bp_pillar.cylinder_diameter = 16

bp_pillar.render_magnets = True
bp_pillar.magnet_padding = 1
bp_pillar.magnet_padding_x = 2
bp_pillar.base_height = 5.6
bp_pillar.magnet_width = 20
bp_pillar.make()

ex_pillar = bp_pillar.build()

#show_object(ex_pillar)

cq.exporters.export(ex_pillar, 'stl/fence_pillar_brick.stl')