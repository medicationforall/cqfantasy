import cadquery as cq
from cqfantasy.tower import TowerTop, RoundBlockUnevenGenerator

bp_tower_top = TowerTop()
bp_tower_top.render_blocks = True
bp_tower_top.bp_block_gen_outside = RoundBlockUnevenGenerator()
bp_tower_top.bp_block_gen_outside.uneven_block_depth = 1
bp_tower_top.bp_block_gen_outside.seed = 'test4'
bp_tower_top.bp_block_gen_outside.block_length = 2.5
bp_tower_top.bp_block_gen_outside.block_ring_count = 30
bp_tower_top.bp_block_gen_outside.row_count = 3
bp_tower_top.bp_block_gen_outside.facing = "outside"

bp_tower_top.bp_block_gen_inside = RoundBlockUnevenGenerator()
bp_tower_top.bp_block_gen_inside.uneven_block_depth = 1
bp_tower_top.bp_block_gen_inside.seed = 'test4'
bp_tower_top.bp_block_gen_inside.block_length = 2.5
bp_tower_top.bp_block_gen_inside.block_ring_count = 30
bp_tower_top.bp_block_gen_inside.row_count = 3
bp_tower_top.bp_block_gen_inside.facing = "inside"

bp_tower_top.diameter = 130
bp_tower_top.height = 30

bp_tower_top.wall_width = 4
bp_tower_top.floor_height = 4
bp_tower_top.top_diameter = 150

bp_tower_top.render_floor_cut = True

bp_tower_top.battlement_width = 20
bp_tower_top.battlement_height = 17
bp_tower_top.battlement_padding = 2.5
bp_tower_top.battlement_count = 5

bp_tower_top.render_magnets = True
bp_tower_top.magnet_diameter = 3.4
bp_tower_top.magnet_height = 2.2
bp_tower_top.magnet_count = 4

bp_tower_top.make()
ex_tower = bp_tower_top.build()
#show_object(ex_tower)

cq.exporters.export(ex_tower,'stl/tower_top_greebled.stl')