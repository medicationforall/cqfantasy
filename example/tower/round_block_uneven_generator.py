import cadquery as cq
from cqfantasy.tower import RoundBlockUnevenGenerator

bp_blocks = RoundBlockUnevenGenerator()
bp_blocks.top_diameter = 150
bp_blocks.base_diameter = 150
bp_blocks.height = 100

bp_blocks.margin = (1,1.5)
bp_blocks.block_length = 2.5
bp_blocks.block_ring_count = 30
bp_blocks.facing = "outside" #inside

bp_blocks.make()

ex_blocks = bp_blocks.build()

# show_object(ex_blocks)
cq.exporters.export(ex_blocks,'stl/round_block_uneven_generator.stl')