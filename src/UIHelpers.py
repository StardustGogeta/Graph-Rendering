from pygame.math import Vector2 as V2
import pygame.gfxdraw
import pygame.draw
from functools import lru_cache
from math import floor, ceil


def draw_aaline(surf, start, end, color, width):
    if width == 1:
        pygame.draw.line(surf, color, start, end, width)
        return
    
    if start == end:
        return
    
    offset_a = V2(end) - V2(start)
    offset_b = V2(offset_a)
    offset_a.scale_to_length(floor(width / 2))
    offset_b.scale_to_length(ceil(width / 2))
    offset_a = offset_a.rotate(90)
    offset_b = offset_b.rotate(90)
    points = [
        start + offset_a,
        start - offset_b,
        end - offset_b,
        end + offset_a
    ]
    pygame.gfxdraw.aapolygon(surf, points, color)
    pygame.gfxdraw.filled_polygon(surf, points, color)

def draw_aa_arrow(surf, start, end, color, width, offset):
    ARROW_HEIGHT = 20
    ARROW_WIDTH = 20

    if width == 1:
        pygame.draw.line(surf, color, start, end, width)
        return
    
    if start == end:
        return
    
    offset_a = V2(end) - V2(start)
    offset_b = V2(offset_a)
    offset_a.scale_to_length(floor(width / 2))
    offset_b.scale_to_length(ceil(width / 2))
    offset_a = offset_a.rotate(90)
    offset_b = offset_b.rotate(90)
    points = [
        start + offset_a,
        start - offset_b,
        end - offset_b,
        end + offset_a
    ]
    pygame.gfxdraw.aapolygon(surf, points, color)
    pygame.gfxdraw.filled_polygon(surf, points, color)

    # Draw arrow head
    vec = V2(end) - V2(start)
    vec.scale_to_length(offset)

    # Mark arrow to point at edge of body
    arrow_tip = V2(end) - vec

    vec.scale_to_length(ARROW_HEIGHT)
    arrow_base = arrow_tip - vec

    # Create arrow base
    half_base = vec.rotate(90)
    half_base.scale_to_length(ARROW_WIDTH // 2)
    arrow_base_left = arrow_base - half_base
    arrow_base_right = arrow_base + half_base

    # Make arrow pointed
    vec.scale_to_length(ARROW_HEIGHT // 2)
    arrow_base += vec

    arrow_points = [
        arrow_tip,
        arrow_base_left,
        arrow_base,
        arrow_base_right
    ]
    pygame.gfxdraw.filled_polygon(surf, arrow_points, color)


# exterior is bounded by the given rect
def draw_aarectangle(surf, rect, color, width):
    width += 1 - width % 2
    off_x = V2(width // 2, 0)
    off_y = V2(0, width // 2)
    lines = [
        (rect.topleft + off_y, rect.topright + off_y),
        (rect.topright - off_x - (1, 0), rect.bottomright - off_x - (1, 0)),
        (rect.bottomright - off_y - (0, 1), rect.bottomleft - off_y  - (0, 1)),
        (rect.bottomleft + off_x, rect.topleft + off_x)
    ]
    for line in lines:
        draw_aaline(surf, *line, color, width)


def draw_aacircle(surf, center, radius, color):
    pygame.gfxdraw.filled_circle(surf, *center, radius, color)
    pygame.gfxdraw.aacircle(surf, *center, radius, color)


pygame.font.init()
# Binary search to find a font size s.t. the given text fills width_px pixels horizontally
@lru_cache(maxsize=1000)
def get_sized_font(font_family, text, width_px, bold=False):
    size_lower_bound = 8
    size_upper_bound = 100

    font = None
    size = width_px  # initial guess
    while size_upper_bound - size_lower_bound > 1:
        font = pygame.font.SysFont(font_family, size, bold=bold)
        text_size_px = max(font.size(text))
        error = text_size_px - width_px
        # print(size, error, size_lower_bound, size_upper_bound)
        if error >= 0:
            size_upper_bound = size
        else:
            size_lower_bound = size
        size = (size_lower_bound + size_upper_bound) // 2

    return font


def bounding_box(rect_list):
    return rect_list[0].unionall(rect_list[1:])


def ccw(A, B, C):
    return (C.y - A.y) * (B.x - A.x) > (B.y - A.y) * (C.x - A.x)

# Return true if line segments AB and CD intersect
def line_segment_intersect(line_a, line_b):
    A, B, C, D = *line_a, *line_b
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)
