#!/usr/bin/env python3

from math import ceil

from boardgamegeek import BGGClient
from boardgamegeek.api import BGGRestrictCollectionTo as restrict

INCH_TO_CM = 2.54  # Exactly!

bgg = BGGClient()

collection = bgg.collection(
    'arnauldvm', own=True,
    exclude_subtype=restrict.BOARD_GAME_EXTENSION, versions=True)
print(f"{collection}")

unknown_boxes_count = 0

longest_dimension = 0

long_boxes_count = 0
long_boxes_total_height = 0

average_boxes_count = 0
average_boxes_total_height = 0

small_boxes_count = 0
small_boxes_total_height = 0

for game in collection:
    print(f"{game.name}")
    if not hasattr(game, 'versions'):
        # print('\tSize unknown!')
        unknown_boxes_count += 1
        continue
    for version in game.versions:
        # print(f"{version}: {version.keys()}")
        width = version['width'] * INCH_TO_CM
        length = version['length'] * INCH_TO_CM
        depth = version['depth'] * INCH_TO_CM
        # print(f"\t{width}x{length}x{depth}")
        dimensions = sorted([width, length, depth])
        thickness = dimensions[0]
        medium = dimensions[1]
        length = dimensions[2]
        if length > longest_dimension:
            longest_dimension = length
        if thickness <= 0:
            # print('\tSize unknown!')
            unknown_boxes_count += 1
            continue
        if length > 35:
            # This is a long box, it does not fit into a 30x30x30 cube
            long_boxes_count += 1
            long_boxes_total_height += thickness
        elif medium > 15:
            # Average box, only 1 fits horizontally in a 30x30x30 cube
            average_boxes_count += 1
            average_boxes_total_height += thickness
        else:
            small_boxes_count += 1
            small_boxes_total_height += thickness

big_cubes_factor = ceil(longest_dimension/30.0)
print(
    f"longest dimension = {longest_dimension} "
    f"=> big cubes = {big_cubes_factor} normal cubes")
big_cubes_count = ceil(long_boxes_total_height/30.0)
print(
    f"long boxes: # = {long_boxes_count}, "
    f"tot height = {long_boxes_total_height} "
    f"-> {big_cubes_count} big cubes"
)
normal_cubes_count = ceil(average_boxes_total_height/30.0)
print(
    f"average boxes: # = {average_boxes_count}, "
    f"tot height = {average_boxes_total_height} "
    f"-> {normal_cubes_count} cubes")
small_cubes_count = ceil(small_boxes_total_height/30.0
                         )
print(
    f"small boxes: # = {small_boxes_count}, "
    f"tot height = {small_boxes_total_height} "
    f"-> {small_cubes_count} small cubes")
print(f"unknown boxes: # = {unknown_boxes_count}"
      )

total_cubes_count = big_cubes_factor*big_cubes_count + \
    normal_cubes_count + ceil(small_cubes_count/2.0)
actual_count_estimate = ceil(
    1.0*total_cubes_count /
    (len(collection)-unknown_boxes_count)*len(collection))
print(
    f"total boxes required > {total_cubes_count}, "
    f"estimate {actual_count_estimate}"
)
