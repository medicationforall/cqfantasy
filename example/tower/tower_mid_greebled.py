import cadquery as cq
from cqfantasy.tower import TowerMid, RoundBlockUnevenGenerator, LatticeWindow

bp_tower = TowerMid()
bp_tower.render_blocks = True
bp_tower.bp_block_gen_outside = RoundBlockUnevenGenerator()
bp_tower.bp_block_gen_outside.uneven_block_depth = 1
bp_tower.bp_block_gen_outside.seed = 'test4'
bp_tower.bp_block_gen_outside.block_length = 2.5
bp_tower.bp_block_gen_outside.block_ring_count = 30
bp_tower.bp_block_gen_outside.row_count = 9
bp_tower.bp_block_gen_outside.facing = "outside"

bp_tower.bp_block_gen_inside = RoundBlockUnevenGenerator()
bp_tower.bp_block_gen_inside.uneven_block_depth = 1
bp_tower.bp_block_gen_inside.seed = 'test4'
bp_tower.bp_block_gen_inside.block_length = 2.5
bp_tower.bp_block_gen_inside.block_ring_count = 30
bp_tower.bp_block_gen_inside.row_count = 9
bp_tower.bp_block_gen_inside.facing = "inside"

bp_tower.diameter = 130
bp_tower.height = 100

bp_tower.wall_width = 4
bp_tower.floor_height = 4

bp_tower.bp_window = LatticeWindow()
bp_tower.bp_window.length = 12
bp_tower.bp_window.width = 18
bp_tower.bp_window.height = 40
bp_tower.window_padding = 4
bp_tower.window_count = 4

bp_tower.render_stairs = True

bp_tower.render_magnets = True
bp_tower.magnet_diameter = 3.4
bp_tower.magnet_height = 2.2
bp_tower.magnet_count = 4

bp_tower.make()
ex_tower = bp_tower.build()
#show_object(ex_tower)

cq.exporters.export(ex_tower,'stl/tower_mid_greebled.stl')