import cadquery as cq
from cqfantasy.tower import LatticeWindow

bp_window = LatticeWindow()
bp_window.frame_width = 2
bp_window.frame_margin = 2
bp_window.lattice_angle = 45
bp_window.lattice_width = 1.5
bp_window.lattice_height = 1.3
bp_window.tile_size = 4.5

bp_window.length = 25
bp_window.width = 2
bp_window.height = 30
bp_window.inner_height_margin = 15

#bp_window.diameter = 130
#bp_window.render_outline = False
bp_window.make()

window = bp_window.build()

#show_object(window)

cq.exporters.export(window, 'stl/tower_lattice_window.stl')