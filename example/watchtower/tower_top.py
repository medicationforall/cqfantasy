import cadquery as cq
from cqfantasy.watchtower import TowerTop

bp_top = TowerTop()
bp_top.length:float = 115
bp_top.width:float = 115
bp_top.height:float = 75
bp_top.make()

ex_top = bp_top.build()

#show_object(ex_top)

cq.exporters.export(ex_top, "stl/watch_tower_top.stl")