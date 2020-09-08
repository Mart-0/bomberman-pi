#!/usr/bin/env python3

chunks = [
    {
        "position": {"x": 1, "y": 1},
        "grid": [
            [3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 0, 3, 0, 3, 0, 3],
            [3, 0, 0, 0, 0, 0, 0, 0],
            [3, 3, 0, 3, 0, 3, 0, 3],
            [3, 0, 0, 0, 0, 0, 0, 0],
            [3, 3, 0, 3, 0, 3, 0, 3],
            [3, 0, 0, 0, 0, 0, 0, 0],
            [3, 3, 0, 3, 0, 3, 0, 3],
        ],
    },
    {
        "position": {"x": 2, "y": 1},
        "grid": [
            [3, 3, 0, 3, 0, 3, 0, 3],
            [0, 3, 0, 3, 0, 3, 0, 3],
            [0, 3, 3, 3, 3, 3, 3, 3],
            [0, 3, 3, 2, 2, 0, 0, 0],
            [0, 3, 3, 2, 2, 0, 0, 0],
            [0, 3, 3, 0, 0, 0, 0, 0],
            [0, 3, 3, 0, 0, 0, 0, 0],
            [0, 3, 3, 0, 0, 0, 0, 0],
        ],
    },
    {
        "position": {"x": 3, "y": 1},
        "grid": [
            [0, 0, 0, 3, 3, 3, 3, 3],
            [0, 3, 3, 3, 0, 3, 3, 3],
            [0, 2, 3, 3, 3, 3, 2, 3],
            [0, 2, 3, 0, 0, 3, 2, 0],
            [0, 2, 3, 0, 0, 3, 2, 0],
            [0, 2, 3, 0, 0, 3, 2, 0],
            [0, 3, 3, 0, 0, 3, 3, 0],
            [0, 3, 3, 0, 0, 0, 0, 0],
        ],
    },
    {
        "position": {"x": 1, "y": 2},
        "grid": [
            [0, 0, 0, 3, 3, 3, 3, 3],
            [0, 3, 3, 3, 0, 3, 3, 3],
            [0, 2, 3, 3, 3, 3, 2, 3],
            [0, 3, 3, 3, 3, 3, 3, 0],
            [0, 3, 3, 3, 3, 3, 3, 0],
            [0, 2, 3, 0, 0, 3, 2, 0],
            [0, 3, 3, 0, 0, 3, 3, 0],
            [0, 3, 3, 0, 0, 0, 0, 0],
        ],
    },
    {
        "position": {"x": 2, "y": 2},
        "grid": [
            [0, 0, 0, 3, 3, 3, 3, 3],
            [0, 3, 3, 3, 0, 3, 3, 3],
            [0, 2, 3, 3, 3, 3, 2, 3],
            [0, 3, 3, 3, 3, 3, 3, 0],
            [0, 3, 3, 3, 3, 3, 3, 0],
            [0, 2, 3, 0, 0, 3, 2, 0],
            [0, 3, 3, 0, 0, 3, 3, 0],
            [0, 3, 3, 0, 0, 0, 0, 0],
        ],
    },
    {
        "position": {"x": 3, "y": 2},
        "grid": [
            [0, 0, 0, 3, 3, 3, 3, 3],
            [0, 3, 3, 3, 0, 3, 3, 3],
            [0, 2, 3, 3, 3, 3, 2, 3],
            [0, 3, 3, 3, 3, 3, 3, 0],
            [0, 3, 3, 3, 3, 3, 3, 0],
            [0, 2, 3, 0, 0, 3, 2, 0],
            [0, 3, 3, 0, 0, 3, 3, 0],
            [0, 3, 3, 0, 0, 0, 0, 0],
        ],
    },
    {
        "position": {"x": 1, "y": 3},
        "grid": [
            [0, 0, 0, 3, 3, 3, 3, 3],
            [0, 3, 3, 3, 0, 3, 3, 3],
            [0, 2, 3, 3, 3, 3, 2, 3],
            [0, 3, 3, 3, 3, 3, 3, 0],
            [0, 3, 3, 3, 3, 3, 3, 0],
            [0, 2, 3, 0, 0, 3, 2, 0],
            [0, 3, 3, 0, 0, 3, 3, 0],
            [0, 3, 3, 0, 0, 0, 0, 0],
        ],
    },
    {
        "position": {"x": 2, "y": 3},
        "grid": [
            [0, 0, 0, 3, 3, 3, 3, 3],
            [0, 3, 3, 3, 0, 3, 3, 3],
            [0, 2, 3, 3, 3, 3, 2, 3],
            [0, 3, 3, 3, 3, 3, 3, 0],
            [0, 3, 3, 3, 3, 3, 3, 0],
            [0, 2, 3, 0, 0, 3, 2, 0],
            [0, 3, 3, 0, 0, 3, 3, 0],
            [0, 3, 3, 0, 0, 0, 0, 0],
        ],
    },
    {
        "position": {"x": 3, "y": 3},
        "grid": [
            [0, 0, 0, 3, 3, 3, 3, 3],
            [0, 3, 3, 3, 0, 3, 3, 3],
            [0, 2, 3, 3, 3, 3, 2, 3],
            [0, 3, 3, 3, 3, 3, 3, 0],
            [0, 3, 3, 3, 3, 3, 3, 0],
            [0, 2, 3, 0, 0, 3, 2, 0],
            [0, 3, 3, 0, 0, 3, 3, 0],
            [0, 3, 3, 0, 0, 0, 0, 0],
        ],
    },
]

#posities en kleuren moeten nog worden aangepast.
users = [
        {"position": {"X": 3, "Y": 3, "x": 2, "y": 6}, "color": (255, 255, 0)},
        {"position": {"X": 3, "Y": 3, "x": 6, "y": 6}, "color": (0, 255, 0)},
        {"position": {"X": 3, "Y": 3, "x": 7, "y": 4}, "color": (0, 255, 255)},
        {"position": {"X": 3, "Y": 3, "x": 7, "y": 1}, "color": (0, 0, 255)},
        {"position": {"X": 3, "Y": 3, "x": 2, "y": 0}, "color": (127, 0, 255)},
        {"position": {"X": 3, "Y": 3, "x": 1, "y": 3}, "color": (255, 0, 255)},
        
]