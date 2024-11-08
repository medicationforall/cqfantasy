import cadquery as cq
from cqfantasy.tower import TowerTop

bp_tower_top = TowerTop()
# properties
bp_tower_top.diameter = 130
bp_tower_top.height = 30

bp_tower_top.wall_width = 4
bp_tower_top.floor_height = 4
bp_tower_top.top_diameter = 150

bp_tower_top.block_length = 5
bp_tower_top.block_width = 14
bp_tower_top.block_height = 8.5

bp_tower_top.block_ring_count = 30
bp_tower_top.even_ring_rotate = 6

bp_tower_top.render_blocks = True
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

cq.exporters.export(ex_tower,'stl/tower_top.stl')