import math

def reward_function(params):
    # Read input variables
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    positionX = params['x']
    positionY = params['y']

    # Initialize the reward with typical value
    reward = 1e-3
    
     # Read input parameters
    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    left_of_center = params['is_left_of_center']
    track_width = params['track_width']
    steering_angle = params['steering_angle']
    speed = params['speed']
    progress = params['progress']
    steps = params['steps']
    is_reversed = params['is_reversed'] #True for cw and false for ccw
    track_length = params['track_length']
    abs_steering = abs(steering_angle)


    # Calculate the direction of the center line based on the closest waypoints
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]

    # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
    # Convert to degree
    track_direction_degrees = math.degrees(track_direction)

    # Calculate the difference between the track direction and the heading direction of the car
    direction_diff = abs(track_direction_degrees - heading)

    SPEED_THRESHOLD_STRAIGHT = 3.5
    SPEED_THRESHOLD_MEDIUM_TURN_MIN = 2.0
    SPEED_THRESHOLD_MEDIUM_TURN_MAX = 3.0
    SPEED_THRESHOLD_WIDE_TURN_MIN = 1.5
    SPEED_THRESHOLD_WIDE_TURN_MAX = 2.0

    NUM_OF_ACTIONS = 6

    ABS_STRAIGHT_ANGLE = 5.0
    ABS_WIDE_TURN_ANGLE = 15.0

    if all_wheels_on_track and (0.5*track_width - distance_from_center ) >= 0.05 :
        #reward for being on track
        reward += 10.0

    #on the straight angles go a certain minimum speed
    if abs_steering < ABS_STRAIGHT_ANGLE:
        if speed > SPEED_THRESHOLD_STRAIGHT:
            reward += 2.0
    
    if abs_steering > ABS_STRAIGHT_ANGLE and abs_steering < ABS_WIDE_TURN_ANGLE:
        if speed < SPEED_THRESHOLD_MEDIUM_TURN_MIN:
            reward += 0.5
        elif speed < SPEED_THRESHOLD_MEDIUM_TURN_MAX:
            reward += 1.0
    
    #on turns, go a minimum speed
    if abs_steering > ABS_WIDE_TURN_ANGLE:
        if speed < SPEED_THRESHOLD_WIDE_TURN_MIN:
            reward += 1.0
        elif speed < SPEED_THRESHOLD_WIDE_TURN_MAX:
            reward += 0.5

    if direction_diff > 180:
        direction_diff = 360 - direction_diff
    # Give dynamic reward if following the heading angle
    HEADING_PENALTY = 1 - (direction_diff / 180.0)
    reward += 10.0*HEADING_PENALTY

    # steering reward 
    # calculate reward for car steering in the same direction as the track heading
    steering_heading = abs(steering_angle - direction_diff)/180.0
    STEERING_PENALTY = 1 - steering_heading
    reward += 10.0*STEERING_PENALTY

    #penalty section
    if is_reversed:
        reward = 1e-3

    if not all_wheels_on_track:
        reward = 1e-3

    return float(reward)