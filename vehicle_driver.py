# Copyright 1996-2023 Cyberbotics Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""vehicle_driver controller."""

import math, os, csv
from controller import Display, Keyboard, Camera
from vehicle import Driver

# variables globales
TIME_STEP = 50
SPEED = 5
MYDIR = "/Users/alexbautistaramos/Downloads/images"
angle = 0 # angulo de giro
steering_angle = 0 # angulo de las ruedas
manual_steering = 0 # angulo manual
step = 0
LEFT = 0
RIGHT = 0
IMAGE_SAVE_INTERVAL = 25

# creacion del vehiculo
driver = Driver()
driver.setSteeringAngle(0.2)
driver.setCruisingSpeed(SPEED)

# creacion de la camara
camera = driver.getDevice('camera')
camera.enable(TIME_STEP)
camera_width = camera.getWidth()
camera_height = camera.getHeight()
camera_fov = camera.getFov()
timestep = int(driver.getBasicTimeStep())

# folder para guardar las imagenes
image_folder = MYDIR
os.makedirs(image_folder, exist_ok=True)

# params para escribir el csv
csv_file = open(os.path.join(image_folder, "driving_log.csv"), mode='w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['filename', 'angle', 'speed', 'left', 'right'])

#txt_file = open(os.path.join(image_folder, "driving_log.txt"), mode='w')
#txt_file.write('filename, angle, speed, left, right\n')

# creacion del teclado
keyboard = Keyboard()
keyboard.enable(timestep)

# control velocidad
def set_speed(speed):
    global SPEED
    SPEED = speed
    driver.setCruisingSpeed(SPEED)
    
# angulo de las ruedas
def set_steering_angle(wheel_angle):
    global angle, steering_angle
    # Check limits of steering
    if (wheel_angle - steering_angle) > 0.1:
        wheel_angle = steering_angle + 0.1
    if (wheel_angle - steering_angle) < -0.1:
        wheel_angle = steering_angle - 0.1
    steering_angle = wheel_angle 
    
    # limit range of the steering angle
    if wheel_angle > 0.5:
        wheel_angle = 0.5
    elif wheel_angle < -0.5:
        wheel_angle = -0.5
    # update steering angle
    angle = wheel_angle
    print(angle)
    driver.setSteeringAngle(angle)

# angulo del volante
def change_steer_angle(inc):
    global manual_steering
    # Apply increment
    new_manual_steering = manual_steering + inc
    # valida el intervalo 
    if new_manual_steering <= 25.0 and new_manual_steering >= -25.0: 
        manual_steering = new_manual_steering
        # establece el angulo de las ruedas
        set_steering_angle(manual_steering * 0.01)
    # Debugging
    # if manual_steering == 0:
        # print("going straight")
    # else:
        # turn = "left" if steering_angle < 0 else "right"
        # print("turning {} rad {}".format(str(steering_angle),turn))

def save_image(step):
    #global angle 
    filename = os.path.join(image_folder, f"image_{step}.png")
    camera.saveImage(filename, 100)
    #print(filename, angle, SPEED, LEFT, RIGHT)
    csv_writer.writerow([filename, angle, SPEED, LEFT, RIGHT])
    # txt_file.write(f"{filename}, {angle}, {SPEED}, {LEFT}, {RIGHT}\n")


while driver.step() != -1:
    #angle, left, Right, Speed
    key = keyboard.getKey()
    if key == keyboard.UP:  # up
        set_speed(SPEED + 5.0)
        print("speed up to "+str(SPEED))
    elif key == keyboard.DOWN:  # down
        set_speed(SPEED - 5.0)
        print("speed down to "+str(SPEED))
    elif key == keyboard.RIGHT:  # right
        change_steer_angle(+0.5)
        RIGHT = 1
        LEFT = 0
        print("right")
    elif key == keyboard.LEFT:  # left
        change_steer_angle(-0.5)
        LEFT = 1
        RIGHT = 0
        print("left")
       
    if step % IMAGE_SAVE_INTERVAL == 0:
        save_image(step)    
    step += 1
    
#txt_file.close()
csv_file.close()