
import cadquery as cq
from cqfantasy.door import ArchDoor

bp_door = ArchDoor()

bp_door.length = 50
bp_door.width = 7
bp_door.height = 75
bp_door.door_inset = 2

bp_door.make()
ex_door = bp_door.build()

#show_object(ex_door)
cq.exporters.export(ex_door, "stl/door_arch_door.stl")