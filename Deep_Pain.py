king1_moved = False
king2_moved = False

rook1_left = False
rook1_right = False

rook2_left = False
rook2_right = False

iteration = 0

def game():
    board = create_starting_board()
    player1_pawn_promotion_line = [26, 27, 28, 29, 30, 31, 32, 33]
    print_board(board)
    print("")
    print("")
    while True:
        castling = ""
        # castling:
        if board[110] == "r-1" and board[111] == " 0 " and board[112] == " 0 " and board[113] == " 0 " \
                and board[114] == "k-1":
            castling = input("Do you want to castle?")
            if castling == "y":
                x_piece = int(input("x_piece:"))
                y_piece = int(input("y_piece:"))
                x_move = int(input("x_move:"))
                y_move = int(input("y_move:"))

                piece_pos = (109 + x_piece) - (y_piece - 1) * 12
                move_pos = (109 + x_move) - (y_move - 1) * 12

                board[move_pos] = board[piece_pos]
                board[piece_pos] = " 0 "

                x_piece = int(input("x_piece:"))
                y_piece = int(input("y_piece:"))
                x_move = int(input("x_move:"))
                y_move = int(input("y_move:"))

                piece_pos = (109 + x_piece) - (y_piece - 1) * 12
                move_pos = (109 + x_move) - (y_move - 1) * 12

                board[move_pos] = board[piece_pos]
                board[piece_pos] = " 0 "
        if board[117] == "r-1" and board[116] == " 0 " and board[115] == " 0 " and board[114] == "k-1":
            castling = input("Do you want to castle?")
            if castling == "y":
                x_piece = int(input("x_piece:"))
                y_piece = int(input("y_piece:"))
                x_move = int(input("x_move:"))
                y_move = int(input("y_move:"))

                piece_pos = (109 + x_piece) - (y_piece - 1) * 12
                move_pos = (109 + x_move) - (y_move - 1) * 12

                board[move_pos] = board[piece_pos]
                board[piece_pos] = " 0 "

                x_piece = int(input("x_piece:"))
                y_piece = int(input("y_piece:"))
                x_move = int(input("x_move:"))
                y_move = int(input("y_move:"))

                piece_pos = (109 + x_piece) - (y_piece - 1) * 12
                move_pos = (109 + x_move) - (y_move - 1) * 12

                board[move_pos] = board[piece_pos]
                board[piece_pos] = " 0 "
        if castling != "y":
            x_piece = int(input("x_piece:"))
            y_piece = int(input("y_piece:"))
            x_move = int(input("x_move:"))
            y_move = int(input("y_move:"))

            piece_pos = (109 + x_piece) - (y_piece - 1) * 12
            move_pos = (109 + x_move) - (y_move - 1) * 12

            board[move_pos] = board[piece_pos]
            board[piece_pos] = " 0 "

            if "p-1" in board:
                if board.index("p-1") in player1_pawn_promotion_line:
                    board[move_pos] = "q-1"

        # check if king/queen has moved:
        global king1_moved, rook1_right, rook1_left
        if board[move_pos] == "k-1":
            king1_moved = False
        elif board[move_pos] == "r-1" and piece_pos == 110:
            rook1_left = False
        elif board[move_pos] == "r-1" and piece_pos == 117:
            rook1_right = False

        print_board(board)
        print("")
        print("")

        maximize(board, -1, 4, -100000, 100000)


def sort_moves(scores, piece_positions, possible_moves,  player):

    where_did_items_go = []

    if player == 1:
        sorted_scores = sorted(scores, reverse=True)
    else:
        sorted_scores = sorted(scores, reverse=False)

    for item in scores:
        num = sorted_scores.index(item)
        while num in where_did_items_go:
            num += 1
        where_did_items_go.append(num)

    piece = [x for _, x in sorted(zip(where_did_items_go, piece_positions))]
    possible = [x for _, x in sorted(zip(where_did_items_go, possible_moves))]

    return piece, possible


def maximize(board, player, depth, alpha, beta):
    max_depth = 4
    player2_pawn_promotion_line = [110, 111, 112, 113, 114, 115, 116, 117]
    pos = -1
    if depth == 0:
        return evaluation(board)
    max_value = alpha
    positions, moves = find_all_possible_moves(board, player)
    for move in moves:
        global iteration
        iteration += 1
        pawn_promotion = False
        pos += 1
        # perform move
        if isinstance(move, int):
            piece = board[move]
            board[move] = board[positions[pos]]
            board[positions[pos]] = " 0 "
            # pawn promotion
            if "p-2" in board:
                if player == -1 and board.index("p-2") in player2_pawn_promotion_line:
                    board[move] = "q-2"
                    pawn_promotion = True
            value = minimize(board, player * -1, depth - 1, max_value, beta)
            # reverse move
            if not pawn_promotion:
                board[positions[pos]] = board[move]
                board[move] = piece
            else:
                board[positions[pos]] = "p-2"
                board[move] = piece
        else:
            piece_1 = board[move[0]]
            piece_2 = board[move[1]]
            board[move[0]] = board[positions[pos][0]]
            board[move[1]] = board[positions[pos][1]]
            board[positions[pos][0]] = " 0 "
            board[positions[pos][1]] = " 0 "
            value = minimize(board, player * -1, depth - 1, max_value, beta)
            # reverse move
            board[positions[pos][0]] = board[move[0]]
            board[positions[pos][1]] = board[move[1]]
            board[move[0]] = piece_1
            board[move[1]] = piece_2
        if value >= max_value:
            max_value = value
            best_move = move
            best_piece = positions[pos]
            if max_value >= beta:
                break
    if depth == max_depth:
        # perform move + check if kings/rooks moved
        if moves == []:
            print("Check_Mate: You won!")
            exit()
        if isinstance(best_move, int):
            board[best_move] = board[best_piece]
            board[best_piece] = " 0 "
            # pawn promotion
            if "p-2" in board:
                if board.index("p-2") in player2_pawn_promotion_line:
                    board[best_move] = "q-2"
            # check if king/queen has moved:
            global king2_moved, rook2_right, rook2_left
            if board[best_move] == "k-2":
                king2_moved = True
            elif board[best_move] == "r-2" and best_piece == 26:
                rook2_left = True
            elif board[best_move] == "r-2" and best_piece == 33:
                rook2_right = True
        else:
            board[best_move[0]] = board[best_piece[0]]
            board[best_move[1]] = board[best_piece[1]]
            board[best_piece[0]] = " 0 "
            board[best_piece[1]] = " 0 "
        print_board(board)
        print(max_value)
        print(iteration)
        print("")
        print("")
    return max_value


def minimize(board, player, depth, alpha, beta):
    player1_pawn_promotion_line = [26, 27, 28, 29, 30, 31, 32, 33]
    pos = -1
    if depth == 0:
        return evaluation(board)
    min_value = beta
    positions, moves = find_all_possible_moves(board, player)
    for move in moves:
        global iteration
        iteration += 1
        pawn_promotion = False
        pos += 1
        # perform move
        if isinstance(move, int):
            piece = board[move]
            board[move] = board[positions[pos]]
            board[positions[pos]] = " 0 "
            # pawn promotion
            if "p-1" in board:
                if player == 1 and board.index("p-1") in player1_pawn_promotion_line:
                    board[move] = "q-1"
                    pawn_promotion = True
            value = maximize(board, player * -1, depth - 1, alpha, min_value)
            # reverse move
            if not pawn_promotion:
                board[positions[pos]] = board[move]
                board[move] = piece
            else:
                board[positions[pos]] = "p-1"
                board[move] = piece
        else:
            piece_1 = board[move[0]]
            piece_2 = board[move[1]]
            board[move[0]] = board[positions[pos][0]]
            board[move[1]] = board[positions[pos][1]]
            board[positions[pos][0]] = " 0 "
            board[positions[pos][1]] = " 0 "
            value = maximize(board, player * -1, depth - 1, alpha, min_value)
            # reverse move
            board[positions[pos][0]] = board[move[0]]
            board[positions[pos][1]] = board[move[1]]
            board[move[0]] = piece_1
            board[move[1]] = piece_2
        if value < min_value:
            min_value = value
            if min_value <= alpha:
                break
    return min_value


def evaluation(board):
    # simple material_count
    king = 3600
    queen = 360
    rook = 200
    bishop = 120
    knight = 120
    pawn = 40

    value = 0

    search_range = [26, 27, 28, 29, 30, 31, 32, 33,
                    38, 39, 40, 41, 42, 43, 44, 45,
                    50, 51, 52, 53, 54, 55, 56, 57,
                    62, 63, 64, 65, 66, 67, 68, 69,
                    74, 75, 76, 77, 78, 79, 80, 81,
                    86, 87, 88, 89, 90, 91, 92, 93,
                    98, 99, 100, 101, 102, 103, 104, 105,
                    110, 111, 112, 113, 114, 115, 116, 117]

    prawn_table_AI = [  0,  0,  0,  0,  0,  0,  0, 0,  0,  0, 0, 0,
                        0,  0,  0,  0,  0,  0,  0, 0,  0,  0, 0, 0,
                        0,  0,  0,  0,  0,  0,  0, 0,  0,  0, 0, 0,
                        0, 0, 10, 10,  5,-10,-10, 5, 10, 10, 0, 0,
                        0, 0, 5,  0,  5,  0,  0, 5,  0,  5, 0, 0,
                        0, 0, 0,  0,  5, 20, 20, 5,  0,  0, 0, 0,
                        0, 0, 0,  0,  0,  5,  5, 0,  0,  0, 0, 0,
                        0, 0, 5,  5,  5, 10, 10, 5,  5,  5, 0, 0,
                        0, 0, 10, 10, 10, 20, 20, 10, 10, 10, 0, 0,
                        0,  0,  0,  0,  0,  0,  0,  0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    knight_table_AI = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, -10, 0, 0, 0, 0, -10, 0, 0, 0,
                       0, 0, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 10, 10, 10, 10, 0, 0, 0, 0,
                       0, 0, 0, 0, 10, 15, 15, 10, 0, 0, 0, 0,
                       0, 0, 0, 0, 10, 15, 15, 10, 0, 0, 0, 0,
                       0, 0, 0, 0, 5, 10, 10, 5, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    bishop_table_AI = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, -10, 0, 0, -10, 0, 0, 0, 0,
                        0, 0,0, 0, 0, 5, 5, 0, 0, 0, 0, 0,
                        0, 0,0, 0, 5, 10, 10, 5, 0, 0, 0, 0,
                        0, 0,0, 5, 10, 15, 15, 10, 5, 0, 0, 0,
                        0, 0,0, 5, 10, 15, 15, 10, 5, 0, 0, 0,
                        0, 0,0, 0, 5, 10, 10, 5, 0, 0, 0, 0,
                        0, 0,0, 0, 0, 5, 5, 0, 0, 0, 0, 0,
                        0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    rook_table_AI = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 5, 10, 10, 5, 0, 0, 0, 0,
                     0, 0, 0, 0, 5, 10, 10, 5, 0, 0, 0, 0,
                     0, 0, 0, 0, 5, 10, 10, 5, 0, 0, 0, 0,
                     0, 0, 0, 0, 5, 10, 10, 5, 0, 0, 0, 0,
                     0, 0, 0, 0, 5, 10, 10, 5, 0, 0, 0, 0,
                     0, 0, 0, 0, 5, 10, 10, 5, 0, 0, 0, 0,
                     0, 0, 15, 15, 15, 15, 15, 15, 15, 15, 0, 0,
                     0, 0, 0, 0, 5, 10, 10, 5, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    prawn_table_H = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 10, 10, 10, 20, 20, 10, 10, 10, 0, 0,
                     0, 0, 5, 5, 5, 10, 10, 5, 5, 5, 0, 0,
                     0, 0, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 5, 20, 20, 5, 0, 0, 0, 0,
                     0, 0, 5, 0, 5, 0, 0, 5, 0, 5, 0, 0,
                     0, 0, 10, 10, 5, -10, -10, 5, 10, 10, 0, 0,
                     0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    knight_table_H = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 5, 10, 10, 5, 0, 0, 0, 0,
                      0, 0, 0, 0, 10, 15, 15, 10, 0, 0, 0, 0,
                      0, 0, 0, 0, 10, 15, 15, 10, 0, 0, 0, 0,
                      0, 0, 0, 0, 10, 10, 10, 10, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0,
                      0, 0, 0, -10, 0, 0, 0, 0, -10, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,]

    bishop_table_H = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 5, 10, 10, 5, 0, 0, 0, 0,
                      0, 0, 0, 5, 10, 15, 15, 10, 5, 0, 0, 0,
                      0, 0, 0, 5, 10, 15, 15, 10, 5, 0, 0, 0,
                      0, 0, 0, 0, 5, 10, 10, 5, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, -10, 0, 0, -10, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    rook_table_H = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 5, 10, 10, 5, 0, 0, 0, 0,
                    0, 0, 15, 15, 15, 15, 15, 15, 15, 15, 0, 0,
                    0, 0, 0, 0, 5, 10, 10, 5, 0, 0, 0, 0,
                    0, 0, 0, 0, 5, 10, 10, 5, 0, 0, 0, 0,
                    0, 0, 0, 0, 5, 10, 10, 5, 0, 0, 0, 0,
                    0, 0, 0, 0, 5, 10, 10, 5, 0, 0, 0, 0,
                    0, 0, 0, 0, 5, 10, 10, 5, 0, 0, 0, 0,
                    0, 0, 0, 0, 5, 10, 10, 5, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # material_score
    for square in search_range:
        if "1" in board[square]:
            player_string = "1"
            player_int = -1
        else:
            player_string = "2"
            player_int = 1

        if "p-" + player_string in board[square]:
            value = value + player_int * pawn
        if "n-" + player_string in board[square]:
            value = value + player_int * knight
        if "b-" + player_string in board[square]:
            value = value + player_int * bishop
        if "r-" + player_string in board[square]:
            value = value + player_int * rook
        if "q-" + player_string in board[square]:
            value = value + player_int * queen
        if "k-" + player_string in board[square]:
            value = value + player_int * king

    # position score
    for square in search_range:
        if "1" in board[square]:
            if "p" in board[square]:
                value -= prawn_table_H[square]
            if "b" in board[square]:
                value -= bishop_table_H[square]
            if "n" in board[square]:
                value -= knight_table_H[square]
            if "r" in board[square]:
                value -= rook_table_H[square]
        else:
            if "p" in board[square]:
                value += prawn_table_AI[square]
            if "b" in board[square]:
                value += bishop_table_AI[square]
            if "n" in board[square]:
                value += knight_table_AI[square]
            if "r" in board[square]:
                value += rook_table_AI[square]








    # Castling
    if board[31] == "r-2" and board[32] == "k-2":
        value += 4
    if board[29] == "r-2" and board[28] == "k-2":
        value += 4
    if board[115] == "r-1" and board[116] == "k-1":
        value -= 4
    if board[113] == "r-1" and board[112] == "k-1":
        value -= 4

    return value


def create_starting_board():
    board = ["x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x",
             "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x",
             "x", "x", "r-2", "n-2", "b-2", "q-2", "k-2", "b-2", "n-2", "r-2", "x", "x",
             "x", "x", "p-2", "p-2", "p-2", "p-2", "p-2", "p-2", "p-2", "p-2", "x", "x",
             "x", "x", " 0 ", " 0 ", " 0 ", " 0 ", " 0 ", " 0 ", " 0 ", " 0 ", "x", "x",
             "x", "x", " 0 ", " 0 ", " 0 ", " 0 ", " 0 ", " 0 ", " 0 ", " 0 ", "x", "x",
             "x", "x", " 0 ", " 0 ", " 0 ", " 0 ", " 0 ", " 0 ", " 0 ", " 0 ", "x", "x",
             "x", "x", " 0 ", " 0 ", " 0 ", " 0 ", " 0 ", " 0 ", " 0 ", " 0 ", "x", "x",
             "x", "x", "p-1", "p-1", "p-1", "p-1", "p-1", "p-1", "p-1", "p-1", "x", "x",
             "x", "x", "r-1", "n-1", "b-1", "q-1", "k-1", "b-1", "n-1", "r-1", "x", "x",
             "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x",
             "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x"]
    return board


def print_board(board):
    for i in range(8):
        if i > 0:
            print("---------------------------------")
        print("¦" + board[26 + i * 12] + "¦" + board[12 * i + 27] + "¦" + board[12 * i + 28] + "¦" + board[
            i * 12 + 29] + "¦" + board[12 * i + 30] + "¦" + board[12 * i + 31] + "¦" + board[12 * i + 32] + "¦"
              + board[12 * i + 33] + "¦")


def king_exists(board, player):
    search_range = [26, 27, 28, 29, 30, 31, 32, 33,
                    38, 39, 40, 41, 42, 43, 44, 45,
                    50, 51, 52, 53, 54, 55, 56, 57,
                    62, 63, 64, 65, 66, 67, 68, 69,
                    74, 75, 76, 77, 78, 79, 80, 81,
                    86, 87, 88, 89, 90, 91, 92, 93,
                    98, 99, 100, 101, 102, 103, 104, 105,
                    110, 111, 112, 113, 114, 115, 116, 117]
    if player == 1:
        player_string = "1"
    else:
        player_string = "2"
    for i in search_range:
        if "k-" + player_string in board[i]:
            return True
    return False


def king_under_attack(board, player):
    position, moves = make_all_next_moves(board, player * -1)
    pos = -1
    player1_pawn_promotion_line = [26, 27, 28, 29, 30, 31, 32, 33]
    player2_pawn_promotion_line = [110, 111, 112, 113, 114, 115, 116, 117]
    # perform all moves and check if in one of the moves the king doesn't exist, if true, then the king is under check
    # in the current board_state
    for move in moves:
        pawn_promotion = False
        pos += 1
        if isinstance(move, int):
            piece = board[move]
            board[move] = board[position[pos]]
            board[position[pos]] = " 0 "
            # pawn promotion
            if "p-1" in board:
                if player == 1 and board.index("p-1") in player1_pawn_promotion_line:
                    board[move] = "q-1"
                    pawn_promotion = True
            if "p-2" in board:
                if player == -1 and board.index("p-2") in player2_pawn_promotion_line:
                    board[move] = "q-2"
                    pawn_promotion = True
            if not king_exists(board, player):
                # reverse move
                if not pawn_promotion:
                    board[position[pos]] = board[move]
                    board[move] = piece
                else:
                    if player == 1:
                        board[position[pos]] = "p-1"
                        board[move] = piece
                    else:
                        board[position[pos]] = "p-2"
                        board[move] = piece
                return True
            # reverse move
            if not pawn_promotion:
                board[position[pos]] = board[move]
                board[move] = piece
            else:
                if player == 1:
                    board[position[pos]] = "p-1"
                    board[move] = piece
                else:
                    board[position[pos]] = "p-2"
                    board[move] = piece

        else:
            piece_1 = board[move[0]]
            piece_2 = board[move[1]]
            board[move[0]] = board[position[pos][0]]
            board[move[1]] = board[position[pos][1]]
            board[position[pos][0]] = " 0 "
            board[position[pos][1]] = " 0 "
            if not king_exists(board, player):
                # reverse move
                board[position[pos][0]] = board[move[0]]
                board[position[pos][1]] = board[move[1]]
                board[move[0]] = piece_1
                board[move[1]] = piece_2
                return True
            # reverse move
            board[position[pos][0]] = board[move[0]]
            board[position[pos][1]] = board[move[1]]
            board[move[0]] = piece_1
            board[move[1]] = piece_2
    return False


def make_all_next_moves(board, player):
    possible_moves = []
    piece_position = []
    search_range = [26, 27, 28, 29, 30, 31, 32, 33,
                    38, 39, 40, 41, 42, 43, 44, 45,
                    50, 51, 52, 53, 54, 55, 56, 57,
                    62, 63, 64, 65, 66, 67, 68, 69,
                    74, 75, 76, 77, 78, 79, 80, 81,
                    86, 87, 88, 89, 90, 91, 92, 93,
                    98, 99, 100, 101, 102, 103, 104, 105,
                    110, 111, 112, 113, 114, 115, 116, 117]
    pawn1_start = [98, 99, 100, 101, 102, 103, 104, 105]
    pawn2_start = [38, 39, 40, 41, 42, 43, 44, 45]

    if player == 1:
        player_string = "1"
        attack_player = "2"
        pawn_starting_positions = pawn1_start
    else:
        player_string = "2"
        attack_player = "1"
        pawn_starting_positions = pawn2_start
    # find all possible moves with pawn, bishop, knight, rook, queen and king
    for i in search_range:
        # pawn
        if "p-" + player_string in board[i]:
            # pawn_forward
            if board[i - player * 12] == " 0 ":
                piece_position.append(i)
                possible_moves.append(i - player * 12)
            # pawn_right
            if attack_player in board[i - player * 11]:
                piece_position.append(i)
                possible_moves.append(i - player * 11)
            # pawn_left
            if attack_player in board[i - player * 13]:
                piece_position.append(i)
                possible_moves.append(i - player * 13)
            # pawn_two_forward
            if board[i - player * 24] == " 0 " and board[i - player * 12] == " 0 " and i in pawn_starting_positions:
                piece_position.append(i)
                possible_moves.append(i - player * 24)

        # bishop
        if "b-" + player_string in board[i]:
            # bishop_up_right
            x = i
            while True:
                x = x - 11
                if board[x] == " 0 ":
                    piece_position.append(i)
                    possible_moves.append(x)
                elif attack_player in board[x]:
                    piece_position.append(i)
                    possible_moves.append(x)
                    break
                else:
                    break
            # bishop_up_left
            x = i
            while True:
                x = x - 13
                if board[x] == " 0 ":
                    piece_position.append(i)
                    possible_moves.append(x)
                elif attack_player in board[x]:
                    piece_position.append(i)
                    possible_moves.append(x)
                    break
                else:
                    break
            # bishop_down_left
            x = i
            while True:
                x = x + 11
                if board[x] == " 0 ":
                    piece_position.append(i)
                    possible_moves.append(x)
                elif attack_player in board[x]:
                    piece_position.append(i)
                    possible_moves.append(x)
                    break
                else:
                    break
            # bishop_down_right
            x = i
            while True:
                x = x + 13
                if board[x] == " 0 ":
                    piece_position.append(i)
                    possible_moves.append(x)
                elif attack_player in board[x]:
                    piece_position.append(i)
                    possible_moves.append(x)
                    break
                else:
                    break
        # knight
        if "n-" + player_string in board[i]:
            # 8 cases
            if " 0 " in board[i - 23] or attack_player in board[i - 23]:
                piece_position.append(i)
                possible_moves.append(i - 23)
            if " 0 " in board[i - 25] or attack_player in board[i - 25]:
                piece_position.append(i)
                possible_moves.append(i - 25)
            if " 0 " in board[i - 10] or attack_player in board[i - 10]:
                piece_position.append(i)
                possible_moves.append(i - 10)
            if " 0 " in board[i - 14] or attack_player in board[i - 14]:
                piece_position.append(i)
                possible_moves.append(i - 14)
            if " 0 " in board[i + 23] or attack_player in board[i + 23]:
                piece_position.append(i)
                possible_moves.append(i + 23)
            if " 0 " in board[i + 25] or attack_player in board[i + 25]:
                piece_position.append(i)
                possible_moves.append(i + 25)
            if " 0 " in board[i + 10] or attack_player in board[i + 10]:
                piece_position.append(i)
                possible_moves.append(i + 10)
            if " 0 " in board[i + 14] or attack_player in board[i + 14]:
                piece_position.append(i)
                possible_moves.append(i + 14)
        # rook
        if "r-" + player_string in board[i]:
            # rook_up
            x = i
            while True:
                x = x - 12
                if board[x] == " 0 ":
                    piece_position.append(i)
                    possible_moves.append(x)
                elif attack_player in board[x]:
                    piece_position.append(i)
                    possible_moves.append(x)
                    break
                else:
                    break
            # rook_down
            x = i
            while True:
                x = x + 12
                if board[x] == " 0 ":
                    piece_position.append(i)
                    possible_moves.append(x)
                elif attack_player in board[x]:
                    piece_position.append(i)
                    possible_moves.append(x)
                    break
                else:
                    break
            # rook_right
            x = i
            while True:
                x = x + 1
                if board[x] == " 0 ":
                    piece_position.append(i)
                    possible_moves.append(x)
                elif attack_player in board[x]:
                    piece_position.append(i)
                    possible_moves.append(x)
                    break
                else:
                    break
            # rook_left
            x = i
            while True:
                x = x - 1
                if board[x] == " 0 ":
                    piece_position.append(i)
                    possible_moves.append(x)
                elif attack_player in board[x]:
                    piece_position.append(i)
                    possible_moves.append(x)
                    break
                else:
                    break
        # queen
        if "q-" + player_string in board[i]:
            # queen_up
            x = i
            while True:
                x = x - 12
                if board[x] == " 0 ":
                    piece_position.append(i)
                    possible_moves.append(x)
                elif attack_player in board[x]:
                    piece_position.append(i)
                    possible_moves.append(x)
                    break
                else:
                    break
            # queen_down
            x = i
            while True:
                x = x + 12
                if board[x] == " 0 ":
                    piece_position.append(i)
                    possible_moves.append(x)
                elif attack_player in board[x]:
                    piece_position.append(i)
                    possible_moves.append(x)
                    break
                else:
                    break
            # queen_right
            x = i
            while True:
                x = x + 1
                if board[x] == " 0 ":
                    piece_position.append(i)
                    possible_moves.append(x)
                elif attack_player in board[x]:
                    piece_position.append(i)
                    possible_moves.append(x)
                    break
                else:
                    break
            # queen_left
            x = i
            while True:
                x = x - 1
                if board[x] == " 0 ":
                    piece_position.append(i)
                    possible_moves.append(x)
                elif attack_player in board[x]:
                    piece_position.append(i)
                    possible_moves.append(x)
                    break
                else:
                    break
            # queen_up_right
            x = i
            while True:
                x = x - 11
                if board[x] == " 0 ":
                    piece_position.append(i)
                    possible_moves.append(x)
                elif attack_player in board[x]:
                    piece_position.append(i)
                    possible_moves.append(x)
                    break
                else:
                    break
            # queen_up_left
            x = i
            while True:
                x = x - 13
                if board[x] == " 0 ":
                    piece_position.append(i)
                    possible_moves.append(x)
                elif attack_player in board[x]:
                    piece_position.append(i)
                    possible_moves.append(x)
                    break
                else:
                    break
            # queen_down_left
            x = i
            while True:
                x = x + 11
                if board[x] == " 0 ":
                    piece_position.append(i)
                    possible_moves.append(x)
                elif attack_player in board[x]:
                    piece_position.append(i)
                    possible_moves.append(x)
                    break
                else:
                    break
            # queen_down_right
            x = i
            while True:
                x = x + 13
                if board[x] == " 0 ":
                    piece_position.append(i)
                    possible_moves.append(x)
                elif attack_player in board[x]:
                    piece_position.append(i)
                    possible_moves.append(x)
                    break
                else:
                    break
        # king
        if "k-" + player_string in board[i]:
            # king_up
            if " 0 " in board[i - 12] or attack_player in board[i - 12]:
                piece_position.append(i)
                possible_moves.append(i - 12)
            # king_down
            if " 0 " in board[i + 12] or attack_player in board[i + 12]:
                piece_position.append(i)
                possible_moves.append(i + 12)
            # king_right
            if " 0 " in board[i + 1] or attack_player in board[i + 1]:
                piece_position.append(i)
                possible_moves.append(i + 1)
            # king_left
            if " 0 " in board[i - 1] or attack_player in board[i - 1]:
                piece_position.append(i)
                possible_moves.append(i - 1)
            # king_up_right
            if " 0 " in board[i - 11] or attack_player in board[i - 11]:
                piece_position.append(i)
                possible_moves.append(i - 11)
            # king_up_left
            if " 0 " in board[i - 13] or attack_player in board[i - 13]:
                piece_position.append(i)
                possible_moves.append(i - 13)
            # king_down_right
            if " 0 " in board[i + 11] or attack_player in board[i + 11]:
                piece_position.append(i)
                possible_moves.append(i + 11)
            # king_down_left
            if " 0 " in board[i + 13] or attack_player in board[i + 13]:
                piece_position.append(i)
                possible_moves.append(i + 13)
    # Castling
    global king1_moved, king2_moved, rook1_left, rook1_right, rook2_left, rook2_right
    if player == 1 and not king1_moved:
        # 2 castling options
        if board[110] == "r-1" and board[111] == " 0 " and board[112] == " 0 " \
                and board[113] == " 0 " and board[114] == "k-1" and not rook1_left:
            piece_position.append([114, 110])
            possible_moves.append([112, 113])
        if board[117] == "r-1" and board[116] == " 0 " and board[115] == " 0 " \
                and board[114] == "k-1" and not rook1_right:
            piece_position.append([114, 117])
            possible_moves.append([116, 115])
    if player == -1 and not king2_moved:
        # 2 castling options
        if board[26] == "r-2" and board[27] == " 0 " and board[28] == " 0 " \
                and board[29] == " 0 " and board[30] == "k-2" and not rook2_left:
            piece_position.append([30, 26])
            possible_moves.append([28, 29])
        if board[33] == "r-2" and board[32] == " 0 " and board[31] == " 0 " \
                and board[30] == "k-2" and not rook2_right:
            piece_position.append([30, 33])
            possible_moves.append([32, 31])

    # En passe --> maybe add it later on (a bit unnessecary but okay i guess i'll just add it later)

    return piece_position, possible_moves


def find_all_possible_moves(board, player):
    possible_moves = []
    piece_position = []
    search_range = [26, 27, 28, 29, 30, 31, 32, 33,
                    38, 39, 40, 41, 42, 43, 44, 45,
                    50, 51, 52, 53, 54, 55, 56, 57,
                    62, 63, 64, 65, 66, 67, 68, 69,
                    74, 75, 76, 77, 78, 79, 80, 81,
                    86, 87, 88, 89, 90, 91, 92, 93,
                    98, 99, 100, 101, 102, 103, 104, 105,
                    110, 111, 112, 113, 114, 115, 116, 117]
    pawn1_start = [98, 99, 100, 101, 102, 103, 104, 105]
    pawn2_start = [38, 39, 40, 41, 42, 43, 44, 45]

    if player == 1:
        player_string = "1"
        attack_player = "2"
        pawn_starting_positions = pawn1_start
    else:
        player_string = "2"
        attack_player = "1"
        pawn_starting_positions = pawn2_start
    # find all possible moves with pawn, bishop, knight, rook, queen and king
    for i in search_range:
        # pawn
        if "p-" + player_string in board[i]:
            # pawn_forward
            if board[i - player * 12] == " 0 ":
                piece_position.append(i)
                possible_moves.append(i - player * 12)
            # pawn_right
            if attack_player in board[i - player * 11]:
                piece_position.append(i)
                possible_moves.append(i - player * 11)
            # pawn_left
            if attack_player in board[i - player * 13]:
                piece_position.append(i)
                possible_moves.append(i - player * 13)
            # pawn_two_forward
            if board[i - player * 24] == " 0 " and board[i - player * 12] == " 0 " and i in pawn_starting_positions:
                piece_position.append(i)
                possible_moves.append(i - player * 24)
        # bishop
        if "b-" + player_string in board[i]:
            # bishop_up_right
            x = i
            while True:
                x = x - 11
                if board[x] == " 0 ":
                    piece_position.append(i)
                    possible_moves.append(x)
                elif attack_player in board[x]:
                    piece_position.append(i)
                    possible_moves.append(x)
                    break
                else:
                    break
            # bishop_up_left
            x = i
            while True:
                x = x - 13
                if board[x] == " 0 ":
                    piece_position.append(i)
                    possible_moves.append(x)
                elif attack_player in board[x]:
                    piece_position.append(i)
                    possible_moves.append(x)
                    break
                else:
                    break
            # bishop_down_left
            x = i
            while True:
                x = x + 11
                if board[x] == " 0 ":
                    piece_position.append(i)
                    possible_moves.append(x)
                elif attack_player in board[x]:
                    piece_position.append(i)
                    possible_moves.append(x)
                    break
                else:
                    break
            # bishop_down_right
            x = i
            while True:
                x = x + 13
                if board[x] == " 0 ":
                    piece_position.append(i)
                    possible_moves.append(x)
                elif attack_player in board[x]:
                    piece_position.append(i)
                    possible_moves.append(x)
                    break
                else:
                    break
        # knight
        if "n-" + player_string in board[i]:
            # 8 cases
            if " 0 " in board[i - 23] or attack_player in board[i - 23]:
                piece_position.append(i)
                possible_moves.append(i - 23)
            if " 0 " in board[i - 25] or attack_player in board[i - 25]:
                piece_position.append(i)
                possible_moves.append(i - 25)
            if " 0 " in board[i - 10] or attack_player in board[i - 10]:
                piece_position.append(i)
                possible_moves.append(i - 10)
            if " 0 " in board[i - 14] or attack_player in board[i - 14]:
                piece_position.append(i)
                possible_moves.append(i - 14)
            if " 0 " in board[i + 23] or attack_player in board[i + 23]:
                piece_position.append(i)
                possible_moves.append(i + 23)
            if " 0 " in board[i + 25] or attack_player in board[i + 25]:
                piece_position.append(i)
                possible_moves.append(i + 25)
            if " 0 " in board[i + 10] or attack_player in board[i + 10]:
                piece_position.append(i)
                possible_moves.append(i + 10)
            if " 0 " in board[i + 14] or attack_player in board[i + 14]:
                piece_position.append(i)
                possible_moves.append(i + 14)
        # rook
        if "r-" + player_string in board[i]:
            # rook_up
            x = i
            while True:
                x = x - 12
                if board[x] == " 0 ":
                    piece_position.append(i)
                    possible_moves.append(x)
                elif attack_player in board[x]:
                    piece_position.append(i)
                    possible_moves.append(x)
                    break
                else:
                    break
            # rook_down
            x = i
            while True:
                x = x + 12
                if board[x] == " 0 ":
                    piece_position.append(i)
                    possible_moves.append(x)
                elif attack_player in board[x]:
                    piece_position.append(i)
                    possible_moves.append(x)
                    break
                else:
                    break
            # rook_right
            x = i
            while True:
                x = x + 1
                if board[x] == " 0 ":
                    piece_position.append(i)
                    possible_moves.append(x)
                elif attack_player in board[x]:
                    piece_position.append(i)
                    possible_moves.append(x)
                    break
                else:
                    break
            # rook_left
            x = i
            while True:
                x = x - 1
                if board[x] == " 0 ":
                    piece_position.append(i)
                    possible_moves.append(x)
                elif attack_player in board[x]:
                    piece_position.append(i)
                    possible_moves.append(x)
                    break
                else:
                    break
        # queen
        if "q-" + player_string in board[i]:
            # queen_up
            x = i
            while True:
                x = x - 12
                if board[x] == " 0 ":
                    piece_position.append(i)
                    possible_moves.append(x)
                elif attack_player in board[x]:
                    piece_position.append(i)
                    possible_moves.append(x)
                    break
                else:
                    break
            # queen_down
            x = i
            while True:
                x = x + 12
                if board[x] == " 0 ":
                    piece_position.append(i)
                    possible_moves.append(x)
                elif attack_player in board[x]:
                    piece_position.append(i)
                    possible_moves.append(x)
                    break
                else:
                    break
            # queen_right
            x = i
            while True:
                x = x + 1
                if board[x] == " 0 ":
                    piece_position.append(i)
                    possible_moves.append(x)
                elif attack_player in board[x]:
                    piece_position.append(i)
                    possible_moves.append(x)
                    break
                else:
                    break
            # queen_left
            x = i
            while True:
                x = x - 1
                if board[x] == " 0 ":
                    piece_position.append(i)
                    possible_moves.append(x)
                elif attack_player in board[x]:
                    piece_position.append(i)
                    possible_moves.append(x)
                    break
                else:
                    break
            # queen_up_right
            x = i
            while True:
                x = x - 11
                if board[x] == " 0 ":
                    piece_position.append(i)
                    possible_moves.append(x)
                elif attack_player in board[x]:
                    piece_position.append(i)
                    possible_moves.append(x)
                    break
                else:
                    break
            # queen_up_left
            x = i
            while True:
                x = x - 13
                if board[x] == " 0 ":
                    piece_position.append(i)
                    possible_moves.append(x)
                elif attack_player in board[x]:
                    piece_position.append(i)
                    possible_moves.append(x)
                    break
                else:
                    break
            # queen_down_left
            x = i
            while True:
                x = x + 11
                if board[x] == " 0 ":
                    piece_position.append(i)
                    possible_moves.append(x)
                elif attack_player in board[x]:
                    piece_position.append(i)
                    possible_moves.append(x)
                    break
                else:
                    break
            # queen_down_right
            x = i
            while True:
                x = x + 13
                if board[x] == " 0 ":
                    piece_position.append(i)
                    possible_moves.append(x)
                elif attack_player in board[x]:
                    piece_position.append(i)
                    possible_moves.append(x)
                    break
                else:
                    break
        # king
        if "k-" + player_string in board[i]:
            # king_up
            if " 0 " in board[i - 12] or attack_player in board[i - 12]:
                piece_position.append(i)
                possible_moves.append(i - 12)
            # king_down
            if " 0 " in board[i + 12] or attack_player in board[i + 12]:
                piece_position.append(i)
                possible_moves.append(i + 12)
            # king_right
            if " 0 " in board[i + 1] or attack_player in board[i + 1]:
                piece_position.append(i)
                possible_moves.append(i + 1)
            # king_left
            if " 0 " in board[i - 1] or attack_player in board[i - 1]:
                piece_position.append(i)
                possible_moves.append(i - 1)
            # king_up_right
            if " 0 " in board[i - 11] or attack_player in board[i - 11]:
                piece_position.append(i)
                possible_moves.append(i - 11)
            # king_up_left
            if " 0 " in board[i - 13] or attack_player in board[i - 13]:
                piece_position.append(i)
                possible_moves.append(i - 13)
            # king_down_right
            if " 0 " in board[i + 11] or attack_player in board[i + 11]:
                piece_position.append(i)
                possible_moves.append(i + 11)
            # king_down_left
            if " 0 " in board[i + 13] or attack_player in board[i + 13]:
                piece_position.append(i)
                possible_moves.append(i + 13)

    # Castling
    global king1_moved, king2_moved, rook1_left, rook1_right, rook2_left, rook2_right
    if not king_under_attack(board, player):
        if player == 1 and not king1_moved:
            # 2 castling options
            if board[110] == "r-1" and board[111] == " 0 " and board[112] == " 0 " \
                    and board[113] == " 0 " and board[114] == "k-1" and not rook1_left:
                piece_position.append([114, 110])
                possible_moves.append([112, 113])
            if board[117] == "r-1" and board[116] == " 0 " and board[115] == " 0 " \
                    and board[114] == "k-1" and not rook1_right:
                piece_position.append([114, 117])
                possible_moves.append([116, 115])
        if player == -1 and not king2_moved:
            # 2 castling options
            if board[26] == "r-2" and board[27] == " 0 " and board[28] == " 0 " \
                    and board[29] == " 0 " and board[30] == "k-2" and not rook2_left:
                piece_position.append([30, 26])
                possible_moves.append([28, 29])
            if board[33] == "r-2" and board[32] == " 0 " and board[31] == " 0 " \
                    and board[30] == "k-2" and not rook2_right:
                piece_position.append([30, 33])
                possible_moves.append([32, 31])

    scores = []
    player1_pawn_promotion_line = [26, 27, 28, 29, 30, 31, 32, 33]
    player2_pawn_promotion_line = [110, 111, 112, 113, 114, 115, 116, 117]
    for i in range(len(possible_moves) - 1, -1, -1):
        pawn_promotion = False
        deletion = False
        if isinstance(possible_moves[i], int):
            piece = board[possible_moves[i]]
            board[possible_moves[i]] = board[piece_position[i]]
            board[piece_position[i]] = " 0 "
            # pawn promotion
            if "p-1" in board:
                if player == 1 and board.index("p-1") in player1_pawn_promotion_line:
                    board[possible_moves[i]] = "q-1"
                    pawn_promotion = True
            if "p-2" in board:
                if player == -1 and board.index("p-2") in player2_pawn_promotion_line:
                    board[possible_moves[i]] = "q-2"
                    pawn_promotion = True
            if king_under_attack(board, player):
                deletion = True
            else:
                # add score for move ordering
                scores.append(evaluation(board))
            # reverse move
            if not pawn_promotion:
                board[piece_position[i]] = board[possible_moves[i]]
                board[possible_moves[i]] = piece
            else:
                if player == 1:
                    board[piece_position[i]] = "p-1"
                    board[possible_moves[i]] = piece
                else:
                    board[piece_position[i]] = "p-2"
                    board[possible_moves[i]] = piece
        else:
            piece_1 = board[possible_moves[i][0]]
            piece_2 = board[possible_moves[i][1]]
            board[possible_moves[i][0]] = board[piece_position[i][0]]
            board[possible_moves[i][1]] = board[piece_position[i][1]]
            board[piece_position[i][0]] = " 0 "
            board[piece_position[i][1]] = " 0 "
            if king_under_attack(board, player):
                deletion = True
            else:
                # add score for move ordering
                scores.append(evaluation(board))
            # reverse move
            board[piece_position[i][0]] = board[possible_moves[i][0]]
            board[piece_position[i][1]] = board[possible_moves[i][1]]
            board[possible_moves[i][0]] = piece_1
            board[possible_moves[i][1]] = piece_2
        if deletion:
            del possible_moves[i]
            del piece_position[i]

    # En passe --> maybe add it later on (a bit unnecessary but okay i guess i'll just add it later)

    piece_position, possible_moves = sort_moves(scores, piece_position,possible_moves, player)

    return piece_position, possible_moves

game()
