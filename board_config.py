import arcade

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 800
BOARD_SIDELENGTH = SCREEN_HEIGHT * (11 / 12)
CENTER_X = SCREEN_WIDTH / 2
CENTER_Y = SCREEN_HEIGHT / 2

def draw_board():
    draw_outline(CENTER_X, CENTER_Y, BOARD_SIDELENGTH)
    draw_squares(CENTER_X - (BOARD_SIDELENGTH / 2), CENTER_Y + (BOARD_SIDELENGTH / 2),
                 BOARD_SIDELENGTH / 8)

    
def draw_outline(cx, cy, offset):
    offset /= 2
    color = arcade.color.BLACK
    border_width = 20
    arcade.draw_lrtb_rectangle_outline(cx - offset, cx + offset, cy + offset,
                                       cy - offset, color, border_width)
                                      
def draw_squares(x, y, sidelength):
    orig_x = x
    color = arcade.color.LIGHT_BROWN
    for square in range(1, 65):
        arcade.draw_lrtb_rectangle_filled(x, x + sidelength, 
                                          y, y - sidelength, color)
        if square % 8 == 0:
            x = orig_x
            y -= sidelength
        else:
            x += sidelength
            if color == arcade.color.LIGHT_BROWN:
                color = arcade.color.DARK_BROWN
            else:
                color = arcade.color.LIGHT_BROWN




