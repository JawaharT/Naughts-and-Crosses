from tkinter import Tk, Canvas, messagebox
from collections import defaultdict
import random
import sys


def check_game_end(title_text):
    '''Game ends here with a small info box disaplying the outcome of game.

    Parameters
    __________
    title_text: str, not optional
        The text to display once game is complete.

    Return
    ______
    Displays winner and closes game.'''

    #Show final game outcome and quit game
    messagebox.showinfo(title=title_text, message=title_text)
    master.destroy()
    sys.exit()


def check_winner(player):
    '''Check if game is won and finished.

    Parameters
    __________
    Player: str, not optional
    To check whether game is won by user or computer.

    Return
    ______
    Winner if game is won.'''
    
    #Check player has won
    
    #Check for horizontal wins
    if (("topleft" in game_moves_dict[player]) and ("topmiddle" in game_moves_dict[player]) and ("topright" in game_moves_dict[player])
        or (("middleleft" in game_moves_dict[player]) and ("middlemiddle" in game_moves_dict[player]) and ("middleright" in game_moves_dict[player]))
        or (("bottomleft" in game_moves_dict[player]) and ("bottommiddle" in game_moves_dict[player]) and ("bottomright" in game_moves_dict[player]))):
            check_game_end("Player {} Wins!".format(player))

    #Check for vertical wins
    if (("topleft" in game_moves_dict[player]) and ("middleleft" in game_moves_dict[player]) and ("bottomleft" in game_moves_dict[player])
        or (("topmiddle" in game_moves_dict[player]) and ("middlemiddle" in game_moves_dict[player]) and ("bottommiddle" in game_moves_dict[player]))
        or (("topright" in game_moves_dict[player]) and ("middleright" in game_moves_dict[player]) and ("bottomright" in game_moves_dict[player]))):
            check_game_end("Player {} Wins!".format(player))

    #Check for diagonal wins
    if (("topleft" in game_moves_dict[player]) and ("middlemiddle" in game_moves_dict[player]) and ("bottomright" in game_moves_dict[player])
        or (("topright" in game_moves_dict[player]) and ("middlemiddle" in game_moves_dict[player]) and ("bottomleft" in game_moves_dict[player]))):
        check_game_end("Player {} Wins!".format(player))


def draw(limits,turn_text):
    '''Updates canvas player and computer moves.

    Parameters
    __________
    limits: str, not optional
        Using the limits of the square clicked to place X or 0 on the correct place.

    turn_text: str, not optional
        X or 0 for placement.

    Return
    ______
    Placement of X or 0 on the square clicked.'''
    
    #Place letter X or 0 on clicked square and computer's selected square
    canvas.create_text((limits[0][0]+limits[0][1])/2, (limits[1][0]+limits[1][1])/2, text=turn_text)
    canvas.update()


def motion(event):
    '''Checks where the user has clicked and places an X on that square.

    Parameters
    __________
    event: mouse event
        mouse click on GUI board.

    Return
    ______
    Main game play logic.'''
    
    x, y = event.x, event.y
    #Define the bounds of each box based on the lines drawn
    #x1 = x coordinate of top left corner of square, x2 = x coordinate of bottom right of square
    #y1 = y coordinate of top left corner of square, y2 = y coordinate of bottom right of square
    #[(x1,x2),(y1,y2)]

    #Check which square has been clicked
    for square,square_limits in coord_dict.items():
        if(x > square_limits[0][0] and x < square_limits[0][1]) and (y > square_limits[1][0] and y < square_limits[1][1]):
            if square in squares_left:

                #User X placed
                draw(square_limits,"X")
                squares_left.remove(square), game_moves_dict["X"].append(square)

                #Since all squares not selected, check if game is won
                check_winner("X")
                
                #Computer 0 placed
                if squares_left:
                    comp_choice = random.choice(squares_left)
                    draw(coord_dict[comp_choice], "0")
                    squares_left.remove(comp_choice), game_moves_dict["0"].append(comp_choice)

                    #Since all squares not selected, check if game is won
                    check_winner("0")
                break
            else:
                #Show messagebox if clicked on a square that has already been selected
                messagebox.showwarning(title="Warning", message="This square has already been selected")

    #Check if all squares have been used, if so end game
    if not squares_left:
        check_game_end("Draw! Game Over!")


def main():
    '''Creates and displays the main Naughts and Crosses board.

    Parameters
    __________
    No parameters required but global variables are defined as the game begins.

    Return
    ______
    The main GUI board is made.'''

    global master,canvas,coord_dict,squares_left,game_moves_dict

    #Defining the board GUI
    master = Tk()
    master.title("Simple Naughts and Crosses")
    master.geometry("300x300")
    master.resizable(False, False)
    
    canvas = Canvas(master, width=300, height=300)
    
    #All vertical lines
    canvas.create_line(100,0,100,300),canvas.create_line(200,0,200,300)

    #All horizontal lines
    canvas.create_line(0,100,300,100),canvas.create_line(0,200,300,200)
    
    canvas.pack(fill="both", expand=True)

    #Defining squares on the board
    coord_dict = dict()
    coord_dict["topleft"], coord_dict["topmiddle"], coord_dict["topright"] = [(0,100), (0,100)], [(100,200), (0,100)], [(200,300), (0,100)]
    coord_dict["middleleft"], coord_dict["middlemiddle"], coord_dict["middleright"] = [(0,100), (100,200)], [(100,200), (100,200)], [(200,300), (100,200)]
    coord_dict["bottomleft"], coord_dict["bottommiddle"], coord_dict["bottomright"] = [(0,100), (200,300)], [(100,200), (200,300)], [(200,300), (200,300)]

    squares_left = ["topleft", "topmiddle", "topright", "middleleft", "middlemiddle", "middleright", "bottomleft", "bottommiddle", "bottomright"]

    game_moves_dict = defaultdict(list)

    #Check for mouse clicks
    master.bind("<Button>", motion)
    master.mainloop()


#Starts Game.
if __name__ == '__main__':
    main()
