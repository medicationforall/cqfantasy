import cadquery as cq
from cqfantasy.watchtower import TowerBase

bp_base = TowerBase()
bp_base.length = 125
bp_base.width = 125
bp_base.height = 10
bp_base.make()

ex_base= bp_base.build()

#show_object(ex_base)

cq.exporters.export(ex_base, "stl/watch_tower_base.stl")