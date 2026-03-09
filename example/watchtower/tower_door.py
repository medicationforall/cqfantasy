import cadquery as cq
from cqfantasy.watchtower import TowerDoor

bp_door = TowerDoor()
bp_door.make()
ex_door = bp_door.build()
ex_cross = bp_door.build_cross_section()

#show_object(ex_door)
#show_object(ex_cross)

cq.exporters.export(ex_door, "stl/watch_tower_door.stl")