import radio
import microbit
from random import randint

# definition of functions
def get_message():
    """Wait and return a message from another micro:bit.

    Returns
    -------
    message: message sent by another micro:bit (str) 
    """
    
    message = None    
    while message == None:
        microbit.sleep(250)
        message = radio.receive()
    
    return message


# Tuple of directions
directions = ('left', 'right', 'top', 'bottom', None) 





def move_submarines():
    """Move the submarines in the right direction while adhering to the micro:bit board limits."""

    for submarine in submarines:

        if submarine['direction'] == 'left' and submarine['position']['x'] > 0:
            submarine['position']['x'] -= 1

        elif submarine['direction'] == 'right' and submarine['position']['x'] < 4:
            submarine['position']['x'] += 1

        elif submarine['direction'] == 'top' and submarine['position']['y'] > 0:
            submarine['position']['y'] -= 1

        elif submarine['direction'] == 'bottom' and submarine['position']['y'] < 4:
            submarine['position']['y'] += 1
            




def update_submarines_direction():
    """Update the direction of the submarines after receiving a player action."""

    probability_satisfied = randint(0, 9) == 0

    for submarine in submarines:
        direction = submarine['direction']
        position = submarine['position']

        if (direction == 'left' and position['x'] == 0) or probability_satisfied:
            submarine['direction'] = directions[randint(0, 3)]

        elif (direction == 'right' and position['x'] == 4) or probability_satisfied:
            submarine['direction'] = directions[randint(0, 3)]

        elif (direction == 'top' and position['y'] == 0) or probability_satisfied:
            submarine['direction'] = directions[randint(0, 3)]

        elif (direction == 'bottom' and position['y'] == 4) or probability_satisfied:
            submarine['direction'] = directions[randint(0, 3)]





def intensity(current_life):
    """Get the intensity of the pixel where the submarine is situated
    
    Parameters
    ----------
    current_life: Represents the points of life for the submarine (int).

    Returns
    -------
    intensity: The intensity of the pixel where the submarine is situated (int)
    """
    life_percentage = current_life * 100 / submarine_life
    intensity = life_percentage * 9 / 100

    return int(intensity)




def show_submarines():
    """Display the current positions of submarines on the micro:bit board."""

    for submarine in submarines:
        microbit.display.set_pixel(submarine['position']['x'], submarine['position']['y'], intensity(submarine['life']))



def show_shoot_result(target_x, target_y):
    """Execute the shoot order and show if a submarine is touched or not
    
    Parameters
    ----------
    target_x: The X position of the shot pixel (int).
    target_y: The Y position of the shot pixel (int).

    """

    for submarine in submarines :
        if submarine["position"]["x"] == target_x and submarine["position"]["y"] == target_y and submarine['life'] > 0:
            submarine["life"] -= 1

            microbit.display.set_pixel(submarine["position"]["x"], submarine["position"]["y"], intensity(submarine['life']))
            microbit.sleep(180)
            microbit.display.clear()
            return

    # blink the pixel 3 times if there's no submarine in that pixel
    for signal in range(3):
        microbit.display.set_pixel(target_x, target_y, 9)
        microbit.sleep(180)
        microbit.display.set_pixel(target_x, target_y, 0)
        microbit.sleep(180)





def is_game_over():
    """Determine if the game is over
    
    Returns
    -------
    status: True if game is over, False otherwise (bool)
    """
    for submarin in submarines:
        if submarin['life'] > 0 :
            return False    
    return True

   
   
    

# settings
group_id = 25
nb_submarines = 4
submarine_life = 2



# setup radio to receive orders
radio.on()
radio.config(group=group_id)




# create board and place submarines
submarines = [{
        'position': {
            'x': randint(0, 4),
            'y': randint(0, 4)
        },
        'direction': directions[randint(0, 3)],
        'life': submarine_life
    } for submarine in range(nb_submarines)]






# loop until game is over
game_is_over = False

while not game_is_over:

	# wait until gamepad sends an order
    order = get_message()
    

    # execute order (fire or sonar)
    if(order == 'sonar'):
        show_submarines()
    elif('shoot' in order):
        action, loc_X, loc_Y = str(order).split('-')
        show_shoot_result(int(loc_X), int(loc_Y))

    
    # wait a few seconds and clear screen
    microbit.sleep(2500)
    microbit.display.clear()
    

    # check if game is not over
    game_is_over = is_game_over()
    
    if not game_is_over:
        # update position of submarines
        move_submarines()
        
        # update direction of submarines
        update_submarines_direction()


# tell that the game is over
microbit.display.scroll('YOU WON', delay=100)