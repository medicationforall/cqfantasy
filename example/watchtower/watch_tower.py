import cadquery as cq
from cqfantasy.watchtower import WatchTower

bp_tower = WatchTower()
bp_tower.make()

ex_tower = bp_tower.build()
#ex_cut = bp_tower.build_cut()
#show_object(ex_tower.cut(ex_cut))

#show_object(ex_tower)

cq.exporters.export(ex_tower, "stl/watch_tower.stl")