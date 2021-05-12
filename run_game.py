import os
import sys
import arcade
import chess
import chess.engine
import board_config
from math import floor, ceil


files = board_config.CENTER_X - (board_config.BOARD_SIDELENGTH / 2) 
ranks = board_config.CENTER_Y - (board_config.BOARD_SIDELENGTH / 2)
offset = board_config.BOARD_SIDELENGTH / 16

def main():
    if len(sys.argv) != 2 or sys.argv[1] not in "bw":
        print("Choose a color to play as: either 'b' or 'w'")
    else:
        window_title = "Chess"
        game = GameofChess(board_config.SCREEN_WIDTH, board_config.SCREEN_HEIGHT,
                            window_title, fullscreen=False)
        game.setup()
        arcade.run()


class GameofChess(arcade.Window):
    def __init__(self, width, height, title, fullscreen):
        super().__init__(width, height, title, fullscreen)
        arcade.set_background_color(arcade.color.WHITE)
    
    def setup(self):
        self.piece_sprites = arcade.SpriteList()
        self.user_color = sys.argv[1]
        self.pieces = self.create_pieces()
        self.current_piece = None
        self.start = None
        self.end = None
        self.turn = 0
        self.captured_spacing = [0, 0]
        self.points = [0, 0]
        self.score_text = ""
        self.score_x = 0
        self.score_y = 0
        self.check = [False, False]
        self.board = chess.Board()
        self.promotion_choice = [None, 0]
        for pos in self.pieces:
            current_sprite = self.pieces[pos].sprite
            coords = self.pos_to_coords(pos)
            current_sprite.center_x = coords[0]
            current_sprite.center_y = coords[1]
            self.piece_sprites.append(current_sprite)
        if self.user_color == "b":
            self.run_engine()
    
    def create_pieces(self):
        names = [("rook", 5), ("knight", 3), ("bishop", 3), ("queen", 9),
                ("king", 10), ("bishop", 3), ("knight", 3), ("rook", 5)]
        pieces = {}
        for color in "bw":
            if color == self.user_color:
                rank = "1"
                pawn_rank = "2"
            else:
                rank = "8"
                pawn_rank = "7"
            for i in range(len(names)):
                name = names[i][0]
                value = names[i][1]
                val = i
                if self.user_color == "b":
                    if name == "queen":
                        val += 1
                    if name == "king":
                        val -= 1
                position = chr(val + ord("a")) + rank
                sprite = arcade.Sprite(f"chess_pieces/{name}_{color}.png")
                pieces[position] = Piece(name, value, color, sprite)
            for j in range(8):
                name = "pawn"
                value = 1
                position = chr(j + ord("a")) + pawn_rank
                sprite = arcade.Sprite(f"chess_pieces/{name}_{color}.png")
                pieces[position] = Piece(name, value, color, sprite)
        
        return pieces
    
    def pos_to_coords(self, position):
        x_mult = ord(position[0]) - ord("a") + 1
        y_mult = int(position[1])
        x = files + offset * (2 * x_mult - 1)
        y = ranks + offset * (2 * y_mult - 1)
        return (x, y)

    def coords_to_pos(self, x, y):
        x_int = floor((ceil((x - files) / offset) + 1) / 2)
        y_int = floor((ceil((y - ranks) / offset) + 1) / 2)
        x_letter = chr(x_int + ord("a") - 1)
        return x_letter + str(y_int)
    
    def flipper(self, pos):
        return chr(ord("h") - ord(pos[0]) + ord("a")) + str(8 - int(pos[1]) + 1)
    
    def on_board(self, x, y):
        return x > files and x < files + board_config.BOARD_SIDELENGTH and y > ranks and y < ranks + board_config.BOARD_SIDELENGTH

    def on_draw(self):
        arcade.start_render()
        board_config.draw_board()
        self.piece_sprites.draw()
        arcade.draw_text(self.score_text, self.score_x, self.score_y, arcade.color.BLACK, 30)
    
    def run_engine(self):
        engine = chess.engine.SimpleEngine.popen_uci("stockfish.exe")
        result = engine.play(self.board, chess.engine.Limit(time=0.05))
        move = result.move.uci()
        self.start = move[0:2]
        self.end = move[2:4]
        if self.user_color == "b":
            self.start = self.flipper(self.start)
            self.end = self.flipper(self.end)
        if len(move) == 5:
            if move[4] == "q":
                self.promotion_choicep[0] = "queen"
            elif move[4] == "r":
                self.promtion_choice[0] = "rook"
            elif move[4] == "n":
                self.promotion_choice[0] = "knight"
            else:
                self.promotion_choice[0] = "bishop"
        self.current_piece = self.pieces[self.start]
        self.make_move(move)
        engine.quit()

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT and self.on_board(x, y):
            self.start = self.coords_to_pos(x, y)
            try:
                self.current_piece = self.pieces[self.start]
            except KeyError:
                self.current_piece = None
            else:
                self.current_piece.sprite.scale = 1.3
                self.piece_sprites.remove(self.current_piece.sprite)
                self.piece_sprites.insert(31, self.current_piece.sprite)
    
    def on_mouse_drag(self, x, y, dx, dy, _buttons, _modifiers):
        if self.on_board(x, y) and self.current_piece != None:
            self.current_piece.sprite.center_x = x
            self.current_piece.sprite.center_y = y

    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT and self.current_piece != None:
            self.end = self.coords_to_pos(x, y)
            if self.start == self.end:
                move = "0000"
            elif self.user_color == "b":
                move = self.flipper(self.start) + self.flipper(self.end)
            else:
                move = self.start + self.end
            if self.current_piece.name == "pawn" and (self.end[1] == "1" or self.end[1] == "8"):
                if self.promotion_choice[0] == None:
                    self.promotion_choice[0] = "queen"
                    self.promotion_choice[1] = 9
                    move += "q"
                elif self.promotion_choice[0] == "knight":
                    self.promotion_choice[1] = 3
                    move += "n"
                elif self.promotion_choice[0] == "rook":
                    self.promotion_choice[1] = 5
                    move += "r"
                else:
                    self.promotion_choice[1] = 3
                    move += "b"
            if self.on_board(x, y) and chess.Move.from_uci(move) in self.board.legal_moves:
                self.make_move(move)
                self.run_engine()
            else:
                orig_coords = self.pos_to_coords(self.start)
                self.current_piece.sprite.center_x = orig_coords[0]
                self.current_piece.sprite.center_y = orig_coords[1]
                self.current_piece.sprite.scale = 1
    
    def on_key_press(self, key, modifiers):
        if self.current_piece.name == "pawn" and (self.start[1] == "2" or self.start[1] == "7"):
            keys = {arcade.key.R:"rook", arcade.key.K:"knight", arcade.key.B:"bishop"}
            if key in keys:
                self.promotion_choice[0] = keys[key]

    def make_move(self, move):
        spaces_moved = ord(self.start[0]) - ord(self.end[0])
        if self.current_piece.name == "king" and abs(spaces_moved) == 2: #castling
            current_rank = self.start[1]
            if spaces_moved == 2:
                rook_start = "a" + current_rank
                rook_end = "d" + current_rank
                if self.user_color == "b":
                    rook_end = "c" + current_rank
            elif spaces_moved == -2:
                rook_start = "h" + current_rank
                rook_end = "f" + current_rank
                if self.user_color == "b":
                    rook_end = "e" + current_rank
            rook_to_move = self.pieces[rook_start]
            rook_to_move.sprite.center_x = self.pos_to_coords(rook_end)[0]
            rook_to_move.sprite.center_y = self.pos_to_coords(rook_end)[1]
            self.pieces[rook_end] = rook_to_move
            del self.pieces[rook_start]
        
        if len(move) == 5: #promotion
            self.piece_sprites.remove(self.current_piece.sprite)
            sprite = arcade.Sprite(f"chess_pieces/{self.promotion_choice[0]}_{self.current_piece.color}.png")
            self.current_piece.sprite = sprite
            self.piece_sprites.insert(31, sprite)
            self.current_piece.value = self.promotion_choice[1]
            self.promotion_choice[0] = None
        
        self.current_piece.sprite.scale = 1
        new_coords = self.pos_to_coords(self.end)
        self.current_piece.sprite.center_x = new_coords[0]
        self.current_piece.sprite.center_y = new_coords[1]
        if self.user_color == "b":
            to_parse = self.flipper(self.end)
        else:
            to_parse = self.end
        if self.end in self.pieces:
            self.remove_piece(self.end, False)
        elif chess.parse_square(to_parse) == self.board.ep_square:
            self.remove_piece(self.end, True)
        self.board.push(chess.Move.from_uci(move))
        self.pieces[self.end] = self.current_piece
        del self.pieces[self.start]     
        self.turn += 1
        
        if self.board.is_checkmate():
            self.setup()
        elif self.board.is_game_over():
            pass
        

    def remove_piece(self, pos, is_en_passant):
        if is_en_passant:
            if pos[1] == "6":
                to_remove = self.pieces[pos[0] + "5"]
            else:
                to_remove = self.pieces[pos[0] + "4"]
        else:
            to_remove = self.pieces[pos]
        to_remove.sprite.scale = 0.5
        w = to_remove.sprite.width
        h = to_remove.sprite.height
        i_capture = int(self.user_color == to_remove.color)
        self.points[i_capture] += to_remove.value
        diff = self.points[0] - self.points[1]
        i_score = int(diff < 0)
        self.captured_spacing[i_capture] += w / 2
        to_remove.sprite.center_x = files - self.captured_spacing[i_capture]
        to_remove.sprite.center_y = ranks
        self.score_x = files - self.captured_spacing[i_score] - w
        self.score_y = ranks - h / 3
        if i_capture:
            to_remove.sprite.center_y += board_config.BOARD_SIDELENGTH
        if i_score:
            self.score_y += board_config.BOARD_SIDELENGTH
        if self.score_x <= 0:
            self.captured_spacing[i_capture] = w / 2
            self.check[i_capture] = True
        if self.check[i_capture]:
            to_remove.sprite.center_x = files - self.captured_spacing[i_capture]
            if i_capture:
                to_remove.sprite.center_y -= h
            else:
                to_remove.sprite.center_y += h
        if self.check[i_score]:
            self.score_x = files - self.captured_spacing[i_score] - w
            if i_score:
                self.score_y -= h
            else:
                self.score_y += h
        if diff == 0:
            self.score_text = ""
        else:
            self.score_text = f"+{abs(diff)}"
        
        
        

class Piece:
    def __init__(self, name, value, color, sprite):
        self.name = name
        self.value = value
        self.color = color
        self.sprite = sprite
        
        
if __name__ == "__main__":
    main()
