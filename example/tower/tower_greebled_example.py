import cadquery as cq
from cqfantasy.tower import Tower, LatticeWindow
from cqfantasy.tower import TowerBase,TowerMid, TowerTop, RoundBlockUnevenGenerator

bp_tower = Tower()
bp_tower.base_bp = TowerBase()
bp_tower_base = bp_tower.base_bp
bp_tower_base.render_blocks = True
bp_tower_base.bp_block_gen_outside = RoundBlockUnevenGenerator()
bp_tower_base.bp_block_gen_outside.uneven_block_depth = 1
bp_tower_base.bp_block_gen_outside.seed = 'test4'
bp_tower_base.bp_block_gen_outside.block_length = 2.5
bp_tower_base.bp_block_gen_outside.block_ring_count = 30
bp_tower_base.bp_block_gen_outside.row_count = 9
bp_tower_base.bp_block_gen_outside.facing = "outside"

bp_tower_base.bp_block_gen_inside = RoundBlockUnevenGenerator()
bp_tower_base.bp_block_gen_inside.uneven_block_depth = 1
bp_tower_base.bp_block_gen_inside.seed = 'test4'
bp_tower_base.bp_block_gen_inside.block_length = 2.5
bp_tower_base.bp_block_gen_inside.block_ring_count = 30
bp_tower_base.bp_block_gen_inside.row_count = 9
bp_tower_base.bp_block_gen_inside.facing = "inside"

bp_tower.mid_bp = TowerMid()
bp_tower.mid_bp.render_blocks = True
bp_tower_mid = bp_tower.mid_bp
bp_tower_mid.render_blocks = True
bp_tower_mid.bp_block_gen_outside = RoundBlockUnevenGenerator()
bp_tower_mid.bp_block_gen_outside.uneven_block_depth = 1
bp_tower_mid.bp_block_gen_outside.seed = 'test4'
bp_tower_mid.bp_block_gen_outside.block_length = 2.5
bp_tower_mid.bp_block_gen_outside.block_ring_count = 30
bp_tower_mid.bp_block_gen_outside.row_count = 9
bp_tower_mid.bp_block_gen_outside.facing = "outside"

bp_tower_mid.bp_block_gen_inside = RoundBlockUnevenGenerator()
bp_tower_mid.bp_block_gen_inside.uneven_block_depth = 1
bp_tower_mid.bp_block_gen_inside.seed = 'test4'
bp_tower_mid.bp_block_gen_inside.block_length = 2.5
bp_tower_mid.bp_block_gen_inside.block_ring_count = 30
bp_tower_mid.bp_block_gen_inside.row_count = 9
bp_tower_mid.bp_block_gen_inside.facing = "inside"

bp_tower_mid.bp_window = LatticeWindow()
bp_tower_mid.bp_window.length = 12
bp_tower_mid.bp_window.width = 18
bp_tower_mid.bp_window.height = 40
bp_tower_mid.window_padding = 4
bp_tower_mid.window_count = 4

bp_tower.top_bp = TowerTop()
bp_tower_top = bp_tower.top_bp
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

bp_tower.make()
ex = bp_tower.build()
#show_object(ex)

cq.exporters.export(ex,'stl/tower_greebled_example.stl')