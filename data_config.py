#!/usr/bin/env python3

chunks = [
    {
        "position": {"x": 0, "y": 0},
        "grid": [
            [3, 3, 3, 3, 3, 3, 3, 3],
            [3, 0, 0, 1, 1, 3, 1, 3],
            [3, 0, 3, 3, 1, 1, 1, 0],
            [3, 1, 3, 3, 1, 3, 1, 3],
            [3, 1, 1, 1, 1, 3, 1, 0],
            [3, 3, 1, 3, 3, 3, 3, 3],
            [3, 1, 1, 1, 1, 3, 1, 0],
            [3, 3, 0, 3, 0, 3, 0, 3],
        ],
    },
    {
        "position": {"x": 0, "y": 1},
        "grid": [
            [3, 3, 1, 3, 0, 3, 0, 3],
            [3, 3, 1, 3, 1, 3, 1, 3],
            [3, 0, 0, 1, 1, 1, 1, 0],
            [3, 0, 3, 1, 3, 3, 1, 3],
            [3, 0, 3, 1, 3, 3, 1, 3],
            [3, 1, 1, 1, 1, 1, 1, 0],
            [3, 3, 1, 3, 1, 3, 1, 3],
            [3, 3, 0, 3, 0, 3, 0, 3],
        ],
    },
    {
        "position": {"x": 0, "y": 2},
        "grid": [
            [3, 3, 0, 3, 0, 3, 0, 3],
            [3, 1, 1, 1, 1, 3, 1, 0],
            [3, 3, 1, 3, 3, 3, 3, 3],
            [3, 1, 1, 1, 1, 3, 1, 0],
            [3, 1, 3, 3, 1, 3, 1, 3],
            [3, 0, 3, 3, 1, 1, 1, 0],
            [3, 0, 0, 1, 1, 3, 1, 3],
            [3, 3, 3, 3, 3, 3, 3, 3],
        ],
    },
    {
        "position": {"x": 1, "y": 0},
        "grid": [
            [3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 1, 1, 0, 0, 3, 3],
            [0, 1, 1, 3, 3, 0, 1, 0],
            [3, 3, 1, 1, 1, 1, 3, 3],
            [1, 1, 1, 3, 3, 1, 1, 0],
            [3, 3, 1, 3, 3, 1, 3, 3],
            [0, 1, 1, 1, 1, 1, 1, 0],
            [3, 3, 0, 3, 3, 0, 3, 3],
        ],
    },
    {
        "position": {"x": 1, "y": 1},
        "grid": [
            [3, 3, 0, 3, 3, 0, 3, 3],
            [3, 3, 1, 3, 3, 1, 3, 3],
            [0, 1, 1, 1, 1, 1, 1, 0],
            [3, 3, 1, 3, 3, 1, 3, 3],
            [3, 3, 1, 3, 3, 1, 3, 3],
            [0, 1, 1, 1, 1, 1, 1, 0],
            [3, 3, 1, 3, 3, 1, 3, 3],
            [3, 3, 0, 3, 3, 0, 3, 3],
        ],
    },
    {
        "position": {"x": 1, "y": 2},
        "grid": [
            [3, 3, 0, 3, 3, 0, 3, 3],
            [0, 1, 1, 1, 1, 1, 1, 0],
            [3, 3, 1, 3, 3, 1, 3, 3],
            [0, 1, 1, 3, 3, 1, 1, 0],
            [3, 3, 1, 1, 1, 1, 3, 3],
            [0, 1, 1, 3, 3, 0, 1, 0],
            [3, 3, 1, 1, 0, 0, 3, 3],
            [3, 3, 3, 3, 3, 3, 3, 3],
        ],
    },
    {
        "position": {"x": 2, "y": 0},
        "grid": [
            [3, 3, 3, 3, 3, 3, 3, 3],
            [3, 1, 3, 1, 1, 0, 0, 3],
            [0, 1, 1, 1, 3, 3, 0, 3],
            [3, 1, 3, 1, 3, 3, 1, 3],
            [0, 1, 3, 1, 1, 1, 1, 3],
            [3, 3, 3, 3, 3, 1, 3, 3],
            [0, 1, 3, 1, 1, 1, 1, 3],
            [3, 0, 3, 0, 3, 0, 3, 3],
        ],
    },
    {
        "position": {"x": 2, "y": 1},
        "grid": [
            [3, 0, 3, 0, 3, 0, 3, 3],
            [3, 1, 3, 1, 3, 1, 3, 3],
            [0, 1, 1, 1, 1, 1, 1, 3],
            [3, 1, 3, 3, 1, 3, 1, 3],
            [3, 1, 3, 3, 1, 3, 0, 3],
            [0, 1, 1, 1, 0, 0, 0, 3],
            [3, 1, 3, 1, 3, 0, 3, 3],
            [3, 0, 3, 0, 3, 0, 3, 3],
        ],
    },
    {
        "position": {"x": 2, "y": 2},
        "grid": [
            [3, 0, 3, 0, 3, 0, 3, 3],
            [0, 1, 3, 1, 1, 1, 1, 3],
            [3, 3, 3, 3, 3, 1, 3, 3],
            [0, 1, 3, 1, 1, 1, 1, 3],
            [3, 1, 3, 1, 3, 3, 1, 3],
            [0, 1, 1, 1, 3, 3, 0, 3],
            [3, 1, 3, 1, 1, 0, 0, 3],
            [3, 3, 3, 3, 3, 3, 3, 3],
        ],
    },
]

players = [
    {
        "id": 1,
        "alive": 1,
        "position": {"X": 0, "Y": 0, "x": 1, "y": 1},
        "color": (255, 255, 0),
    },
    {
        "id": 2,
        "alive": 1,
        "position": {"X": 0, "Y": 1, "x": 1, "y": 2},
        "color": (0, 255, 0),
    },
    {
        "id": 3,
        "alive": 1,
        "position": {"X": 0, "Y": 2, "x": 1, "y": 6},
        "color": (255, 165, 0),
    },
    {
        "id": 4,
        "alive": 1,
        "position": {"X": 2, "Y": 0, "x": 6, "y": 1},
        "color": (0, 0, 255),
    },
    {
        "id": 5,
        "alive": 1,
        "position": {"X": 2, "Y": 1, "x": 6, "y": 5},
        "color": (0, 191, 255),
    },
    {
        "id": 6,
        "alive": 1,
        "position": {"X": 2, "Y": 2, "x": 6, "y": 6},
        "color": (255, 0, 255),
    },
]