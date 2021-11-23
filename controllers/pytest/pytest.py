from controller import Robot, Motor
import math
#https://cyberbotics.com/doc/guide/epuck
#https://cyberbotics.com/doc/reference/robot?tab-language=python
#https://github.com/haoransh/Maze-Robot-on-Webots/blob/master/controllers/maze_controller/maze_controller.c

TIME_STEP = 64
DEFAULT_SPEED = 6.28 * .1
WALL_THRESHOLD = 0.02
THRESHOLD = 0.0125

camera_w, camera_h = 640, 480

# create the Robot instance.
robot = Robot()

# get a handler to the motors and set target position to infinity (speed control)
leftMotor = robot.getDevice('left wheel motor')
rightMotor = robot.getDevice('right wheel motor')

cam = robot.getDevice('camera')
cam.enable(1)

leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))

# set up the motor speeds at 10% of the MAX_SPEED.
leftMotor.setVelocity(DEFAULT_SPEED)
rightMotor.setVelocity(DEFAULT_SPEED)

disLeft = 0.0
disRight = 0.0
disForward = 0.0
    
ps = [robot.getDevice('ps' + str(i)) for i in range(8)]
for i in ps:
    i.enable(1)
psValues = [psi.getValue() for psi in ps]

def leftWall():
    global disLeft
    curLeft = psValues[5]
    diff = math.fabs(curLeft - disLeft)
    disLeft = curLeft
    
    return diff > THRESHOLD
    
def rightWall():  
    global disRight
    curRight = psValues[2]
    diff = math.fabs(curRight - disRight)
    disRight = curRight
    
    return diff > THRESHOLD  
    
def forwardWall():  
    global disForward
    curForward = (psValues[0] + psValues[7])/2
    diff = math.fabs(curForward - disForward)
    disForward = curForward
    
    return diff > THRESHOLD  
    
def wallChanged():
    return leftWall() or rightWall() or forwardWall()
    
def biasBack():
    pass
    

def reachable():
    leftFree = psValues[5] < WALL_THRESHOLD
    rightFree = psValues[2] < WALL_THRESHOLD
    forwardFree = psValues[0] < WALL_THRESHOLD and psValues[7] < WALL_THRESHOLD
    
    return leftFree << 2 | forwardFree << 1 | rightFree

def turnLeft():
    leftMotor.setVelocity(-DEFAULT_SPEED)
    rightMotor.setVelocity(DEFAULT_SPEED)
    
    for i in range(55):
        robot.step(TIME_STEP)
        
    leftMotor.setVelocity(0)
    rightMotor.setVelocity(0)
    
def turnRight():
    leftMotor.setVelocity(DEFAULT_SPEED)
    rightMotor.setVelocity(-DEFAULT_SPEED)
    
    for i in range(55):
        robot.step(TIME_STEP)
        
    leftMotor.setVelocity(0)
    rightMotor.setVelocity(0)
    
def turnWhich():
    if not reachable() >> 2:
        if reachable == 0:
            turnRight()
            turnRight()
        if reachable() == 1:
            turnRight()
        else:
            return
    else:
        turnLeft()
        leftMotor.setVelocity(DEFAULT_SPEED)
        rightMotor.setVelocity(DEFAULT_SPEED)
        
        for i in range(65):
            robot.step(TIME_STEP)
            
        psValue[5] = ps[5].getValue()
        
        if psValue[5] < WALL_THRESHOLD:
            print('No access\n')
            turnLeft()
        
            for i in range(80):
                robot.step(TIME_STEP)
       
def main():        
    psValues = [psi.getValue() for psi in ps]
    
    while True:
        delay = robot.step(TIME_STEP)
        if delay == -1:
            break
            
        psValues = [psi.getValue() for psi in ps]
        
        if wallChanged():
            turnWhich()
        else:
            biasBack()
            
        leftMotor.setVelocity(DEFAULT_SPEED)
        rightMotor.setVelocity(DEFAULT_SPEED)
    
main()
#while robot.step(TIME_STEP) != -1:
#    cam.getImage()
#    pass
