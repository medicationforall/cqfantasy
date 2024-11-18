import cadquery as cq
from cqfantasy.tower import Tower, LatticeWindow
from cqfantasy.tower import TowerBase,TowerMid, TowerTop, RoundBlockAltGenerator, RoundBlockUnevenGenerator, TileGenerator
from cqterrain.tile import dwarf_star

def make_dwarf_star(
    length:float, 
    width:float, 
    height:float
) -> cq.Workplane:
    tile = dwarf_star(
        length, 
        width, 
        height
        #set hardcoded overrides here
    )
    return tile

bp_tower = Tower()

#----------------
# Base
bp_tower.base_bp = TowerBase()
bp_tower_base = bp_tower.base_bp
bp_tower_base.height = 75
bp_tower_base.stair_count = 8
bp_tower_base.render_blocks = True
bp_tower_base.magnet_count = 8
bp_tower_base.bp_block_gen_outside = RoundBlockAltGenerator()
bp_tower_base.bp_block_gen_outside.uneven_block_depth = 1
bp_tower_base.bp_block_gen_outside.seed = 'test4'
bp_tower_base.bp_block_gen_outside.block_length = 2.5
bp_tower_base.bp_block_gen_outside.block_ring_count = 28
bp_tower_base.bp_block_gen_outside.row_count = 7
bp_tower_base.bp_block_gen_outside.modulus_even = 0
bp_tower_base.bp_block_gen_outside.facing = "outside"
bp_tower_base.bp_block_gen_outside.block_modulus = 7
bp_tower_base.bp_block_gen_outside.block_remainder = 4

bp_tower_base.bp_block_gen_inside = RoundBlockUnevenGenerator()
bp_tower_base.bp_block_gen_inside.uneven_block_depth = 1
bp_tower_base.bp_block_gen_inside.seed = 'test4'
bp_tower_base.bp_block_gen_inside.block_length = 2.5
bp_tower_base.bp_block_gen_inside.block_ring_count = 28
bp_tower_base.bp_block_gen_inside.row_count = 7
bp_tower_base.bp_block_gen_inside.modulus_even = 0
bp_tower_base.bp_block_gen_inside.facing = "inside"

bp_tower_base.bp_tile_gen = TileGenerator()
bp_tower_base.bp_tile_gen.diameter = 100
bp_tower_base.bp_tile_gen.tile_length = 20
bp_tower_base.bp_tile_gen.tile_width = 20
bp_tower_base.bp_tile_gen.tile_height = 3
bp_tower_base.bp_tile_gen.tile_padding = .5
bp_tower_base.bp_tile_gen.overflow = 21
bp_tower_base.bp_tile_gen.make_tile_method = make_dwarf_star

#----------------
# Mid
bp_tower.mid_bp = TowerMid()
bp_tower_mid = bp_tower.mid_bp
bp_tower_mid.height = 75
bp_tower_mid.stair_count = 8
bp_tower_mid.render_blocks = True
bp_tower_mid.magnet_count = 8
bp_tower_mid.bp_block_gen_outside = RoundBlockAltGenerator()
bp_tower_mid.bp_block_gen_outside.uneven_block_depth = 1
bp_tower_mid.bp_block_gen_outside.seed = 'test4'
bp_tower_mid.bp_block_gen_outside.block_length = 2.5
bp_tower_mid.bp_block_gen_outside.block_ring_count = 28
bp_tower_mid.bp_block_gen_outside.row_count = 9
bp_tower_mid.bp_block_gen_outside.modulus_even = 1
bp_tower_mid.bp_block_gen_outside.facing = "outside"
bp_tower_mid.bp_block_gen_outside.block_modulus = 7
bp_tower_mid.bp_block_gen_outside.block_remainder = 4

bp_tower_mid.bp_block_gen_inside = RoundBlockUnevenGenerator()
bp_tower_mid.bp_block_gen_inside.uneven_block_depth = 1
bp_tower_mid.bp_block_gen_inside.seed = 'test4'
bp_tower_mid.bp_block_gen_inside.block_length = 2.5
bp_tower_mid.bp_block_gen_inside.block_ring_count = 28
bp_tower_mid.bp_block_gen_inside.row_count = 9
bp_tower_mid.bp_block_gen_inside.modulus_even = 1
bp_tower_mid.bp_block_gen_inside.facing = "inside"

bp_tower_mid.bp_window = LatticeWindow()
bp_tower_mid.bp_window.length = 20
bp_tower_mid.bp_window.width = 4
bp_tower_mid.bp_window.height = 40
bp_tower_mid.window_padding = 4
bp_tower_mid.window_count = 4

bp_tower_mid.bp_tile_gen = TileGenerator()
bp_tower_mid.bp_tile_gen.diameter = 100
bp_tower_mid.bp_tile_gen.tile_length = 20
bp_tower_mid.bp_tile_gen.tile_width = 20
bp_tower_mid.bp_tile_gen.tile_height = 3
bp_tower_mid.bp_tile_gen.tile_padding = .5
bp_tower_mid.bp_tile_gen.overflow = 21
bp_tower_mid.bp_tile_gen.make_tile_method = make_dwarf_star

#----------------
# Top
bp_tower.top_bp = TowerTop()
bp_tower_top = bp_tower.top_bp
bp_tower_top.render_blocks = True
bp_tower_top.magnet_count = 8
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

bp_tower_top.bp_tile_gen = TileGenerator()
bp_tower_top.bp_tile_gen.diameter = 100
bp_tower_top.bp_tile_gen.tile_length = 20
bp_tower_top.bp_tile_gen.tile_width = 20
bp_tower_top.bp_tile_gen.tile_height = 3
bp_tower_top.bp_tile_gen.tile_padding = .5
bp_tower_top.bp_tile_gen.overflow = 21
bp_tower_top.bp_tile_gen.make_tile_method = make_dwarf_star

bp_tower.make()
ex = bp_tower.build()
#show_object(ex)

cq.exporters.export(ex,'stl/tower_alt_greebled_example.stl')

base = bp_tower_base.build()
cq.exporters.export(base,'stl/tower_alt_greebled_base.stl')

mid = bp_tower_mid.build()
cq.exporters.export(mid,'stl/tower_alt_greebled_mid.stl')

top = bp_tower_top.build()
cq.exporters.export(top,'stl/tower_alt_greebled_top.stl')