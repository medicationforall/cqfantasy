import cadquery as cq
from cqfantasy.tower import TowerBaseGreebled

bp_tower_base = TowerBaseGreebled()
bp_tower_base.uneven_block_depth = 1
bp_tower_base.seed = 'test4'
bp_tower_base.render_base = True
bp_tower_base.render_blocks = True
bp_tower_base.render_outside_blocks = True
bp_tower_base.render_inside_blocks = True

bp_tower_base.diameter = 130
bp_tower_base.base_diameter = 150
bp_tower_base.height = 100

bp_tower_base.wall_width = 4
bp_tower_base.floor_height = 4

bp_tower_base.block_length = 5
bp_tower_base.block_width = 14
bp_tower_base.block_height = 10

bp_tower_base.block_ring_count = 30
bp_tower_base.even_ring_rotate = 6

bp_tower_base.render_stairs = True
bp_tower_base.render_window_outline = False

bp_tower_base.window_length = 12
bp_tower_base.window_width = 18
bp_tower_base.window_height = 40
bp_tower_base.window_padding = 6
bp_tower_base.window_count = 2

bp_tower_base.door_length = 30
bp_tower_base.door_width = 27
bp_tower_base.door_height = 50
bp_tower_base.door_padding = 7
bp_tower_base.door_count = 1
bp_tower_base.make()
ex_tower = bp_tower_base.build()
#show_object(ex_tower)

cq.exporters.export(ex_tower,'stl/tower_base_greebled.stl')