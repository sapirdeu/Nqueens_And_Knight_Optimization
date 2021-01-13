from __future__ import print_function
import os, sys
from copy import copy

sys.path.append('../')
sys.path.append('../pieces')
from time import time
from Board import Board
from random import randint


class HillClimbing:
    """
    Ctor.
    request : dictionary- list of object to be created.
    option : int- mark which algorithm type should be used.
    maxIter : int- number of max iterations.
    """

    def __init__(self, request, option, maxIter):
        self.__GOAL = 0
        self.__REQUEST = request
        self.__MAX_ITER = maxIter

        # If option is 1 then use first choice hill climbing, otherwise stochastic.
        if (option == 1):
            return self.first_choice()
        return self.stochastic()

    # Getters.
    def get_request(self):
        return self.__REQUEST

    def get_goal(self):
        return self.__GOAL

    def get_max_iter(self):
        return self.__MAX_ITER

    # First Choice Hill Climbing.
    def first_choice(self):
        """
            Algorithm:
            1. Pick one of the chess piece to be moved.
            2. Get random location that is possible to move
                2.1 Calculate its heuristic.
            3. If it is better than current heuristic
                3.1 Accept it.
            4. Otherwise,
                4.1 Repeat step 2.
            5. If goals achieved
                5.1 Exit.
            6. If there is no possible better move
                6.1 Repeat step 1.
            7. If all pieces do not have any better move, then it is stuck to local maximum.
            8. Restart initial state, if necessary.
        """

        # Start iteration.
        iterationNum = 1
        start = round(time(), 3)
        current_heuristic = None
        best_heuristic = None
        best_board = None

        # Iterate until maxIter is reached.
        while (iterationNum <= self.get_max_iter()):
            print("Iteration\t= " + str(iterationNum))

            # Create board object.
            board = Board(self.get_request())

            # Calculate current heuristic.
            current_heuristic = board.calculate_heuristic()

            # Define local maxima.
            local_maximum = False

            # Iterate until goal heuristic and local maximum is reached.
            while ((current_heuristic['total'] < self.get_goal()) and (not local_maximum)):
                # Get piece queue.
                piece_queue = board.random_pick()
                # Better state is defined as the heuristic is better than current heuristic.
                better_state = False
                # Iterate until all pieces are moved or there is a better state.
                while ((len(piece_queue) > 0) and (not better_state)):
                    # Get one piece to move.
                    current_piece = piece_queue.pop()

                    # Original position.
                    original_position = {
                        'x': current_piece.get_x(),
                        'y': current_piece.get_y(),
                    }

                    # Get list of all possible moves.
                    possible_moves = board.random_move(True)

                    # Loop until no other possible move for current piece.
                    while (len(possible_moves) > 0):
                        # Get a position to move.
                        current_move = possible_moves.pop()
                        # Replace current position of piece with current move.
                        current_piece.set_x(current_move['x'])
                        current_piece.set_y(current_move['y'])
                        # Calculate heuristic after change to new position.
                        heuristic = board.calculate_heuristic()
                        # Accept proposed move, if heuristic is better than current heuristic.
                        if (heuristic['total'] > current_heuristic['total']):
                            current_heuristic = heuristic
                            better_state = True
                            break
                        else:
                            # Restore the position of piece, not accept the changes.
                            current_piece.set_x(original_position['x'])
                            current_piece.set_y(original_position['y'])
                # Local maximum has reached because there is no possible piece moves,
                # that gives a better heuristic.
                if (not better_state):
                    local_maximum = True

            # Check if first iteration
            if (iterationNum == 1):
                best_heuristic = current_heuristic
                best_board = copy(board)

            # Check if current heuristic is better than current best.
            elif (best_heuristic['total'] < current_heuristic['total']):
                best_heuristic = current_heuristic
                best_board = copy(board)

            # Exits code when goal has achieved, or local maximum achieved with max iterations.
            if (current_heuristic['total'] == self.get_goal()):
                break

            # Restart iterations.
            iterationNum += 1

        # Exits code when goal has achieved, or local maximum achieved with max iterations.
        if (current_heuristic['total'] == self.get_goal()):
            finish = round(time(), 3)

            print("Optimal solution found after", str(iterationNum), "iterations")
            print("Elapsed time = " + str(finish - start) + " seconds\n")
        else:
            # maxIter reached.
            finish = round(time(), 3)

            print("First Choice Hill Climbing approximates global optimum (with ", iterationNum - 1, " iterations)")
            print("Elapsed time = " + str(finish - start) + " seconds\n")

        # Draw best Board
        best_board.draw()
        print("Conflicts amount: ", str(best_heuristic['a']))

        return

    # Stochastic Hill Climbing
    def stochastic(self):
        """
            Algorithm:
            1. Pick one of the chess piece to be moved.
            2. Calculate heuristic in each of its possible moves.
            3. Get random location that gives better heuristic value.
            4. If goals achieved
                4.1 Exit.
            5. If there is no possible better move
                5.1 Repeat step 1.
            6. If all pieces do not have any better move, then it is stuck to local maxima.
            7. Restart initial state, if necessary.
        """

        # Start iteration.
        iterationNum = 1
        start = round(time(), 3)
        current_heuristic = None
        best_heuristic = None
        best_board = None

        # Iterate until maxIter is reached.
        while (iterationNum <= self.get_max_iter()):
            print("Iteration\t= " + str(iterationNum))
            # Create board object.
            board = Board(self.get_request())

            # Calculate current heuristic.
            current_heuristic = board.calculate_heuristic()

            # Define local maximum.
            local_maximum = False
            # Iterate until goal heuristic and local maximum is reached.

            while ((current_heuristic['total'] < self.get_goal()) and (not local_maximum)):
                # Get piece queue.
                piece_queue = board.random_pick()
                # Better state is defined as the heuristic is better than current heuristic.
                better_states = []
                # Iterate until all pieces moved or there is a better state.
                while (len(piece_queue) > 0) and (len(better_states) == 0):
                    # Get one piece to move.
                    current_piece = piece_queue.pop()
                    # Original position
                    original_position = {
                        'x': current_piece.get_x(),
                        'y': current_piece.get_y(),
                    }

                    # Get list of all possible moves.
                    possible_moves = board.random_move(True)
                    # Loop until no other possible move for current piece.
                    while len(possible_moves) > 0:
                        # Get a position to move.
                        current_move = possible_moves.pop()
                        # Replace current position of piece with current move.
                        current_piece.set_x(current_move['x'])
                        current_piece.set_y(current_move['y'])
                        # Calculate heuristic after change to new position.
                        heuristic = board.calculate_heuristic()
                        # Accept proposed move, if heuristic is better than current heuristic.
                        if (heuristic['total'] > current_heuristic['total']):
                            # Add to list of better_states
                            better_states.append(current_move)
                        else:
                            # Restore the position of piece, not accept the changes
                            current_piece.set_x(original_position['x'])
                            current_piece.set_y(original_position['y'])
                    # There is/are better states, then choose randomly.
                    if (len(better_states) > 0):
                        idx = randint(0, len(better_states) - 1)
                        chosen_move = better_states[idx]
                        # Replace current position of piece with chosen move.
                        current_piece.set_x(chosen_move['x'])
                        current_piece.set_y(chosen_move['y'])
                        # Calculate heuristic after change to new position.
                        heuristic = board.calculate_heuristic()
                        current_heuristic = heuristic
                # Local maximum has reached because there is no possible piece moves,
                # that gives a better heuristic.
                if len(better_states) == 0:
                    local_maximum = True

            # Check if first iteration
            if iterationNum == 1:
                best_heuristic = current_heuristic
                best_board = copy(board)
            # Check if current heuristic is better than current best
            elif best_heuristic['total'] < current_heuristic['total']:
                best_heuristic = current_heuristic
                best_board = copy(board)

            # Exits code when goal has achieved, or local maximum achieved with maxIter.
            if current_heuristic['total'] == self.get_goal():
                break

            # Restart iteration.
            iterationNum += 1

        # Exits code when goal has achieved, or local maximum achieved with maxIter.
        if current_heuristic['total'] == self.get_goal():
            finish = round(time(), 3)

            print("Optimal solution found after", str(iterationNum), "iterations")
            print("Elapsed time = " + str(finish - start) + " seconds\n")
        else:
            # Maximum iterations reached.
            finish = round(time(), 3)

            print("Stochastic Hill Climbing approximates global optimum (with ", iterationNum - 1,
                  " iterations)")
            print("Elapsed time = " + str(finish - start) + " seconds\n")

        # Draw best Board
        best_board.draw()
        print("Conflicts amount: ", str(best_heuristic['a']))

        return
