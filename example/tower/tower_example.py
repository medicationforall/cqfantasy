import cadquery as cq
from cqfantasy.tower import Tower, LatticeWindow

bp_tower = Tower()
bp_tower.base_bp.render_blocks = True
bp_tower.mid_bp.render_blocks = True
bp_tower.mid_bp.bp_window = LatticeWindow()
bp_tower.top_bp.render_blocks = True
bp_tower.make()
ex = bp_tower.build()
#show_object(ex)

cq.exporters.export(ex,'stl/tower_example.stl')