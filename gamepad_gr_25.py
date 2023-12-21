import radio
from microbit import *

#This code was created in 2023 by Yassir Chennaoui and Jugharta Gaci---
# definition of functions

def aim(loc_X, loc_Y):
    if accelerometer.get_y() > 300 and loc_Y < 4:
        loc_Y += 1
    elif accelerometer.get_y() < -300 and loc_Y > 0:
        loc_Y -= 1

    if accelerometer.get_x() < -300 and loc_X > 0:
        loc_X -= 1
    elif accelerometer.get_x() > 300 and loc_X < 4:
        loc_X += 1

    display.clear()
    display.set_pixel(loc_X, loc_Y, 9)

    return loc_X, loc_Y




def shoot(loc_X, loc_Y):
    radio.send('shoot-' + str(loc_X) + '-' + str(loc_Y))



def use_sonar():
    radio.send('sonar')
   

# settings
group_id = 25
target_x = 2
target_y = 2



# setup radio to send orders
radio.on()
radio.config(group=group_id)


# show where target is right now
display.set_pixel(target_x, target_y, 9)



# loop forever (until micro:bit is switched off)
while True:
    # check if a button is pressed, the micro:bit is moved, etc.
    loc_X, loc_Y = aim(target_x, target_y)

    if button_b.was_pressed():
        use_sonar()

    if button_a.was_pressed():
        shoot(loc_X, loc_Y)


    # wait a few milliseconds before checking again
    sleep(500)
         
    target_x = loc_X 
    target_y = loc_Y 
