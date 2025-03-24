import cv2
import chess
import numpy as np
import math

# Setting chessboard grid dimension
grid_dimension = (8,2)
# Setting HSV lower and upper bound ranges
lower_green = (25, 50, 90)
higher_green = (80, 255, 255)

black = (0, 0, 0)
white = (255, 255, 255)
blue = (82, 113, 255)
green = (0, 191, 99)
red = (255, 49, 49)
pink = (255, 102, 196)
orange = (255, 145, 77)
yellow = (255, 222, 89)

def get_hue(rgb_color):
    rgb_array = np.uint8([[list(rgb_color)]])
    hsv_array = cv2.cvtColor(rgb_array, cv2.COLOR_RGB2HSV)
    hsv_color = tuple(hsv_array[0][0])
    return hsv_color[0]

hues = (
    (get_hue(blue), 'p'),
    (get_hue(green), 'b'),
    (get_hue(red), 'k'),
    (get_hue(pink), 'n'),
    (get_hue(orange), 'q'),
    (get_hue(yellow), 'r')
)

def get_piece(image, circle):
    x, y, r = (int(a) for a in circle)
    piece_type_color = image[y+r-3][x]
    #print(y+r-3, x)
    #print(piece_type_color)
    piece_type_hue = piece_type_color[0]
    closest_type = 'p'
    closest_dist = float('inf')
    for hue, piece_type in hues:
        dist = piece_type_hue - hue
        if dist < closest_dist:
            closest_dist = dist
            closest_type = piece_type
    piece_center_color = image[y][x]
    piece_center_val = piece_center_color[2]
    if piece_center_val > 128:
        closest_type = closest_type.upper()
    return closest_type

# Experiment with thresholds once we have real pictures
# Saturation of lower bound might need to be increased
color_threshold_lower = (0, 10, 0)
color_threshold_upper= (255, 255, 255)

# TODO: Create the color ranges for each chess piece

while True:
    user_input = input("Please Enter to take source picture: ")

    # break the loop
    if user_input == 'q':
        break
    # load the image
    image = cv2.imread("/home/pi/robot_arm/images/chess_game_sequence/eight_colors/start_position.png")
    # break the loop if no image is found or loaded
    if image is None:
        print("Error: Image not found or could not be loaded")
        break

    # convert the image to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # isolate the pixels based on the lower and upper bounds
    mask_green = cv2.inRange(hsv, color_threshold_lower, color_threshold_upper)
    # Green pixels = True, Not green = False
    imask_green = mask_green>0
    # Create new image setting everything that is not green white
    green = np.full(image.shape, (255, 255, 255), dtype=np.uint8)
    # Setting everything green to black
    green[imask_green] = (0, 0, 0)

    # blur the images, used for for live image capture
    blurred = cv2.GaussianBlur(green, (9,9), 2)
    
    cv2.imwrite('image.png', green)

    # display images
    # cv2.imshow('image.jpg', image)
    # cv2.imshow('green.jpg', green)
    # cv2.imshow('blurred.jpg', blurred)
    
    '''
    # detect grid pattern
    ret, corners = cv2.findCirclesGrid(
        green, 
        grid_dimension,
        flags=cv2.CALIB_CB_SYMMETRIC_GRID + cv2.CALIB_CB_CLUSTERING
    )
    
    print(ret, corners)
    '''
    gray = cv2.cvtColor(green, cv2.COLOR_BGR2GRAY)
    
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=20, param2=10, minRadius=15, maxRadius=30)
    
    #print(circles)
    
    if circles is not None:
        circles = np.uint16(np.around(circles))
        circles = sorted(circles[0], key=lambda t: (t[0], t[1]))
        pieces = {}
        for i in circles:
            piece = get_piece(hsv, i)
            pieces[piece] = pieces.get(piece, 0) + 1
            cv2.circle(green, (i[0], i[1]), i[2], (0, 255, 0), 2)
        print(pieces)
        
        cv2.imshow('Detected Circles', green)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    chess_grid = [['r','n','b','q','k','b','n','r']
    ['p' * 8]
    ['x' * 8]
    ['x' * 8]
    ['x' * 8]
    ['x' * 8]
    ['P' * 8]
    ['R','N','B','Q','K','B','N','R']]
    
    
    
    '''
    # if a grid pattern is detected
    if ret:
        # draw the corners onto the image
        img = cv2.drawChessboardCorners(image, grid_dimension, corners, ret)
        # reshape the corners array
        corners = corners.reshape((*grid_dimension, 2))
        # print the locations of each corner row by row
        # for row in corners:
        #     for x, y in row:
        #         print(x,y,end=",  ")
        #     print()

        # cv2.imshow('board', img)
        # create a chessboard array of False values
        squares_filled = np.full(corners.shape[:2], False)

        while input("Press Enter ('c' to take new source image):") != 'c':
            # covered_image = picam2.capture_array()
            new_image = cv2.imread("/home/pi/robot_arm/images/chess_game_sequence/eight_colors/")
            hsv_pixels = cv2.cvtColor(np.array([[new_image[int(x)][7 - int(y)] for y, x in row] for row in corners]), 
                                      cv2.COLOR_BGR2HSV)
            mask_green = cv2.inRange(hsv_pixels, lower_green, higher_green)
            mask_green = np.flipud(mask_green)
            print(mask_green)

        occupied_squares = []
        unoccupied_squares = []

        for y in range(mask_green.shape[0]):
            for x in range(mask_green.shape[1]):
                column = chr(ord('a') + x)
                row = str(8 - y)
                square = column + row
                if mask_green[y, x] == 0:
                    occupied_squares.append(square)
                else:
                    unoccupied_squares.append(square)

        print(occupied_squares)
        print(unoccupied_squares)
    '''

cv2.destroyAllWindows()
