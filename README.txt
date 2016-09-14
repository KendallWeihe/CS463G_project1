Kendall Weihe
CS463G Project 1

Data structure: I use a very raw data structure. I have a simple 2D array [6x13].

    Index 0 is the red tube, so there are 6 spaces until the *rotation line*.
    Index 1 is the green tube, so there are 5 spaces until the rotation line.
    Index 2 is the yellow tube, so there are 4 spaces until the rotation line.
    Index 3 is the blue tube, so there are 3 spaces until the rotation line.
    Index 4 is the white tube, so there are 2 spaces until the rotation line.
    Index 5 is the black tube, so there is 1 space until the rotation line.
      Note: it is important you understand that the rotation line does not
            vertically line up

  In the case of a flip, where the upper tubes are potentially different
  lengths, the tubes are reorganized so that the above indexing specification
  remains true.

    Values:
      0 = non existent (end of tube)
      1 = empty space
      2 = red
      3 = green
      4 = yellow
      5 = blue
      6 = white
      7 = black

  I wrote the program in Python. Python has a library called NumPy, and it has
  clean tricks for indexing. For example, vector[3:6] are all elements between
  indices 3 and 6. I initialize the data structure (in a solved state) with
  the following code:

      puzzle = np.zeros((6,13))
      for i in range(6):
          puzzle[i,6-i:12-i*2] = 1

      puzzle[0,0:6] = 2
      puzzle[1,0:5] = 3
      puzzle[2,0:4] = 4
      puzzle[3,0:3] = 5
      puzzle[4,0:2] = 6
      puzzle[5,0:1] = 7

  An example output of what the puzzle looks like (solved) is as follows:

    array([[ 2.,  2.,  2.,  2.,  2.,  2.,  1.,  1.,  1.,  1.,  1.,  1.,  0.],
           [ 3.,  3.,  3.,  3.,  3.,  1.,  1.,  1.,  1.,  1.,  0.,  0.,  0.],
           [ 4.,  4.,  4.,  4.,  1.,  1.,  1.,  1.,  0.,  0.,  0.,  0.,  0.],
           [ 5.,  5.,  5.,  1.,  1.,  1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
           [ 6.,  6.,  1.,  1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
           [ 7.,  1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.]])

Program requirements:

  Generate a list of random moves, where a move is one of three things:
    - reverse rotate left
    - reverse rotate right
    - flip

  Call a function that does the reverse moves.

  The tricky part about this project is building a state that I know
  can be solved in k steps (a requirement for Project 2). In order to reach this
  state I need to do *reverse moves* -- which are NOT normal moves (moves that can be made on the actual puzzle by a human).
  For example, a human rotating the puzzle forward could results in a ball dropping from one tube into
  another. But doing this in reverse, the program must move the ball from the lower
  tube to the top of the adjacent tube.


  PART I:
  My code finds tubes that are filled to at least the fill line. Then, since these tubes
  are filled, there is a possibility that they could have dropped a ball into an
  adjacent tube, as shown in the figure below.

          _<-0______
          | |0| |0|
          |0|0|0|--
          --|0|0|
            --|0|
              --

  PART II
  There is another constraint that must be handled with this implementation. Imagine
  I had the above configuration after I completed the turn (where the arrow points).
  But I knew that the user actually made *two* consecutive turns in that direction in
  order to get to the shown state (after moving the ball down to the left).
  If I simply checked adjacent tubes and then moved two turns in reverse,
  then the ball would now be under the rotation line in tube #3. If I wanted to
  make real-life moves to get back to my original state, there would be
  no two moves that would get me there. The state after two reverse moves would look
  like the following diagram (notice the ball is in tube #3).

          _________
          | |0|0|0|
          |0|0|0|--
          --|0|0|
            --|0|
              --

  To handle the above problem, the randomizer must lookahead to see how many consecutive
  moves are made. If, like above, there are two consecutive turns to the left, then the
  program must find a tube to the "left" where there are two tubes to the right that
  are at least filled to the rotation line.

  PART III
  Furthermore, the program must also have a function that checks whether a move is legal.
  This is the same principal as the problem I just mentioned. There can be no reverse moves
  in which balls drop into lower tubes -- balls can either remain where they are, or
  move on top of the adjacent tube. If balls were to drop in a reverse move, then there
  would be no way for a human to place the ball that just dropped back on top in a single move.


Pseudocode:

  - generate a list of moves
  - execute list of moves
    - if flip, then simply flip (see flip pseudocode below)
    - else, look ahead how many of the same moves are made (see look_ahead()) (a parameter required for PART II above)
      - call a function to check whether or not it is a legal move (see is_legal_move())
      - if not legal, skip over move
      - else
        - call function to find all filled tubes (see find_filled_tubes())
        - call a function to randomly select filled tubes (see find_random_filled_tubes())
        - call a function to find tubes where balls fell (see find_tube_where_balls_fell())
        - call rotate function (see pseudocode for rotate function)

  FUNCTIONS:

    flip()
      for i in range(6)
        length of entire tube = all elements > 0
        size_of_upper_tube = length of entire tube - (6-i) //note length of entire tube can be found
                                                                // by all elements > 0
                                                                // ALSO note 6-index = capacity of lower tube
        temporary_vector = all elements > 1 //note 1 = empty and 0 = nonexistent
        call NumPy function to reverse temporary_vector
        insert temporary_vector into puzzle in index (6-i)
        pad with 1's to length of entire tube

    is_legal_move()
      parameter: direction
      for i in range(6)
        if the next tube has less balls than capacity AND the current tube has more than its capacity, then illegal

    find_filled_tubes()
      for i in range(6)
        temp_vector = puzzle[i,:] where puzzle[i,:] > 1
        if temp_vector == 6-i //note again, 6-i is equal to the capacity of the lower tube
          then append to output array

    find_random_filled_tubes()
      simple take a random subset of the array returned in find_filled_tubes()

    find_tubes_where_balls_fell()
      parameter: the number of consecutive moves
      find subsets of array returned in find_random_filled_tubes where there are n consecutive tubes

    rotate():
      for i in range(6)

NOTE: I did not complete this project in it's entirety. I am very close, and I wish I had more time to complete it. I believe there is a single
bug that is preventing this from working.

My heuristic:
  - count the number of balls that are next to a ball of the same color.
  Argument:
    - As the puzzle is solved, I have noticed that after each step there are more balls that are adjacent to balls of the same color.
      I have no argument as to whether this heuristic is admissible. It appears to me that is makes sense that after each move, the number
      of balls of the same color next to each other would increase, but I have no concrete proof.

What I learned from this project:

  I learned what a heuristic is. I wish I could've completed this project sooner so that I would have had more time to
  come up with a heuristic that is truly admissible. 
