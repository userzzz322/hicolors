#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
=============================================================================
[ HICOLORS ]
A lightweight, zero-dependency color utility for terminal graphics.
=============================================================================
"""

import sys

class AnsiStyles:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"

class Color:
    def __init__(self, r: int, g: int, b: int):
        self.r = max(0, min(255, r))
        self.g = max(0, min(255, g))
        self.b = max(0, min(255, b))

    @classmethod
    def from_hex(cls, hex_str: str):
        hex_str = hex_str.lstrip('#')
        if len(hex_str) == 3:
            hex_str = ''.join([c*2 for c in hex_str])
        r = int(hex_str[0:2], 16)
        g = int(hex_str[2:4], 16)
        b = int(hex_str[4:6], 16)
        return cls(r, g, b)

    def to_hex(self) -> str:
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"

    def fg_ansi(self) -> str:
        return f"\033[38;2;{self.r};{self.g};{self.b}m"

    def bg_ansi(self) -> str:
        return f"\033[48;2;{self.r};{self.g};{self.b}m"

    def paint(self, text: str, bold: bool = False) -> str:
        style = AnsiStyles.BOLD if bold else ""
        return f"{style}{self.fg_ansi()}{text}{AnsiStyles.RESET}"

    def __repr__(self):
        return f"Color(r={self.r}, g={self.g}, b={self.b}, hex='{self.to_hex()}')"


# basic colors
red = Color(231, 76, 60)
green = Color(46, 204, 113)
blue = Color(52, 152, 219)
yellow = Color(241, 196, 15)
purple = Color(155, 89, 182)
cyan = Color(26, 188, 156)
pink = Color(255, 121, 198)
dark = Color(30, 30, 30)


def mix(color1: Color, color2: Color, weight: float = 0.5) -> Color:
    weight = max(0.0, min(1.0, weight))
    r = int(color1.r * (1 - weight) + color2.r * weight)
    g = int(color1.g * (1 - weight) + color2.g * weight)
    b = int(color1.b * (1 - weight) + color2.b * weight)
    return Color(r, g, b)


def gradient(text: str, color_start: Color, color_end: Color) -> str:
    length = len(text)
    if length <= 1:
        return color_start.paint(text)

    result = []
    for i, char in enumerate(text):
        r = int(color_start.r + (color_end.r - color_start.r) * (i / (length - 1)))
        g = int(color_start.g + (color_end.g - color_start.g) * (i / (length - 1)))
        b = int(color_start.b + (color_end.b - color_start.b) * (i / (length - 1)))
        
        current_color = Color(r, g, b)
        result.append(current_color.fg_ansi() + char)

    return "".join(result) + AnsiStyles.RESET


def show_palette():
    # shows all colors
    print("\n" + AnsiStyles.BOLD + "=== ВИЗУАЛЬНАЯ ПАЛИТРА HICOLORS ===" + AnsiStyles.RESET)
    for name, item in globals().items():
        if isinstance(item, Color):
            block = item.paint("████████")
            print(f" {block} -> {name} ({item.to_hex()})")
    print("=" * 35 + "\n")