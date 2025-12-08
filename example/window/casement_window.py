import cadquery as cq
from cqfantasy.window import CasementWindow

bp_window = CasementWindow()
bp_window.length = 25
bp_window.width = 2
bp_window.height = 30
bp_window.inner_height_margin = 15
bp_window.frame_columns = 2 
bp_window.frame_rows = 2
bp_window.frame_width=2 
bp_window.grill_width=1.5
bp_window.grill_height=1.5

#bp_window.diameter = 130
#bp_window.render_outline = False

bp_window.frame_width = 2
bp_window.frame_margin = 2
bp_window.render_cylinder = True
bp_window.make()

window = bp_window.build()
window_cut = bp_window.build_cut()

#show_object(window)
cq.exporters.export(window, 'stl/CasementWindow.stl')