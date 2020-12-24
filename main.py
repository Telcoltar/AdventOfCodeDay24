import logging
from logging.config import fileConfig
import re
from typing import TextIO


fileConfig("log.ini")

logger = logging.getLogger("dev")


def get_input_data(filname: str) -> list[list[int]]:
    f: TextIO = open(filname)

    tiles: list[list[int]] = []

    for tile in f.readlines():
        tiles.append(parse_string_path(tile))
    f.close()

    return tiles


def parse_string_path(path_str: str) -> list[int]:
    path: list[int] = []
    for m in re.finditer(r"se|e|sw|w|nw|ne", path_str.strip()):
        if m.group(0) == "e":
            path.append(0)
        elif m.group(0) == "ne":
            path.append(1)
        elif m.group(0) == "nw":
            path.append(2)
        elif m.group(0) == "w":
            path.append(3)
        elif m.group(0) == "sw":
            path.append(4)
        elif m.group(0) == "se":
            path.append(5)
    return path


def get_coordinate_from_path(path: list[int]) -> tuple[int, int]:
    currrent_coordinate = (0, 0)
    for move in path:
        if move == 0:
            currrent_coordinate = (currrent_coordinate[0], currrent_coordinate[1] + 2)
        elif move == 1:
            currrent_coordinate = (currrent_coordinate[0] - 1, currrent_coordinate[1] + 1)
        elif move == 2:
            currrent_coordinate = (currrent_coordinate[0] - 1, currrent_coordinate[1] - 1)
        elif move == 3:
            currrent_coordinate = (currrent_coordinate[0], currrent_coordinate[1] - 2)
        elif move == 4:
            currrent_coordinate = (currrent_coordinate[0] + 1, currrent_coordinate[1] - 1)
        elif move == 5:
            currrent_coordinate = (currrent_coordinate[0] + 1, currrent_coordinate[1] + 1)
    return currrent_coordinate


def build_flipped_tiles_set(tiles: list[tuple[int, int]]) -> set[tuple[int, int]]:
    flipped_tiles: set[tuple[int, int]] = set()
    for tile in tiles:
        if tile in flipped_tiles:
            flipped_tiles.remove(tile)
        else:
            flipped_tiles.add(tile)
    return flipped_tiles


def solution_part_1(filename: str) -> int:
    tile_pathes = get_input_data(filename)
    tiles: list[tuple[int, int]] = [get_coordinate_from_path(path_to_tile) for path_to_tile in tile_pathes]
    flipped_tiles: set[tuple[int, int]] = build_flipped_tiles_set(tiles)
    return len(flipped_tiles)


def get_number_of_black_tile_neighbors(black_tile_set: set[tuple[int, int]], coord: tuple[int, int]):
    count: int = 0
    for neighbor in [(0, 2), (-1, 1), (-1, -1), (0, -2), (1, -1), (1, 1)]:
        if (coord[0] + neighbor[0], coord[1] + neighbor[1]) in black_tile_set:
            count += 1
    return count


def cycle(black_tile_dict: set[tuple[int, int]], radius_add: int):
    radius: int = 50 + 2 * radius_add
    new_black_tiles_set: set[tuple[int, int]] = set()
    for i in range(-radius, radius + 1):
        for j in range(-radius, radius + 1):
            if (i + j) % 2 != 0:
                continue
            neighbor_count = get_number_of_black_tile_neighbors(black_tile_dict, (i, j))
            if (i, j) not in black_tile_dict and neighbor_count == 2:
                new_black_tiles_set.add((i, j))
            elif (i, j) in black_tile_dict and 1 <= neighbor_count <= 2:
                new_black_tiles_set.add((i, j))
    return new_black_tiles_set


def solution_part_2(filename: str) -> int:
    tile_pathes = get_input_data(filename)
    tiles: list[tuple[int, int]] = [get_coordinate_from_path(path_to_tile) for path_to_tile in tile_pathes]
    flipped_tiles: set[tuple[int, int]] = build_flipped_tiles_set(tiles)
    for i in range(100):
        flipped_tiles = cycle(flipped_tiles, i)
    return len(flipped_tiles)


if __name__ == '__main__':
    logger.info(solution_part_1("inputData.txt"))
    logger.info(solution_part_2("inputData.txt"))
