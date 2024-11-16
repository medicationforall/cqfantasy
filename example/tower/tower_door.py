import cadquery as cq
from cqfantasy.tower import TowerDoor
from cqterrain.door import TiledDoor

bp_door = TowerDoor()
# properties
bp_door.length = 30
bp_door.width = 27
bp_door.height = 50
bp_door.frame_width = 4
#bp_door.diameter = 130

# blueprints
bp_door.bp_door = TiledDoor()

bp_door.make()

door_ex = bp_door.build()

# show_object(door_ex)

cq.exporters.export(door_ex, 'stl/tower_door.stl')