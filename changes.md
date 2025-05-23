## Main Wip

## 2.1.0
* Upped minimum python version to 3.10
* Added arch package
  * Added arch
  * Added BasicArch
  * Added StoneArch
* Added door package
  * Added VDoor
  * Added ArchDoor
* Added build return annotations for tower classes.
* Modified tower TowerDoor to have better custom outline support.
* Wrote Documentation for Arch, Door, House, and House Wall
* Added various missing type annotations when I spotted them.
* Updated README.md

## 2.0.0
* Updated cqterrain to version 3.4.1
* Cleaned up instances where I was setting the callback parameter for workplane.eachpoint invocations.
  * https://github.com/CadQuery/cadquery/issues/1395
* Refactored code and moved various wall components to house_wall module.
  * tudor_wall
  * WallStuccoBrick
  * WallTudor
  * WallTudorPaneling 
* Added house BodyGreebled
* Added house_wall SplitWall
* Added house example house_greebled_two
* Flipped house_wall tudor_wall orientation
* bug fix - house BodyGreebled fixed internal wall orientation
* house_wall walltudor added render_top_bar and render_bottom_bar parameters.
* tower BaseSection added floor_cut_length_rotate parameter to define the size of the floor hole made for the stairs.
* tower TowerDoor added y_offset parameter to position the door along the yaxis.

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