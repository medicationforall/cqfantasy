import time

print('start tower_greebled_example')
t1 = time.perf_counter(), time.process_time()
import example.tower.tower_greebled_example
t2 = time.perf_counter(), time.process_time()
print(f" Real time: {t2[0] - t1[0]:.2f} seconds")
print(f" CPU time: {t2[1] - t1[1]:.2f} seconds")
print('end tower_greebled_example')


print('Unility Examples')
import example.tower.cut_cylinder

print('Window Examples')
import example.tower.frame_window
import example.tower.lattice_window

print('Tile Examples')
import example.tower.tile_generator
import example.tower.tile_generator_dwarf_star

print('Tower Examples')
print('start tower_example')
t1 = time.perf_counter(), time.process_time()
import example.tower.tower_example
t2 = time.perf_counter(), time.process_time()
print(f" Real time: {t2[0] - t1[0]:.2f} seconds")
print(f" CPU time: {t2[1] - t1[1]:.2f} seconds")
print('end tower_example')

print('start tower_base')
t1 = time.perf_counter(), time.process_time()
import example.tower.tower_base
t2 = time.perf_counter(), time.process_time()
print(f" Real time: {t2[0] - t1[0]:.2f} seconds")
print(f" CPU time: {t2[1] - t1[1]:.2f} seconds")
print('end tower_base')

print('start tower_mid')
t1 = time.perf_counter(), time.process_time()
import example.tower.tower_mid
t2 = time.perf_counter(), time.process_time()
print(f" Real time: {t2[0] - t1[0]:.2f} seconds")
print(f" CPU time: {t2[1] - t1[1]:.2f} seconds")
print('end tower_mid')

print('start tower_top')
t1 = time.perf_counter(), time.process_time()
import example.tower.tower_top
t2 = time.perf_counter(), time.process_time()
print(f" Real time: {t2[0] - t1[0]:.2f} seconds")
print(f" CPU time: {t2[1] - t1[1]:.2f} seconds")
print('end tower_top')


print('Tower Greebled Examples')
print('start tower_base_greebled')
t1 = time.perf_counter(), time.process_time()
import example.tower.tower_base_greebled
t2 = time.perf_counter(), time.process_time()
print(f" Real time: {t2[0] - t1[0]:.2f} seconds")
print(f" CPU time: {t2[1] - t1[1]:.2f} seconds")
print('end tower_base_greebled')

print('start tower_mid_greebled')
t1 = time.perf_counter(), time.process_time()
import example.tower.tower_mid_greebled
t2 = time.perf_counter(), time.process_time()
print(f" Real time: {t2[0] - t1[0]:.2f} seconds")
print(f" CPU time: {t2[1] - t1[1]:.2f} seconds")
print('end tower_mid_greebled')

print('start tower_top_greebled')
t1 = time.perf_counter(), time.process_time()
import example.tower.tower_top_greebled
t2 = time.perf_counter(), time.process_time()
print(f" Real time: {t2[0] - t1[0]:.2f} seconds")
print(f" CPU time: {t2[1] - t1[1]:.2f} seconds")
print('end tower_top_greebled')


