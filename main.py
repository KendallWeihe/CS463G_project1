import numpy as np
import pdb

def find_filled_tubes(puzzle):

    filled_tubes = []

    for i in range(6):
        temp_vector = puzzle[i,:].copy()
        lower_tube = temp_vector[0:6-i]
        if len(lower_tube[lower_tube > 1]) == 6-i:
            filled_tubes.append(i)

    return np.array(filled_tubes)

#extract random number of filled tubes
def extract_rand_num_of_filled_tubes(filled_tubes):
    try:
        rand_size = np.random.randint(1,max(len(filled_tubes),2))
    except:
        pdb.set_trace()
    filled_tubes_random = np.random.choice(filled_tubes, rand_size, 0)
    filled_tubes_random = np.sort(filled_tubes_random)
    return filled_tubes_random

#verify that no tubes where balls have been dropped are adjacent in the
    #in the direction of the turn
def verify_adjacent_tubes(filled_tubes_random, num_consecutive_moves, direction):
    tail = 0
    head = 0
    tubes_where_balls_fell = []
    while 1:
        string_of_filled_tubes = 0
        for i in range(num_consecutive_moves):

            if tail+i == 6: next_tube = 0
            elif tail+i == 7: next_tube = 1
            else: next_tube = tail+i

            if next_tube in filled_tubes_random:
                string_of_filled_tubes = string_of_filled_tubes + 1
                head = next_tube

        if string_of_filled_tubes == num_consecutive_moves:
            if direction == 0:
                index_where_ball_fell = tail - 1
                if tail == 0: index_where_ball_fell = 5
            else:
                index_where_ball_fell = head + 1
                if head == 5: index_where_ball_fell = 0
            if index_where_ball_fell not in filled_tubes_random:
                tubes_where_balls_fell.append(index_where_ball_fell)

        tail = tail + 1

        if tail == 6:
            break

    return np.sort(np.array(tubes_where_balls_fell))

def generate_random_ball_drops(tubes_where_balls_fell, puzzle, direction):
    #generate random extraction from filled_tubes_verified
    #iterate through index's defined above ^^
            #the actual tube where the balls dropped will be adajcent to the above iteration values^^
        #generate random number where the range is min(actual balls,size_of_upper_tube)
            #this will be the number of balls that were dropped in that tube
        #splice off that ^^ number of the balls on top
        #fill in those balls in a tube size of the upper tube
        #blank puzzle index beyond this point
    #iterate through the index's not defined above ^^
        #splice off all values above the fill line
    #by this point we will have temp variables where all we need to do is place them above the fill lines of the puzzle

    try:
        balls_that_fell = []
        for i in range(len(tubes_where_balls_fell)):
            temp_vector = puzzle[tubes_where_balls_fell[i],:].copy()
            num_balls_in_tube = len(temp_vector[temp_vector > 1])
            size_of_upper_tube = len(temp_vector[temp_vector > 0]) - (6-tubes_where_balls_fell[i])
            if size_of_upper_tube != 1:
                rand_num_balls = np.random.randint(min(num_balls_in_tube, size_of_upper_tube-1))
            else:
                rand_num_balls = 0
            starting_index = num_balls_in_tube - rand_num_balls
            ending_index = starting_index + rand_num_balls
            if len(temp_vector[starting_index:ending_index]) > 0:
                balls_that_fell.append(temp_vector[starting_index:ending_index])
                puzzle[tubes_where_balls_fell[i], starting_index:ending_index] = 1
            else:
                current_tube_index = tubes_where_balls_fell[i]
                balls_that_fell.append(temp_vector[6-current_tube_index:6-current_tube_index+size_of_upper_tube])
                puzzle[tubes_where_balls_fell[i], starting_index:ending_index] = 1

        if balls_that_fell: return np.asarray(balls_that_fell)
        else:
            balls_that_fell.append(np.array([1]))
            return np.array(balls_that_fell)
    except:
        pdb.set_trace()

def rotate(temp_puzzle, puzzle, current_tube, previous_tube, i, balls_that_fell, index_balls_fell_into, direction, falling_balls_index):

    try:
        if direction == 0:
            if i == 0: prev_tube_index = 5
            else: prev_tube_index = i-1
        else:
            if i == 5: prev_tube_index = 0
            else: prev_tube_index = i+1


        prev_tube = previous_tube
        len_of_prev_upper_tube = len(prev_tube[prev_tube > 0]) - (6-prev_tube_index)
        end_of_balls_index = len(current_tube[current_tube > 1])
        len_new_tube = (6-i) + len_of_prev_upper_tube
        if prev_tube_index in index_balls_fell_into:
            num_that_fell = len(balls_that_fell[falling_balls_index])
            puzzle[i, min(end_of_balls_index,6-i):min(end_of_balls_index,6-i)+num_that_fell] = balls_that_fell[falling_balls_index]
            puzzle[i, min(end_of_balls_index,6-i)+num_that_fell:len_new_tube] = 1
            falling_balls_index = falling_balls_index + 1

        else:
            puzzle[i,min(end_of_balls_index,6-i):min(end_of_balls_index,6-i)+len_of_prev_upper_tube] = prev_tube[6-prev_tube_index:6-prev_tube_index+len_of_prev_upper_tube]
            puzzle[i,min(end_of_balls_index,6-i)+len_of_prev_upper_tube:len_new_tube] = 1
        puzzle[i,len_new_tube:13] = 0

        return puzzle, falling_balls_index
    except:
        pdb.set_trace()
        print "broadcast error"

def check_if_legal_move(puzzle, current_tubes, next_tubes, direction):

    for i in range(6):
        # set direction indices
        # if next_tube < fill line and current > fill line, then not a legal move
        if direction == 0:
            if i == 5: next_tube_capacity = 1
            else: next_tube_capacity = 6-i-1
        else:
            if i == 0: next_tube_capacity = 1
            else: next_tube_capacity = 6-i+1

        current_tube_capacity = 6-i

        next_tube = next_tubes[i]
        num_balls_in_next_tube = len(next_tube[next_tube > 1])
        current_tube = current_tubes[i]
        num_balls_in_current_tube = len(current_tube[current_tube > 1])

        if num_balls_in_next_tube < next_tube_capacity and num_balls_in_current_tube > current_tube_capacity:
            # print "this is an illegal move"
            # pdb.set_trace()
            return False

    # pdb.set_trace()
    return True

        # if num_balls_in_current_tube

def call_rotate(puzzle, direction, num_in_a_row):

    current_tubes = {
        0: puzzle[0,:].copy(),
        1: puzzle[1,:].copy(),
        2: puzzle[2,:].copy(),
        3: puzzle[3,:].copy(),
        4: puzzle[4,:].copy(),
        5: puzzle[5,:].copy()
    }

    if direction == 1:
        next_tubes = {
            0: puzzle[5,:].copy(),
            1: puzzle[0,:].copy(),
            2: puzzle[1,:].copy(),
            3: puzzle[2,:].copy(),
            4: puzzle[3,:].copy(),
            5: puzzle[4,:].copy()
        }
    else:
        next_tubes = {
            0: puzzle[1,:].copy(),
            1: puzzle[2,:].copy(),
            2: puzzle[3,:].copy(),
            3: puzzle[4,:].copy(),
            4: puzzle[5,:].copy(),
            5: puzzle[0,:].copy()
        }

    is_legal = check_if_legal_move(puzzle, current_tubes, next_tubes, direction)

    if is_legal:

        temp_puzzle = puzzle.copy()

        filled_tubes = find_filled_tubes(puzzle)
        filled_tubes_random = extract_rand_num_of_filled_tubes(filled_tubes)
        # if num_consec_moves > 1 call the below function
        index_balls_fell_into = verify_adjacent_tubes(filled_tubes_random, num_in_a_row, direction)
        balls_that_fell = generate_random_ball_drops(index_balls_fell_into, puzzle, direction)
        if direction == 0:
            previous_tubes = {
                0: puzzle[5,:].copy(),
                1: puzzle[0,:].copy(),
                2: puzzle[1,:].copy(),
                3: puzzle[2,:].copy(),
                4: puzzle[3,:].copy(),
                5: puzzle[4,:].copy()
            }
        else:
            previous_tubes = {
                0: puzzle[1,:].copy(),
                1: puzzle[2,:].copy(),
                2: puzzle[3,:].copy(),
                3: puzzle[4,:].copy(),
                4: puzzle[5,:].copy(),
                5: puzzle[0,:].copy()
            }
        falling_balls_index = 0
        for i in range(6):
            puzzle, falling_balls_index = rotate(temp_puzzle, puzzle, current_tubes[i], previous_tubes[i], i, balls_that_fell, index_balls_fell_into, direction, falling_balls_index)
        # pdb.set_trace()

    # pdb.set_trace()
    return puzzle, is_legal

def flip(puzzle):
    # print "flip"
    puzzle_temp = np.zeros((6,13))
    red_tube = puzzle[0,:].copy()
    green_tube = puzzle[1,:].copy()
    yellow_tube = puzzle[2,:].copy()
    blue_tube = puzzle[3,:].copy()
    white_tube = puzzle[4,:].copy()
    black_tube = puzzle[5,:].copy()

    for i in range(6):
        if i == 0:
            # find the size of the top tube
            # flip
            # reorder 0's and 1's
            # store in index ^^
            size_vector = red_tube[6:13]
            top_tube_size = len(size_vector[size_vector > 0])
            flip_vector = red_tube[red_tube > 1]
            flip_vector = np.flipud(flip_vector)
            red_tube[0:len(flip_vector)] = flip_vector
            puzzle[6-top_tube_size,:] = red_tube
        if i == 1:
            size_vector = green_tube[5:13]
            top_tube_size = len(size_vector[size_vector > 0])
            flip_vector = green_tube[green_tube > 1]
            flip_vector = np.flipud(flip_vector)
            green_tube[0:len(flip_vector)] = flip_vector
            puzzle[6-top_tube_size,:] = green_tube
        if i == 2:
            size_vector = yellow_tube[4:13]
            top_tube_size = len(size_vector[size_vector > 0])
            flip_vector = yellow_tube[yellow_tube > 1]
            flip_vector = np.flipud(flip_vector)
            yellow_tube[0:len(flip_vector)] = flip_vector
            puzzle[6-top_tube_size,:] = yellow_tube
        if i == 3:
            size_vector = blue_tube[3:13]
            top_tube_size = len(size_vector[size_vector > 0])
            flip_vector = blue_tube[blue_tube > 1]
            flip_vector = np.flipud(flip_vector)
            blue_tube[0:len(flip_vector)] = flip_vector
            puzzle[6-top_tube_size,:] = blue_tube
        if i == 4:
            size_vector = white_tube[2:13]
            top_tube_size = len(size_vector[size_vector > 0])
            flip_vector = white_tube[white_tube > 1]
            flip_vector = np.flipud(flip_vector)
            white_tube[0:len(flip_vector)] = flip_vector
            puzzle[6-top_tube_size,:] = white_tube
        if i == 5:
            size_vector = black_tube[1:13]
            top_tube_size = len(size_vector[size_vector > 0])
            flip_vector = black_tube[black_tube > 1]
            flip_vector = np.flipud(flip_vector)
            black_tube[0:len(flip_vector)] = flip_vector
            puzzle[6-top_tube_size,:] = black_tube

    return puzzle

def forward_rotate(puzzle, direction):

    current_tubes = {
        0: puzzle[0,:].copy(),
        1: puzzle[1,:].copy(),
        2: puzzle[2,:].copy(),
        3: puzzle[3,:].copy(),
        4: puzzle[4,:].copy(),
        5: puzzle[5,:].copy()
    }

    if direction == 0:
        previous_tubes = {
            0: puzzle[5,:].copy(),
            1: puzzle[0,:].copy(),
            2: puzzle[1,:].copy(),
            3: puzzle[2,:].copy(),
            4: puzzle[3,:].copy(),
            5: puzzle[4,:].copy()
        }
    else:
        previous_tubes = {
            0: puzzle[1,:].copy(),
            1: puzzle[2,:].copy(),
            2: puzzle[3,:].copy(),
            3: puzzle[4,:].copy(),
            4: puzzle[5,:].copy(),
            5: puzzle[0,:].copy()
        }
    falling_balls_index = 0
    temp_puzzle = puzzle.copy()
    for i in range(6):
        puzzle, falling_balls_index = rotate(temp_puzzle, puzzle, current_tubes[i], previous_tubes[i], i, [], [], direction, falling_balls_index)

    # pdb.set_trace()
    return puzzle


k = input("Please enter the number of moves you would like to shuffle the puzzle: ")


solved = False
while not solved:

    puzzle = np.zeros((6,13))
    for i in range(6):
        puzzle[i,6-i:12-i*2] = 1

    puzzle[0,0:6] = 2
    puzzle[1,0:5] = 3
    puzzle[2,0:4] = 4
    puzzle[3,0:3] = 5
    puzzle[4,0:2] = 6
    puzzle[5,0:1] = 7

    random_sequence = []
    for i in range(k):
        random_sequence.append(np.random.randint(0,3))

    random_sequence = np.array(random_sequence)
    for i in range(len(random_sequence)):
        look_ahead = 1
        for j in range(len(random_sequence)-1):
            if random_sequence[j] == random_sequence[j+1]:
                look_ahead = look_ahead + 1
            else:
                break

        is_legal = True
        if random_sequence[i] == 0:
            puzzle, is_legal = call_rotate(puzzle, 0, look_ahead)
        elif random_sequence[i] == 1:
            puzzle, is_legal = call_rotate(puzzle, 1, look_ahead)
        else:
            puzzle = flip(puzzle)

        if is_legal == False:
            random_sequence = np.append(random_sequence, np.random.randint(3))
            random_sequence[i] = -1

    random_sequence = random_sequence[random_sequence > -1]
    backwards_sequence = np.flipud(random_sequence)

    for i in range(len(backwards_sequence)):
        if backwards_sequence[i] == 0:
            puzzle = forward_rotate(puzzle, 1)
        elif backwards_sequence[i] == 1:
            puzzle = forward_rotate(puzzle, 0)
        else:
            puzzle = flip(puzzle)


    red_tube = (puzzle[0,:] == [ 2.,  2.,  2.,  2.,  2.,  2.,  1.,  1.,  1.,  1.,  1.,  1.,  0.])
    green_tube = (puzzle[1,:] == [ 3.,  3.,  3.,  3.,  3.,  1.,  1.,  1.,  1.,  1.,  0.,  0.,  0.])
    yellow_tube = (puzzle[2,:] == [ 4.,  4.,  4.,  4.,  1.,  1.,  1.,  1.,  0.,  0.,  0.,  0.,  0.])
    blue_tube = (puzzle[3,:] == [ 5.,  5.,  5.,  1.,  1.,  1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.])
    white_tube = (puzzle[4,:] == [ 6.,  6.,  1.,  1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.])
    black_tube = (puzzle[5,:] == [ 7.,  1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.])

    if np.sum(red_tube) == np.sum(green_tube) == np.sum(yellow_tube) == np.sum(blue_tube) == np.sum(white_tube) == np.sum(black_tube):
        solved = True

pdb.set_trace()
print
