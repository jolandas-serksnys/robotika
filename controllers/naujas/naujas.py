from controller import Robot, Motor
import struct

MAX_SPEED = 6.28

# Get pointer to the robot.
robot = Robot()
checkpoints = []

# Get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

receiver = robot.getDevice('receiver')
receiver.enable(timestep)
receiver.setChannel(1)

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
    #print(index, val)
    return val

def setVelocity(left, right):
    if left >= 0 and left <= MAX_SPEED and right >= 0 and right <= MAX_SPEED:
        leftWheel.setVelocity(left)
        rightWheel.setVelocity(right)
    else:
        if left < 0:
            leftWheel.setVelocity(0)
        if right < 0:
            rightWheel.setVelocity(0)
        if left > MAX_SPEED:
            leftWheel.setVelocity(MAX_SPEED)
        if right > MAX_SPEED:
            rightWheel.setVelocity(MAX_SPEED)

setVelocity(MAX_SPEED, MAX_SPEED)
while robot.step(timestep) != -1:
    if getDistance(2) < 90:
        break
        
setVelocity(MAX_SPEED, 0)
while robot.step(timestep) != -1:
    if getDistance(1) > 90:
        break
        
while robot.step(timestep) != -1:
    if receiver.getQueueLength() > 0:
        message = struct.unpack('i', receiver.getData())
        if message not in checkpoints:
            print('adding checkpoint #', message)
            checkpoints.append(message)
        #print(message)
        receiver.nextPacket()

    if getDistance(0) > 100 or getDistance(7) > 100:
        setVelocity(MAX_SPEED - (MAX_SPEED / 75 * ((getDistance(0) + getDistance(7)) / 2)), MAX_SPEED)
    elif getDistance(2) > 400 or getDistance(1) > 400:
        setVelocity(MAX_SPEED - (MAX_SPEED / 75 * getDistance(2)), MAX_SPEED)
    elif getDistance(0) < 100 and getDistance(1) < 100:
        setVelocity(MAX_SPEED, MAX_SPEED - (MAX_SPEED / 100 * getDistance(0)))
    else:
        setVelocity(MAX_SPEED, MAX_SPEED)
        
setVelocity(0, 0)