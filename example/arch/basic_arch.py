import cadquery as cq
from cqfantasy.arch import BasicArch

bp_arch = BasicArch()

bp_arch.length = 30
bp_arch.width = 5
bp_arch.height = 75
bp_arch.outside_margin = 10
bp_arch.inside_margin = 5

bp_arch.make()
ex_arch = bp_arch.build()

#show_object(ex_arch)
cq.exporters.export(ex_arch, 'stl/arch_basic_arch.stl')