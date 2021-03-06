"""
Demo the trick flying for the python interface

Author: Amy McGovern
"""

from pyparrot.Minidrone import Mambo
import numpy as np
import git
import os

def GitPull(repo_name):
    repo = git.Repo(repo_name)
    o = repo.remotes.origin
    o.pull()

def GitPush():
    try:
        repo = git.Repo(repo_dir)
        repo.git.add('--all')
        repo.index.commit(commit_message)
        origin = repo.remote(name='origin')
        origin.push()
    except:
        print('error pushing')
    finally:
        print('done push!')
    
# If you are using BLE: you will need to change this to the address of YOUR mambo
# if you are using Wifi, this can be ignored
mamboAddr = "e0:14:fb:1a:3d:c6"

# make my mambo object
# remember to set True/False for the wifi depending on if you are using the wifi or the BLE to connect
mambo = Mambo(mamboAddr, use_wifi=False)

init_x = 0
init_y = 0

repo_dir = '/home/pi/MediDrone/MediDrone'


GitPull(repo_dir)

print("trying to connect")
success = mambo.connect(num_retries=3)
print("connected: %s" % success)

drone_to_fly = False
    
while not drone_to_fly:
     #mambo.smart_sleep(0.1)
    if os.path.isfile("drone_init.txt"):
        file = open('drone_init.txt', 'r')
        lines = file.readlines()
        file.close()
        line_num = 0
        for line in lines:
            line = line.strip()
            if line_num == 0:
                final_x = line
            else:
                final_y = line
            line_num += 1
        drone_to_fly = True
    GitPull('/home/pi/MediDrone/MediDrone')

final_x = 0
final_y = 100
print(final_x)
print(final_y)


if (success):
    
    #setting vertical speeds
    mambo.set_max_vertical_speed(0.05)
    
    #picking up care pack
    mambo.close_claw()
    
    #get final x and y
    rotate_angle = 0.0
    
    
    #getting rotation angle
    if final_x == 0:
        if final_y < 0:
            rotate_angle = 180
    else:
        rotate_angle = np.tan(np.abs(final_y)/np.abs(final_x))
        if final_y < 0:
            rotate_angle = 180 - rotate_angle
        if final_x < 0:
            rotate_angle *= -1
    rotate_angle *= 100
    rotate_angle = int(rotate_angle)
    print('rotate angle is: ' + str(rotate_angle))
    
            
    #setting drone speed
    tilt = 12
    drone_speed = 20

    
    #take-off
    print("taking off!")
    mambo.takeoff()
    
    mambo.smart_sleep(2)
    
    #rotate to face corrent position
    mambo.turn_degrees(rotate_angle - 5)
    
    #get distance that needs to be travelled
    straight_dist = np.sqrt(final_x**2 + final_y**2)
    print('distance is: ' + str(straight_dist))
    current_dist = 0
    
    # getting to the location required
    print('getting to location')
    while(current_dist <= straight_dist):
        mambo.fly_direct(roll=0, pitch=tilt, yaw=0, vertical_movement=0, duration=0.5)
        current_dist += drone_speed
        
    #stabilizing
    mambo.smart_sleep(2)
    #mambo.fly_direct(roll=0, pitch=0, yaw=0,vertical_movement=0)
    #mambo.smart_sleep(2)
    
    #dropping care pack
    mambo.open_claw()
    
    mambo.smart_sleep(2)
    mambo.turn_degrees(-170)
    mambo.smart_sleep(2)
    
    #moving back to original pos
    while(current_dist > 0):
        mambo.fly_direct(roll=0, pitch=tilt, yaw=0, vertical_movement=0, duration=0.5)
        current_dist -= drone_speed
    
    #landing in correct location
    print("landing")
    print("flying state is %s" % mambo.sensors.flying_state)
    mambo.safe_land(5)
    mambo.smart_sleep(2)

    os.remove('drone_init.txt')
    GitPush()
    print("disconnect")
    mambo.disconnect()
