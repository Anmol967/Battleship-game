import random
# string library below , for generating letters , which will be used as column names for the battleship boards -
import string
# itertools library for flattening a nested list -
import itertools

"""
Defining some helper functions below - 
"""

# Function for printing all the boards -
def print_board(row_names, col_names, board):
    # Printing the column names -
    print("    ", end="")
    for i in col_names:
        print(i, end=" ")
    print("")
    # Printing the board along with row names -
    for i in range(len(board)):
        if len(str(row_names[i])) > 1:
            print(row_names[i], end="  ")
        else:
            print(row_names[i], end="   ")
        for j in range(len(board)):
            print(board[i][j], end=" ")
        print("\n", end="")
    print("\n")


# Function to calculate the number of consecutive unexplored cells in any direction from a particular cell -
def unexplored_cells(cell, board, dir1):
    if dir1 == "left" or dir1 == "right":
        dir2 = dir1
        p = board.board[int(cell[1:]) - 1]
        idx = board.col_names.index(cell[0])

    if dir1 == "up" or dir1 == "down":
        # extracting that column as a list -
        p = [row[board.col_names.index(cell[0])] for row in board.board]
        idx = int(cell[1:]) - 1
        if dir1 == "up":
            dir2 = "left"
        else:
            dir2 = "right"

    if dir2 == "left":
        ctr = 0
        for i in range(1, idx + 1):
            if p[idx - i] == '.':
                ctr += 1
            else:
                break

    if dir2 == "right":
        ctr = 0
        for i in range(idx + 1, board.board_size):
            if p[i] == '.':
                ctr += 1
            else:
                break

    if dir1 == "left":
        cells_list = []
        row_idx = cell[1:]
        col_idx = cell[0]
        for i in range(1, ctr + 1):
            cells_list.append(board.col_names[board.col_names.index(col_idx) - i] + row_idx)
        return cells_list

    if dir1 == "right":
        cells_list = []
        row_idx = cell[1:]
        col_idx = cell[0]
        for i in range(1, ctr + 1):
            cells_list.append(board.col_names[board.col_names.index(col_idx) + i] + row_idx)
        return cells_list

    if dir1 == "up":
        cells_list = []
        row_idx = cell[1:]
        col_idx = cell[0]
        for i in range(1, ctr + 1):
            cells_list.append(col_idx + str(int(row_idx) - i))
        return cells_list

    if dir1 == "down":
        cells_list = []
        row_idx = cell[1:]
        col_idx = cell[0]
        for i in range(1, ctr + 1):
            cells_list.append(col_idx + str(int(row_idx) + i))
        return cells_list


# Returns the first element of the first non-empty list in a nested list and also the index of the first non-empty list -
def ai_move(k):
    ctr = -1
    for i in k:
        ctr += 1
        if i != []:
            return i[0], ctr


# Returns the nested list with the first element of the first non-empty list popped -
def ai_cells_update(k):
    for i in k:
        if i != []:
            i.pop(0)
            break
    return k


def placement(fit_up, fit_down, fit_left, fit_right, up, down, left, right, direction):
    if direction == "vert":
        if fit_up > fit_down:
            unexp_cells = [up,down]
            if fit_left>fit_right:
                unexp_cells.append(left)
                unexp_cells.append(right)
            else:
                unexp_cells.append(right)
                unexp_cells.append(left)
        else:
            unexp_cells = [down,up]
            if fit_left>fit_right:
                unexp_cells.append(left)
                unexp_cells.append(right)
            else:
                unexp_cells.append(right)
                unexp_cells.append(left)
    else:
        if fit_left > fit_right:
            unexp_cells = [left,right]
            if fit_up>fit_down:
                unexp_cells.append(up)
                unexp_cells.append(down)
            else:
                unexp_cells.append(down)
                unexp_cells.append(up)
        else:
            unexp_cells = [right,left]
            if fit_up>fit_down:
                unexp_cells.append(up)
                unexp_cells.append(down)
            else:
                unexp_cells.append(down)
                unexp_cells.append(up)
    return unexp_cells


# Class for making battleship boards -
class BattleshipBoard():
    def __init__(self, guessing_board, ai, board_size):
        self.guessing_board = guessing_board
        self.ai = ai
        self.board_size = board_size
        self.row_names = [i for i in range(1, self.board_size + 1)]
        self.col_names = ' '.join(string.ascii_uppercase[:self.board_size]).split(' ')
        self.board = []
        for i in range(board_size):
            row = []
            for j in range(board_size):
                row.append(".")
            self.board.append(row)
        if not self.guessing_board:
            self.ship_sizes = [5, 4, 3, 3, 2]
            self.ship_locations = []
            if self.ai:
                temp_locations = []
                for ship_size in self.ship_sizes:
                    # 1 for placing ship column-wise , 2 for row-wise -
                    if random.randint(1, 2) == 1:
                        while True:
                            # Choose one random column -
                            ship_col = random.choice(self.col_names)
                            # Choosing a consecutive sequence of those many cells equal to the ship_size -
                            start_idx_ship_row = random.choice(range(1, (len(self.row_names) - ship_size + 1) + 1)) - 1
                            end_idx_ship_row = start_idx_ship_row + (ship_size - 1)
                            # Checking whether this ship's indices are already occupied , if they are , then keep looping until unoccupied indices are found -
                            flag = 0
                            for row in self.board[start_idx_ship_row : end_idx_ship_row + 1]:
                                if row[self.col_names.index(ship_col)].isdigit():
                                    flag += 1
                                    break
                            if flag:
                                continue
                            else:
                                # Storing ship's locations -
                                for i in range(start_idx_ship_row, end_idx_ship_row + 1):
                                    temp_locations.append(f"{ship_col}{i + 1}")
                                self.ship_locations.append(temp_locations)
                                temp_locations = []
                                # Changing all the cells corresponding to ship's location to "1" -
                                for row in self.board[start_idx_ship_row : end_idx_ship_row + 1]:
                                    row[self.col_names.index(ship_col)] = "1"
                                break

                    else:
                        while True:
                            # Choose one random row -
                            ship_row = random.choice([self.row_names.index(i) for i in self.row_names])
                            # Choosing a consecutive sequence of those many cells equal to the ship_size -
                            start_idx_ship_col = random.choice(range(1, (len(self.col_names) - ship_size + 1) + 1)) - 1
                            end_idx_ship_col = start_idx_ship_col + (ship_size - 1)
                            # Checking whether this ship's indices are already occupied , if they are , then keep looping until unoccupied indices are found -
                            if any([i.isdigit() for i in self.board[ship_row][start_idx_ship_col : end_idx_ship_col + 1]]):
                                continue
                            else:
                                # Storing ship's locations -
                                for i in range(start_idx_ship_col, end_idx_ship_col + 1):
                                    temp_locations.append(f"{self.col_names[i]}{ship_row + 1}")
                                self.ship_locations.append(temp_locations)
                                temp_locations = []
                                # Changing all the cells corresponding to ship's location to "1" -
                                for idx, element in enumerate(self.board[ship_row]):
                                    if (start_idx_ship_col <= idx <= end_idx_ship_col):
                                        self.board[ship_row][idx] = "1"
                                break
            # If it is user's board -
            else:
                # Printing an empty board -
                print("\nEmpty board - \n")
                print_board(self.row_names, self.col_names, self.board)
                print("Enter the cell locations(column letter followed by row number , separated by commas & no spaces anywhere) of the ship for each ship size below - \n")
                # Prompting user to enter ship locations for different ship sizes , one by one -
                for ship_size in self.ship_sizes:
                    print(f"Ship size : {ship_size}")
                    while True:
                        input_cells = input().split(",")
                        if set(itertools.chain.from_iterable(self.ship_locations)).intersection(set(input_cells)) == set():
                            self.ship_locations.append(input_cells)
                            for input_cell in input_cells:
                                self.board[int(input_cell[1:]) - 1][self.col_names.index(input_cell[0])] = "1"
                            break
                        else:
                            print("One or more cell locations you entered , already have a part of some ship . Please enter different locations !")
                # Printing the user's board with battleships -
                print("\n")
                print_board(self.row_names, self.col_names, self.board)

            # Sorting ship_locations in ascending order by ship_size -
            self.ship_locations = sorted(self.ship_locations, key = lambda x : len(x))

            # Building a dictionary which maps the ship name to ship location -
            self.ship_names = ["Destroyer","Submarine","Cruiser","Battleship","Carrier"]
            self.name_loc = {}
            for i in range(len(self.ship_names)):
                self.name_loc[self.ship_names[i]] = self.ship_locations[i]

            # Building a dictionary which maps ship_names to the number of parts of the ship destroyed , initializing it with the ships's sizes -
            self.name_hit_count = {}
            for name in self.ship_names:
                self.name_hit_count[name] = len(self.name_loc[name])

################################################ Class BattleShipBoard definition ends here ######################################################################

class Player():
    def __init__(self, ai):
        self.ai = ai
        self.already_guessed = []
        self.n_moves = 0
        self.n_ships_sunk = 0
        self.remaining = []
        if self.ai:
            # hit_var will be 0 when AI has to choose a cell randomly and 1 when AI has to make an informed decision -
            self.hit_var = 0
            self.history = [0]
            self.unexp_cells = []
            self.guess_list_index = 0
            self.state = ""
            self.dict1 = dict()
            self.dict2 = dict()
    def solve(self, gb, bb, possible_cells):

        if not self.ai:

            while True:
                human_guess = input("Enter a cell location - ")
                if (human_guess not in self.already_guessed) and (human_guess in possible_cells):
                    self.already_guessed.append(human_guess)
                    break
                else:
                    print("The cell you entered either does not exist on the board or has been already entered by you!")

            if bb.board[int(human_guess[1:]) - 1][bb.col_names.index(human_guess[0])] == "1":
                print("It's a hit !")
                gb.board[int(human_guess[1:]) - 1][gb.col_names.index(human_guess[0])] = "X"
                # Updating the hit count -
                loc_hit = sorted(bb.ship_locations, key = lambda x : human_guess in x, reverse = True)[0]
                destroyed_ship = list(bb.name_loc.keys())[list(bb.name_loc.values()).index(loc_hit)]
                bb.name_hit_count[destroyed_ship] -= 1
                # Checking if this hit caused any ship to sink completely -
                if bb.name_hit_count[destroyed_ship] == 0:
                    self.n_ships_sunk += 1
                    print(destroyed_ship + f"(size = {len(bb.name_loc[destroyed_ship])}) destroyed !!!")
                    self.remaining.remove(len(bb.name_loc[destroyed_ship]))

                print_board(gb.row_names, gb.col_names, gb.board)
                print(f"Ships remaining of sizes (for you): {self.remaining}")
                print(f"Number of moves played by you: {self.n_moves + 1}")

            else:
                print("You miss")
                gb.board[int(human_guess[1:]) - 1][gb.col_names.index(human_guess[0])] = "O"
                print_board(gb.row_names, gb.col_names, gb.board)
                print(f"Ships remaining of sizes (for you): {self.remaining}")
                print(f"Number of moves played by you: {self.n_moves + 1}")

            self.n_moves += 1

        else:
            # Implementing solve function for AI player -
            if self.hit_var == 0:
                # Choosing a cell randomly out of all the unoccupied cells -
                ai_guess = random.choice(list(set(possible_cells).difference(set(self.already_guessed))))
                self.already_guessed.append(ai_guess)

            else:
                # Implementation of the main logic -
                if ((self.history[-1] == 1 and self.history[-2] == 0 and self.state == "") or (self.history[-1] == 1 and self.history[-2] == 1 and self.state == "")):
                    # List of consecutive unexplored cells in each direction -
                    up = unexplored_cells(self.already_guessed[-1], gb, "up")
                    down = unexplored_cells(self.already_guessed[-1], gb, "down")
                    left = unexplored_cells(self.already_guessed[-1], gb, "left")
                    right = unexplored_cells(self.already_guessed[-1], gb, "right")

                    # Number of ships that can be fit in each direction -
                    fit_up = sum([len(up) >= (i - 1) for i in bb.ship_sizes])
                    fit_down = sum([len(down) >= (i - 1) for i in bb.ship_sizes])
                    fit_left = sum([len(left) >= (i - 1) for i in bb.ship_sizes])
                    fit_right = sum([len(right) >= (i - 1) for i in bb.ship_sizes])

                    # Horizontal vs vertical direction -
                    hori = sum([(len(left) + len(right)) >= (i - 1) for i in bb.ship_sizes])
                    vert = sum([(len(up) + len(down)) >= (i - 1) for i in bb.ship_sizes])
                    print("Number of ships that can be fit - ")

                    if hori > vert:
                        self.unexp_cells=placement(fit_up, fit_down, fit_left, fit_right, up, down, left, right, "hori")
                    elif vert > hori:
                        self.unexp_cells=placement(fit_up, fit_down, fit_left, fit_right, up, down, left, right, "vert")
                    else:
                        if random.randint(1, 2) == 1:
                            # Going with horizontal direction first -
                            self.unexp_cells=placement(fit_up, fit_down, fit_left, fit_right, up, down, left, right, "hori")
                        else:
                            # Going with vertical direction first -
                            self.unexp_cells=placement(fit_up, fit_down, fit_left, fit_right, up, down, left, right, "vert")

                    ai_guess = ai_move(self.unexp_cells)[0]
                    self.guess_list_index = ai_move(self.unexp_cells)[1]
                    self.state = "done once"
                    # Updating the unexp_cells so that the cell which has been guessed , is not guessed again -
                    self.unexp_cells = ai_cells_update(self.unexp_cells)

                elif self.history[-1] == 1:
                    ai_guess = ai_move(self.unexp_cells)[0]
                    self.guess_list_index = ai_move(self.unexp_cells)[1]
                    self.unexp_cells = ai_cells_update(self.unexp_cells)

                elif self.history[-1] == 0:
                    self.unexp_cells.pop(self.guess_list_index)
                    ai_guess = ai_move(self.unexp_cells)[0]
                    self.guess_list_index = ai_move(self.unexp_cells)[1]
                    self.unexp_cells = ai_cells_update(self.unexp_cells)

                self.already_guessed.append(ai_guess)

            if bb.board[int(ai_guess[1:]) - 1][bb.col_names.index(ai_guess[0])] == "1":
                self.history.append(1)
                print("It's a hit !")
                gb.board[int(ai_guess[1:]) - 1][gb.col_names.index(ai_guess[0])] = "X"
                if self.hit_var == 0:
                    self.hit_var = 1
                # Updating the hit count -
                loc_hit = sorted(bb.ship_locations, key=lambda x: ai_guess in x, reverse=True)[0]
                destroyed_ship = list(bb.name_loc.keys())[list(bb.name_loc.values()).index(loc_hit)]
                bb.name_hit_count[destroyed_ship] -= 1
                # Checking if this hit caused any ship to sink completely -
                if bb.name_hit_count[destroyed_ship] == 0:
                    self.unexp_cells = []
                    self.n_ships_sunk += 1
                    print(destroyed_ship + f"(size = {len(bb.name_loc[destroyed_ship])}) destroyed !!!")
                    self.remaining.remove(len(bb.name_loc[destroyed_ship]))
                # If ship is destroyed , then again the AI will have to choose a cell randomly so changing hit_var to 0 -
                if self.hit_var == 1 and bb.name_hit_count[destroyed_ship] == 0:
                    self.hit_var = 0
                    self.state = ""
                print_board(gb.row_names, gb.col_names, gb.board)
                print(f"Ships remaining of sizes (for AI): {self.remaining}")
                print(f"Number of moves played by AI: {self.n_moves + 1}")

            else:
                self.history.append(0)
                print("AI misses")
                gb.board[int(ai_guess[1:]) - 1][gb.col_names.index(ai_guess[0])] = "O"
                print_board(gb.row_names, gb.col_names, gb.board)
                print(f"Ships remaining of sizes (for AI): {self.remaining}")
                print(f"Number of moves played by AI: {self.n_moves + 1}")

            self.n_moves += 1


# This is the main driver function . All the objects get created here .
def main():
    print("Welcome !")
    human_bb = BattleshipBoard(False, False, 6)
    ai_bb = BattleshipBoard(False, True, 6)
    human_gb = BattleshipBoard(True, False, 6)
    ai_gb = BattleshipBoard(True, True, 6)
    player_human = Player(False)
    player_ai = Player(True)
    player_human.remaining = ai_bb.ship_sizes
    player_ai.remaining = human_bb.ship_sizes
    who_plays = ""
    possible_cells = [x + str(i) for x in ai_bb.col_names for i in ai_bb.row_names]
    # Game loop -
    while True:
        if who_plays == "":
            # Random number to decide who starts first , if 1 then Human and if 2 then AI -
            if random.randint(1, 2) == 1:
                who_plays = "human"
                print("You start - ")
            else:
                who_plays = "ai"
                print("AI player starts - ")

        if who_plays == "human":
            if player_ai.n_moves > 0:
                print("Your turn - ")
            print("AI's board - ")
            print_board(ai_gb.row_names, ai_gb.col_names, ai_gb.board)
            player_human.solve(ai_gb, ai_bb, possible_cells)

            if player_human.n_ships_sunk == len(ai_bb.ship_sizes):
                print("All ships sunk !!")
                if player_ai.n_moves < player_human.n_moves:
                    # Then AI player will get one last turn and we'll have to check for a tie -
                    print("AI player's last turn - ")
                    print("Your board - ")
                    print_board(human_gb.row_names, human_gb.col_names, human_gb.board)
                    player_ai.solve(human_gb, human_bb, possible_cells)
                    if player_ai.n_ships_sunk == len(human_bb.ship_sizes):
                        print("All ships sunk !")
                        print("IT'S A TIE.")
                        break
                    else:
                        print("CONGRATULATIONS, YOU WIN !!!")
                        break
                else:
                    print("CONGRATULATIONS, YOU WIN !!!")
                    break
            who_plays = "ai"

        if who_plays == "ai":
            if player_human.n_moves > 0:
                print("AI player's turn - ")
            print("Your board - ")
            print_board(human_gb.row_names, human_gb.col_names, human_gb.board)
            player_ai.solve(human_gb, human_bb, possible_cells)

            if player_ai.n_ships_sunk == len(human_bb.ship_sizes):
                print("All ships sunk !")
                if player_human.n_moves < player_ai.n_moves:
                    # Then human player will get one last turn and we'll have to check for a tie -
                    print("Your last turn - ")
                    print("AI's board - ")
                    print_board(ai_gb.row_names, ai_gb.col_names, ai_gb.board)
                    player_human.solve(ai_gb, ai_bb, possible_cells)
                    if player_human.n_ships_sunk == len(ai_bb.ship_sizes):
                        print("All ships sunk !!")
                        print("IT'S A TIE.")
                        break
                    else:
                        print("AI PLAYER WINS!")
                        break
                else:
                    print("AI PLAYER WINS!")
                    break

            who_plays = "human"

# Running the code -
if __name__ == "__main__":
    main()





