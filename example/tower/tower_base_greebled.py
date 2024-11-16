import cadquery as cq
from cqfantasy.tower import TowerBase, RoundBlockUnevenGenerator

bp_tower_base = TowerBase()
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

bp_tower_base.diameter = 130
bp_tower_base.base_diameter = 150
bp_tower_base.height = 100

bp_tower_base.wall_width = 4
bp_tower_base.floor_height = 4

bp_tower_base.render_stairs = True

if bp_tower_base.bp_window:
    bp_tower_base.bp_window.length = 12
    bp_tower_base.bp_window.width = 18
    bp_tower_base.bp_window.height = 40
bp_tower_base.window_padding = 6
bp_tower_base.window_count = 2

if bp_tower_base.bp_door:
    bp_tower_base.bp_door.length = 30
    bp_tower_base.bp_door.width = 27
    bp_tower_base.bp_door.height = 50
bp_tower_base.door_padding = 7
bp_tower_base.door_count = 1

bp_tower_base.render_magnets = True
bp_tower_base.magnet_diameter = 3.4
bp_tower_base.magnet_height = 2.2
bp_tower_base.magnet_count = 4

bp_tower_base.make()
ex_tower = bp_tower_base.build()
#show_object(ex_tower)

cq.exporters.export(ex_tower,'stl/tower_base_greebled.stl')