import cadquery as cq
from cqfantasy.fence import BasicBase

bp_base = BasicBase()
bp_base.length = 75
bp_base.width = 20
bp_base.height = 25
bp_base.make()

ex_base = bp_base.build()

#show_object(ex_base)

cq.exporters.export(ex_base, 'stl/fence_basic_base.stl')