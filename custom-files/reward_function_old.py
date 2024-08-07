import math

def reward_function(params):
    # Read input variables
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']

    # Initialize the reward with typical value
    reward = 1.0
    
     # Read input parameters
    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    left_of_center = params['is_left_of_center']
    track_width = params['track_width']
    abs_steering = params['steering_angle']
    speed = params['speed']
    progress = params['progress']
    steps = params['steps']
    is_reversed = params['is_reversed'] #True for cw and false for ccw
    track_length = params['track_length']


    # Calculate the direction of the center line based on the closest waypoints
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]

    # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
    # Convert to degree
    track_direction = math.degrees(track_direction)

    # Calculate the difference between the track direction and the heading direction of the car
    direction_diff = abs(track_direction - heading)
    DIRECTION_THRESHOLD = 3.0

    left = [23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133]
    
    right = [61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,84,86,87,88]
    center =[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,55,56,57,58,59,60,89,90,91,92,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168]

    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width

    SPEED_THRESHOLD = 1.5
    SPEED_THRESHOLD_FOR_CENTER = 3.7
    MAX_WAYPOINT = 168

    ABS_STEERING_THRESHOLD = 22.5
    MAX_TIME_FOR_LAP = 16.0

    CENTER_LAP_POSITION_START= 0.14
    CENTER_LAP_POSITION_END = 0.82

    CURRENT_LAP_POSITION = next_point/MAX_WAYPOINT

    if not all_wheels_on_track:
        # Penalize if the car goes off track
        reward = 1e-3
    elif is_reversed:
        reward = 1e-3
    elif distance_from_center >= marker_3:
        reward = 1e-3
    else:
        if all_wheels_on_track and (0.5*track_width - distance_from_center ) >= 0.05 :
            #reward for being on track
            reward += 5.0
            if (distance_from_center <= marker_1):
                if(CURRENT_LAP_POSITION < CENTER_LAP_POSITION_START or CURRENT_LAP_POSITION > CENTER_LAP_POSITION_END):
                    if(speed >= SPEED_THRESHOLD_FOR_CENTER):
                        reward += 10.0
                else:
                    reward += 3.0
            elif(distance_from_center <= marker_2):
                reward += 1.0
            else:
                reward += 1e-3
        if (progress == 100):
            if (MAX_TIME_FOR_LAP > round(steps/15, 1)):
                reward += 2.5
        if direction_diff > 180:
            direction_diff = 360 - direction_diff
        # Penalize the reward if the difference is too large
        if direction_diff > DIRECTION_THRESHOLD:
            reward *= 0.5
        if abs_steering > ABS_STEERING_THRESHOLD:
            reward *= 0.5

    return float(reward)