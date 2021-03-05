"""Connect Four Terminal Edition w/_AI.

Adapted by Joel Burton <joel@joelburton.com>; designed for use on memory-limited
microcontrollers (takes ~12s for a move at 6 ply on a Raspberry Pi Pico.)

Uses a pretty standard minimax with a/b pruning and a rather crude heuristic.
"""

import random
import time
import gc
import framebuf
from common import oled, button, pot, mark, url

# Define "sprites" (bitmapped images to show, encoded in binary)
FB = framebuf.FrameBuffer

_SPRITES = [FB(s, 8, 8, framebuf.MONO_VLSB) for s in [
    bytearray('\x00\x00\x04\x00\x00'), # empty
    bytearray('\x11\x0a\x04\x0a\x11'), # X
    bytearray('\x0e\x11\x11\x11\x0e'), # O
]]

_HEADERS = [FB(s, 8, 8, framebuf.MONO_VLSB) for s in [
    bytearray('\x38\x0e\x09\x0e\x38'), # A
    bytearray('\x3F\x25\x25\x25\x1a'), # B
    bytearray('\x1e\x21\x21\x21\x12'), # C
    bytearray('\x3f\x21\x21\x21\x1e'), # D
    bytearray('\x3f\x25\x21\x21\x21'), # E
    bytearray('\x3f\x05\x05\x01\x01'), # F
    bytearray('\x1e\x21\x21\x29\x18'), # G
]]
           

_EMPTY = const(0)
_PLAYER = const(1)
_AI = const(2)

_WIDTH = const(7)
_HEIGHT = const(6)
_NUM_CELLS = const(_WIDTH * _HEIGHT)

# MicroPython doesn't have math.inf, so use this as inifinity
_INFINITY = const(10000)
_MINUS_INFINITY = const(-10000)

# The board in the game is going to bytearray that is 42 (7*6) long.
# It is numbered from bottom-to-top, left-to-right. Here are the cells
# in the center column:
_CENTER: tuple[int] = (38,31,24,17,10,3)

# The windows that are checked for wins or board evaluation. It's faster
# to precompute these and loop over these coordinates, rather than doing
# fancier looping in the program.
_WINDOWS: tuple[tuple[int]] = (
    # horizontal
    (0,1,2,3),
    (1,2,3,4),
    (2,3,4,5),
    (3,4,5,6),
    (7,8,9,10),
    (8,9,10,11),
    (9,10,11,12),
    (10,11,12,13),
    (14,15,16,17),
    (15,16,17,18),
    (16,17,18,19),
    (17,18,19,20),
    (21,22,23,24),
    (22,23,24,25),
    (23,24,25,26),
    (24,25,26,27),
    (28,29,30,31),
    (29,30,31,32),
    (30,31,32,33),
    (31,32,33,34),
    (35,36,37,38),
    (36,37,38,39),
    (37,38,39,40),
    (38,39,40,41),
    # vertical
    (0,7,14,21),
    (1,8,15,22),
    (2,9,16,23),
    (3,10,17,24),
    (4,11,18,25),
    (5,12,19,26),
    (6,13,20,27),
    (7,14,21,28),
    (8,15,22,29),
    (9,16,23,30),
    (10,17,24,31),
    (11,18,25,32),
    (12,19,26,33),
    (13,20,27,34),
    (14,21,28,35),
    (15,22,29,36),
    (16,23,30,37),
    (17,24,31,38),
    (18,25,32,39),
    (19,26,33,40),
    (20,27,34,41),
    # diag up
    (14,22,30,38),
    (7,15,23,31),
    (15,23,31,39),
    (0,8,16,24),
    (8,16,24,32),
    (16,24,32,40),
    (1,9,17,25),
    (9,17,25,33),
    (17,25,33,41),
    (2,10,18,26),
    (10,18,26,34),
    (3,11,19,27),
    # diag down
    (21,15,9,3),
    (28,22,16,10),
    (22,16,10,4),
    (35,29,23,17),
    (29,23,17,11),
    (23,17,11,5),
    (36,30,24,18),
    (30,24,18,12),
    (24,18,12,6),
    (37,31,25,19),
    (31,25,19,13),
    (38,32,26,20),
)


@micropython.native
def score_position(board: bytearray, piece: int) -> int:
    """Evaluate this board score from position of `piece`."""
    
    opp_piece: int = _PLAYER if piece == _AI else _PLAYER
    score: int = 0

    # score 3 points for every point in _CENTER
    for i in _CENTER:
        if board[i] == piece:
            score += 3

    # Evaluate each 4-piece "window" and score with heuristics below
    for w in _WINDOWS:
        count: int = 0
        empties: int = 0
        opp_count: int = 0
        
        # Count what's in this window
        for i in w:
            if board[i] == piece:
                count += 1
            elif board[i] == opp_piece:
                opp_count += 1
            else:
                empties += 1

        # Our heuristics:
        # - playing in the _CENTER is strong
        # - three out a window of four is strong
        # - two out of a window of four is good
        window_score: int = 0
        
        if count == 4:
            window_score += 10000
        elif count == 3 and empties == 1:
            window_score += 5
        elif count == 2 and empties == 2:
            window_score += 2

        # defensive angle: don't let _PLAYER get a window w/three pieces
        if opp_count == 3 and empties == 1:
            window_score -= 4

        score += window_score
        
    return score

@micropython.native
def minimax(board: bytearray,
            depth: int,   # depth of current plies (0 = deepest)
            alpha: int,    
            beta: int,     
            max_player: bool,  # is this maximzing player?
            at_top: bool=False,  # are we the top call to this?
    ):
    """Minimax search with alpha-beta pruning."""
    
    # base cases:
    # - Player will win w/this board (since AI loses, return massive negative)
    # - AI will win w/this board (return massive positive)
    # - reached the depth of recursion (score this leaf for AI)
    # - board is full (no score for this leaf)

    won_by: int  = 0
    for c1, c2, c3, c4 in _WINDOWS:
        if board[c1] and  (board[c1] == board[c2] == board[c3] == board[c4]):
            won_by = board[c1]
            break
        
    if won_by == _PLAYER:
        # subtract depth so we delay loss as much as possible 
        return -1000 - depth  
    if won_by == _AI:
        # add depth so faster wins are more attractive
        return 1000 + depth   
    if depth == 0:
        score = score_position(board, _AI)            
        return score

    # (these are arranged _CENTER-out to help make a/b pruning most efficient)
    valid_locations: list[int] = [
        col % 7 for col in (38,37,39,36,40,35,41) if board[col] == _EMPTY]

    if not valid_locations:
        return 0
        
    # minimax strategy: alternate if AI is looking for best move (maximizing)
    # or the most harmful response from the player (minimizing).
    value: int
    new_col: int
    row: int
    
    if max_player:
        value = _MINUS_INFINITY
        new_col = random.choice(valid_locations)
        for col in valid_locations:            
            for r in (0, 1, 2, 3, 4, 5):
                if board[7 * r + col] == 0:
                    row = r
                    break
            b_copy = bytearray(board)
            b_copy[row * 7 + col] = _AI
            new_score: int = minimax(b_copy, depth-1, alpha, beta, False)
            if new_score > value:
                value = new_score
                new_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break

    else:
        value = _INFINITY
        for col in valid_locations:
            for r in (0, 1, 2, 3, 4, 5):
                if board[7 * r + col] == 0:
                    row = r
                    break
            b_copy =  bytearray(board)
            b_copy[row * 7 + col] = _PLAYER
            new_score: int = minimax(b_copy, depth-1, alpha, beta, True)
            if new_score < value:
                value = new_score
            beta = min(beta, value)
            if alpha >= beta:
                break

    # For speed, return simple score except when exiting first recursive call,
    # and return the chosen column & the score in that case.
    if not at_top:
        return value
    else:
        return new_col % 7, value


class ConnectFour:
    def __init__(self, 
                 plies:int=5, 
                 start_player:int=0, 
                 serial_input=True, 
                 debug:bool=False):
        if start_player not in (0, 1, 2):
            raise Exception("Start player must be 0 [random], 1, or 2")
        if plies not in (3, 4, 5, 6):
            raise Exception("Plies must be 3 [easy]-6 [very hard]")
        self.board = bytearray(_NUM_CELLS)
        self.plies = plies
        self.last_play_rc = (None, None)
        self.game_over: bool = False
        self.turn = (
            start_player if start_player else random.choice([_PLAYER, _AI]))
        self.debug: bool = debug
        self.serial_input = serial_input
        self.play()

    def draw_header(self, selected=None):
        for c in range(_WIDTH):
            oled.blit(_HEADERS[c], c * 9, 0)
        if selected:
            oled.hline(selected * 9, 10, 5, 1) 
        oled.show()
        
    def display_board(self):
        """Show board on screen."""
        
        oled.fill(0)
        for r in range(_HEIGHT):
            for c in range(_WIDTH):
                sprite = _SPRITES[self.board[r * _WIDTH + c]]
                oled.blit(sprite, c * 9, (_HEIGHT - r - 1) * 8 + 16)
        
        r, c = self.last_play_rc
        if r != None:
            oled.hline(c * 9, (_HEIGHT - r - 1) * 8 + 16 + 6, 5, 1)  
        self.draw_header()
        oled.show()

    def print_board(self):
        """Print board to serial port."""
        
        # How to show empty/p1/p2
        VALS = ".XO"

        print("\n    a b c d e f g")
        print("  /--+-+-+-+-+-+--\\")
        for r in range(_HEIGHT - 1, -1, -1):
            s = "%s |" % r
            for c in range(_WIDTH):
                # Print mark next to most recent move
                mark = ">" if self.last_play_rc == (r, c) else " "
                s += mark + VALS[self.board[r * 7 + c]]
            print(s + " |")
        print("  \\--+-+-+-+-+-+--/")
        print("    a b c d e f g\n")

    def is_filled(self):
        return all(self.board[c] for c in (38,37,39,36,40,35,41))
    
    def is_game_won(self) -> int:
        """If game is won, return winner"""

        b = self.board
        for c1, c2, c3, c4 in _WINDOWS:
            if b[c1] and  (b[c1] == b[c2] == b[c3] == b[c4]):
                print("win", c1, c2, c3, c4)
                return b[c1]

    def get_row_for_col(self, col: int) -> int:
        """Get row of lowest empty cell in column"""
        for r in (0, 1, 2, 3, 4, 5):
            if self.board[7 * r + col] == 0:
                return r
        return 0

    def get_human_move(self, valid: list[int]) -> int:
        if self.serial_input:
            while True:
                move = input("Column [a-g] >").lower()
                if move and move in "abcdefg":
                    return ord(move) - ord("a")
                print("Invalid move")
        
        # use button & pot
        print("""
To move: use blue knob to choose a column, and button to drop your piece.
""")
        selected = pot.read_u16() // (65535 // _WIDTH)

        while button.value() == 1:
            oled.hline(selected * 9, 10, 5, 1)
            oled.show()        
            col = pot.read_u16() // (65535 // _WIDTH)
            if col != selected:
                oled.hline(selected * 9, 10, 5, 0)
                selected = col
        return selected


    def human_turn(self):
        valid:list[int] = [
            col % 7 for col in (38,37,39,36,40,35,41) if self.board[col] == 0]
        return self.get_human_move(valid)
        
    def ai_turn(self):        
        print("\nThinking; please wait...\n")

        start_at = time.ticks_ms()
        
        # If this is the first move, pick the center (score: 3)
        if self.last_play_rc == (None, None):
            col, minimax_score = 3, 3
        else:
            # Do GC collection now; this can be an optimization hack in MicroPy
            gc.collect()
            gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())
            
            col, minimax_score = minimax(
                board=self.board,
                depth=self.plies,
                alpha=_MINUS_INFINITY,
                beta=_INFINITY,
                max_player=True,
                at_top=True)

        if self.debug:
            print(
                "ai: minimax score=", minimax_score, 
                "time=", time.ticks_ms() - start_at)

        return col
    
    def play(self):
        """Play game until someone wins."""
        
        while True:
            self.print_board()
            self.display_board()
            winner = self.is_game_won()
            if winner or self.is_filled():
                break
        
            if self.turn == _PLAYER:
                col = self.human_turn()
            else:
                col = self.ai_turn()

            row = self.get_row_for_col(col)
            self.board[7 * row + col] = self.turn
            self.last_play_rc = row, col

            if self.debug:
                print("position scores:",
                      "player=", score_position(self.board, _PLAYER),
                      "ai=", score_position(self.board, _AI))
                
            self.turn = _AI if self.turn == _PLAYER else _PLAYER
        
        if winner == 0:
            msg = "Tie!"
        elif winner == 1:
            msg = "You win!"
        else:
            msg = "I win!"
        
        oled.text(msg, 64, 30)
        oled.show()
        print("\n" + msg + "\n")
        
        if winner == 0 or winner == 1:
            if self.plies == 3:
                print("""
(Of course, you did set me to easy mode, which I feel compelled to mention.)
""")
            print("""

There are some interesting things to learn about ConnectFour:

    {url}

To move ahead:

    >>> import sensors
    >>> sensors.start()

""".format(url=url("connectfour")))

        else:
            print("""
Wow. You were beat by a $4 computer--using only one of my processors (!!).
To get the code to move ahead, you'll need to at least tie me.

To play again, make a new instance of the ConnectFour class. You can choose
different options than the defaults:

 connectfour.ConnectFour(plies, start_player, serial_input, debug)
  - plies [5]: moves to look ahead (3-6, where 3 is easy and 6 is slow and hard
  - start_player [0]: 0 for random, 1 for you, 2 for me
  - serial_input [False]: Enter moves w/keyboard in terminal instead of knob
  - debug [False]: Show information about current AI evaluation scores

For example:

    >>> g = ConnectFour(plies=4, start_player=1)
    >>> g.play()

""")
            

def start():
    mark("connectfour")
    g = ConnectFour(plies=5, debug=True, serial_input=False)



