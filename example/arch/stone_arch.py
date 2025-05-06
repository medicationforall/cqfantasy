import cadquery as cq
from cqfantasy.arch import StoneArch

bp_arch = StoneArch()

# basic arch parameters
bp_arch.length = 30
bp_arch.width = 5
bp_arch.height = 75
bp_arch.outside_margin = 10
bp_arch.inside_margin = 5

# stone arch parameters
bp_arch.stone_count = 8
bp_arch.stone_arch_count = 4
bp_arch.stone_margin = .5
bp_arch.width_margin = .5
bp_arch.stone_modulus = 2
bp_arch.outside_stone_position = 0
bp_arch.stone_arch_modulus = 2
bp_arch.outside_stone_arch_position = 1

bp_arch.make()
ex_arch = bp_arch.build()

#show_object(ex_arch)
cq.exporters.export(ex_arch, 'stl/arch_stone_arch.stl')