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
        {"position": {"X": 3, "Y": 3, "x": 2, "y": 2}, "color": (255, 255, 255)},
        {"position": {"X": 3, "Y": 3, "x": 2, "y": 2}, "color": (255, 255, 255)},
        {"position": {"X": 3, "Y": 3, "x": 2, "y": 2}, "color": (255, 255, 255)},
        {"position": {"X": 3, "Y": 3, "x": 2, "y": 2}, "color": (255, 255, 255)},
        {"position": {"X": 3, "Y": 3, "x": 2, "y": 2}, "color": (255, 255, 255)},
        {"position": {"X": 3, "Y": 3, "x": 2, "y": 2}, "color": (255, 255, 255)},
        
]
