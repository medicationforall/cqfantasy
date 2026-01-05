import cadquery as cq
from cqfantasy.fence import BasicPillar

bp_pillar = BasicPillar()
bp_pillar.length = 30
bp_pillar.width = 30
bp_pillar.height = 45
bp_pillar.make()

ex_pillar = bp_pillar.build()

#show_object(ex_base)

cq.exporters.export(ex_pillar, 'stl/fence_basic_pillar.stl')