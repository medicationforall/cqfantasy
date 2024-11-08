import cadquery as cq
from cqfantasy.tower import TowerMidGreebled

bp_tower = TowerMidGreebled()
bp_tower.uneven_block_depth = 1
bp_tower.seed = 'test4'
bp_tower.render_mid = True
bp_tower.render_blocks = True
bp_tower.render_outside_blocks = True
bp_tower.render_inside_blocks = True

bp_tower.diameter = 130
bp_tower.height = 100

bp_tower.wall_width = 4
bp_tower.floor_height = 4

bp_tower.block_length = 5
bp_tower.block_width = 14
bp_tower.block_height = 10

bp_tower.block_ring_count = 30
bp_tower.even_ring_rotate = 6

bp_tower.render_stairs = True
bp_tower.render_window_outline = False

bp_tower.window_length = 20
bp_tower.window_width = 12
bp_tower.window_height = 40
bp_tower.window_padding = 4
bp_tower.window_count = 4

bp_tower.make()
ex_tower = bp_tower.build()
#show_object(ex_tower)

cq.exporters.export(ex_tower,'stl/tower_mid_greebled.stl')