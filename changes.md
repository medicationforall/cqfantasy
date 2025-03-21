## Main Wip

## 2.0.0
* Refactored code and moved various wall components to house_wall module.
  * tudor_wall
  * WallStuccoBrick
  * WallTudor
  * WallTudorPaneling 
* Added house BodyGreebled
* Added house_wall SplitWall
* Added house example house_greebled_two

## 1.5.0
* Updated house documentation screenshots
* Added house WallTudor
* Added house WallStuccoBrick
* Added house WallTudorPaneling
* Added Calculate methods to house body

## 1.4.0
* Added house ShingleRoof
* Upped ctqterrain to 3.3.0
* houe Roof added overhang_inset parameters

## 1.3.0
* Added missing license blocks
* Added house StuccoBrickBody
* Added house TudorBody
* Added house TudorSplitBody
* Added house TileGenerator
* Upped ctqterrain to 3.2.1

## 1.2.0
* Added house package
  * Added Body
  * Added Roof
  * Added House
  * Added house examples
  * Added house documentation
* Upped ctqterrain to 3.1.0

## 1.1.0
* Added wall package
  * Added tileGenerator
* Fixed tower.TileGenerator big the x and y count the grid were getting messed up do to order of operations (rookie mistake)
  * the whole problem with hidden because of the intersect with a cylinder which hid the excess tiles
* Upped ctqterrain to 2.4.0

## 1.0.1
* Remove old code
* Added RoundBlockAltGenerator
* Added RoundBlockUnevenStuccoGenerator
* Added Examples

## 1.0.0
* Added BaseSection to store common code between TowerBase, TowerMid, and TowerTop
* Refactored TowerBase, TowerMid, and TowerTop to use BaseSection
* Fixed window placement
* Fixed Stair Placement
* Fixed door placement
* Upped ctqterrain to 1.2.4
* Added RoundBlockUnevenGenerator
* Fixed Examples

## 0.1.6
* Added RoundBlockGenerator
* Integrated RoundBlockGenerator into TowerBase, TowerMid, and TowerTop

## 0.1.5
* Modified magnet size for printing

## 0.1.4
* TowerBase added stair_count parameter
  * Default to FrameWindow
  * Added window code 
* TowerMid added stair_count parameter

## 0.1.3
* Upped cqterrain version 1.2.3
* Added tile_generator example
* Added tile_generator_dwarf_star example
* Added TileGenerator documentation
* Updated documentation
* Added TowerDoor
  * Added tower_door example, documentation, and stl

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