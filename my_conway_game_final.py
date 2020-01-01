import getopt
import sys

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

# the start function
def conway_runner(size, duration, conway_type):
    
    '''
    :param size: game size
    :param duration: renew time
    :param conway_type: mode
    '''
    
    game_board = np.array([]) # start with an array type
    if conway_type == '1': # type1 glider
        
        game_board = np.zeros(size * size).reshape(size, size) # initiate all the blanks
        
        fly_plane_generater(1, 1, game_board) # give some value from the beginning
        
    elif conway_type == '2': # type2 launcher
       
        game_board = np.zeros(size * size).reshape(size, size) 
        
        launcher_generater(20, 20, game_board)
    else:
        
        game_board = grid_generater(size) # type0 random type position

    # create a figure and axes。
    figure, axes = plt.subplots()
    # show an image, which include a plot in a 2-dimentional frame.
    display_images = axes.imshow(game_board, interpolation='nearest')
    # through call this *FuncAnimation* again and again
    display_dynamic = animation.FuncAnimation(figure, refresh_board, fargs=(display_images, game_board, size,),
                                              frames=15,
                                              interval=duration,
                                              save_count=50)
    # show the animation
    plt.show()


# refresh_board
def refresh_board(grid_sizes, display_images, game_board, size):
    # make a copy at first, in case data lost
    copy_game_board = game_board.copy()

    for i in range(size):    # judge all the surroundings how many elements live ?
        for j in range(size):
            # y轴
            y_axes_life = game_board[i, (j - 1) % size] + game_board[i, (j + 1) % size]
            # x轴
            x_axes_life = game_board[(i - 1) % size, j] + game_board[(i + 1) % size, j]
            # 右上下
            right_axes_life = game_board[(i - 1) % size, (j - 1) % size] + game_board[(i - 1) % size, (j + 1) % size]
            #左上下
            left_axes_life = game_board[(i + 1) % size, (j - 1) % size] + game_board[(i + 1) % size, (j + 1) % size]
            # divide 255 pixel, calculate total number 
            all_lives = int((y_axes_life + x_axes_life + right_axes_life + left_axes_life) / 255)

            # game rules 
            # any elements whose total neighbors are less than 2 will die for sparse population
            # any elements whose total neighbors are more than 3 will die for crowded population
            # any elements whose total neighbors equal 2 or 3 will survive 
            # any one who already died will revive if they have more than 3 neighbors
            # we keep the definition of conway game, the basic rules if we changed, the figure no good 
            
            if game_board[i, j] == 255: # condition judgement
                if (all_lives < 2) or (all_lives > 3):
                    copy_game_board[i, j] = 0
            else:

                if all_lives == 3:
                    copy_game_board[i, j] = 255
    display_images.set_data(copy_game_board)
    game_board[:] = copy_game_board[:]  #renew data 
    return display_images,

# random mode: create a zone with white and black dots, using certain probability
def grid_generater(size):
    ranges = [255, 0]
    return np.random.choice(ranges, size * size, p=[0.2, 0.8]).reshape(size, size)

# glider mode: 3 blanks needed be changed
def fly_plane_generater(i, j, game_board):
    fly_location = np.array([[0, 0, 255], [255, 0, 255], [0, 255, 255]])
    game_board[i:i + 3, j:j + 3] = fly_location

# launcher mode 
def launcher_generater(i, j, grid):
    gererater_new_board = np.zeros(12 * 39).reshape(12, 39) # we need an initiative launching platform matrix inside
    # some rows who have single elements will change one time, others will change accordingly 
    launcher_location = [[[5, 1], [5, 2]],
                         [[6, 1], [6, 2]],
                         [[3, 13], [3, 14]],
                         [[4, 12], [4, 16]],
                         [[5, 11], [5, 17]],
                         [[6, 11], [6, 15], [6, 17], [6, 18]],
                         [[7, 11], [7, 17]],
                         [[8, 12], [8, 16]],
                         [[9, 13], [9, 14]],
                         [[1, 25]],
                         [[2, 23], [2, 25]],
                         [[3, 21], [3, 22]],
                         [[4, 21], [4, 22]],
                         [[5, 21], [5, 22]],
                         [[6, 23], [6, 25]],
                         [[7, 25]],
                         [[3, 35], [3, 36]],
                         [[4, 35], [4, 36]]
                         ]
    for per in launcher_location:  # this means, if the row has 1 element, it only needs change itself
        if len(per) == 1:  
            gererater_new_board[per[0][0]][per[0][1]] = 255
        else:
            gererater_new_board[per[0][0]][per[0][1]] = 255  # change accordingly
            for i in range(1, len(per)):
                gererater_new_board[per[i][0]][per[i][1]] = gererater_new_board[per[0][0]][per[0][1]]
    grid[i:i + 12, j:j + 39] = gererater_new_board  #renew the result


if __name__ == '__main__':
    # we need use opts to get all inputs 
    argv = sys.argv[1:]
    try: 
        opts, args = getopt.getopt(argv, "hs:d:c:", ["size=", "duration=", "conway-type="])
    except getopt.GetoptError:
        print("xxx.py -s <size> -d <duration> -c <conway-type=>")
        sys.exit(-1)
    size = 100
    duration_time = 50
    conway_type = '0'
    for opt, arg in opts:
        if opt == '-h':
            print("xxx.py -s <size> -d <duration> -c <conway-type=>")
            break
        elif opt in ("-s", "size"):
            size = int(arg)
        elif opt in ("-d", "duration"):
            duration_time = float(arg)
        elif opt in ("-c", "conway-type"):
            conway_type = arg
        else:
            print("xxx.py -s <size> -d <duration> -c <conway-type=>")
    conway_runner(size, duration_time, conway_type)
