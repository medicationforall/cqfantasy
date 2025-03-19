import time

#------------------------------
## House Examples
print('House Examples')
import example.house.body
import example.house.roof
import example.house.house
import example.house.house_plate
import example.house.house_cut_away
import example.house.stucco_brick_body
import example.house.tudor_split_body
import example.house.tudor_body
import example.house.body_types
import example.house.house_greebled
import example.house.tile_generator
import example.house.shingle_roof


#------------------------------
## House wall Examples
print('House Examples')
import example.house_wall.tudor_wall
import example.house_wall.wall_tudor_class
import example.house_wall.wall_tudor_paneling_class
import example.house_wall.wall_stucco_brick_class
import example.house_wall.wall_split_class

#------------------------------
## Wall Examples
print('Wall Tile Examples')
import example.wall.tile_generator

#------------------------------

print('Utility Examples')
import example.tower.cut_cylinder

print('Window Examples')
import example.tower.frame_window
import example.tower.lattice_window

print('Door Examples')
import example.tower.tower_door

print('Tower Tile Examples')
import example.tower.tile_generator
import example.tower.tile_generator_dwarf_star

print('Block Examples')
import example.tower.round_block_generator
import example.tower.round_block_uneven_generator
import example.tower.round_block_alt_generator
import example.tower.round_block_stucco_generator
#------------------------------
## Tower Examples


#------------------------------
run_base = False

if run_base:
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

#------------------------------
run_greebled = False

if run_greebled:
    print('start tower_greebled_example')
    t1 = time.perf_counter(), time.process_time()
    import example.tower.tower_greebled_example
    t2 = time.perf_counter(), time.process_time()
    print(f" Real time: {t2[0] - t1[0]:.2f} seconds")
    print(f" CPU time: {t2[1] - t1[1]:.2f} seconds")
    print('end tower_greebled_example')


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


#-----------------------------------
run_alt = False

if run_alt:
    print('start tower_alt_greebled_example')
    t1 = time.perf_counter(), time.process_time()
    import example.tower.tower_alt_greebled_example
    t2 = time.perf_counter(), time.process_time()
    print(f" Real time: {t2[0] - t1[0]:.2f} seconds")
    print(f" CPU time: {t2[1] - t1[1]:.2f} seconds")
    print('end tower_alt_greebled_example')

#-----------------------------------
run_stucco = False

if run_stucco:
    print('start tower_stucco_example')
    t1 = time.perf_counter(), time.process_time()
    import example.tower.tower_stucco_example
    t2 = time.perf_counter(), time.process_time()
    print(f" Real time: {t2[0] - t1[0]:.2f} seconds")
    print(f" CPU time: {t2[1] - t1[1]:.2f} seconds")
    print('end tower_stucco_example')

#-----------------------------------
