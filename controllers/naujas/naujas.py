from controller import Robot, Motor

MAX_SPEED = 6.28

# Get pointer to the robot.
robot = Robot()

# Get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

# Get pointer to the robot wheels motors.
leftWheel = robot.getDevice('left wheel motor')
rightWheel = robot.getDevice('right wheel motor')

# We will use the velocity parameter of the wheels, so we need to
# set the target position to infinity.
leftWheel.setPosition(float('inf'))
rightWheel.setPosition(float('inf'))

psarr = [robot.getDevice('ps' + str(i)) for i in range(8)]
[ps.enable(timestep) for ps in psarr]

def getDistance(index):
    val = psarr[index].getValue()
    print(index, val)
    return val


leftWheel.setVelocity(MAX_SPEED)
rightWheel.setVelocity(MAX_SPEED)
while robot.step(timestep) != -1:
    if getDistance(2) < 90:
        break
        
leftWheel.setVelocity(MAX_SPEED)
rightWheel.setVelocity(-MAX_SPEED)
while robot.step(timestep) != -1:
    if getDistance(1) > 90:
        break
        
while robot.step(timestep) != -1:
    if getDistance(0) > 250 or getDistance(7) > 250:
        leftWheel.setVelocity(MAX_SPEED - (MAX_SPEED / 100 * ((getDistance(0) + getDistance(7)) / 2)))
        rightWheel.setVelocity(MAX_SPEED)
    elif getDistance(0) < 100 and getDistance(1) < 100:
        leftWheel.setVelocity(MAX_SPEED)
        rightWheel.setVelocity(MAX_SPEED - (MAX_SPEED / 100 * getDistance(0)))
    elif getDistance(2) > 500:
        leftWheel.setVelocity(MAX_SPEED - (MAX_SPEED / 100 * getDistance(2)))
        rightWheel.setVelocity(MAX_SPEED)
    else:
        leftWheel.setVelocity(MAX_SPEED)
        rightWheel.setVelocity(MAX_SPEED)
        
leftWheel.setVelocity(0)
rightWheel.setVelocity(0)