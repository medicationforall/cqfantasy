import cadquery as cq
from cqfantasy.door import VDoor

bp_door = VDoor()

bp_door.length = 30
bp_door.width = 5
bp_door.height = 75

bp_door.v_margin = 1
bp_door.v_width = 15
bp_door.v_intersect = 10

bp_door.door_chamfer = 0.5

bp_door.make()

door_ex = bp_door.build()

# show_object(door_ex)
cq.exporters.export(door_ex, 'stl/door_v_door.stl')