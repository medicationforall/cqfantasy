import cadquery as cq
from cqfantasy.tower import TowerMid, LatticeWindow

bp_tower_mid = TowerMid()
# properties
bp_tower_mid.diameter = 130
bp_tower_mid.height = 100

bp_tower_mid.wall_width = 4
bp_tower_mid.floor_height = 4

bp_tower_mid.block_length = 5
bp_tower_mid.block_width = 14
bp_tower_mid.block_height = 10

bp_tower_mid.block_ring_count = 30
bp_tower_mid.even_ring_rotate = 6

bp_tower_mid.render_blocks = True
bp_tower_mid.render_stairs = True
bp_tower_mid.render_window_outline = False

bp_tower_mid.window_length = 20
bp_tower_mid.window_width = 12
bp_tower_mid.window_height = 40
bp_tower_mid.window_padding = 4
bp_tower_mid.window_count = 4

# blueprints
bp_tower_mid.bp_window = LatticeWindow()

bp_tower_mid.make()
ex_tower = bp_tower_mid.build()
#show_object(ex_tower)

cq.exporters.export(ex_tower,'stl/tower_mid.stl')