def reward_function(params):
    '''
    Example of penalize steering, which helps mitigate zig-zag behaviors
    '''

    # Read input parameters
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    steering = abs(params['steering_angle']) # Only need the absolute steering angle
    speed = params['speed']
    is_offtrack = params['is_offtrack']
    # Calculate 3 marks that are farther and father away from the center line
    center_reward = (0.5 - distance_from_center / track_width) * 2 + 0.1

    # Give higher reward if the car is closer to center line and vice versa
    if center_reward >= 0.1:
        reward = center_reward
    else:
        reward = 1e-3  # likely crashed/ close to off track

    if is_offtrack:
        reward = 1e-5

    return float(reward