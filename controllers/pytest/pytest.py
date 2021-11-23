from controller import Robot, Motor

#https://cyberbotics.com/doc/guide/epuck

TIME_STEP = 64
MAX_SPEED = 6.28

camera_w, camera_h = 640, 480

# create the Robot instance.
robot = Robot()

# get a handler to the motors and set target position to infinity (speed control)
leftMotor = robot.getDevice('left wheel motor')
rightMotor = robot.getDevice('right wheel motor')
cam = robot.getDevice('camera')

leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))

# set up the motor speeds at 10% of the MAX_SPEED.
leftMotor.setVelocity(0.1 * MAX_SPEED)
rightMotor.setVelocity(0.1 * MAX_SPEED)

distanceDsensors = [robot.getDevice('ps' + str(i)) for i in range(7)]
print(distanceDsensors)

cam.enable(1)
while robot.step(TIME_STEP) != -1:
   cam.getImage()
   pass