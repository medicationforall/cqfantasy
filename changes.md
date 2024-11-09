## Main Wip
## 0.1.3
* Upped cqterrain version 1.2.2
* Added tile_generator example
* Added tile_generator_dwarf_star example

## 0.1.2
* Added magnets utility
* TowerBase, TowerMid, TowerTop create magnet cutouts.
* Added TileGenerator proof of concept.

## 0.1.1
* TowerBase
  * Move where make stairs is called
* Added TowerMidGreebled
* Added TowerTopGreebled
* Added UnevenBlocks mixin
* TowerBaseGreeble performance improvement
  * remove dupe build
  * when iterating block rows add them instead of unioning them
  * Changes how make_blocks unions to base.
  * Refactored code to use UnevenBlocks mixin

## 0.1.0
* Initial version