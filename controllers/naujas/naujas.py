from controller import Robot, Motor
import struct

MAX_SPEED = 6.28 / 2

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

sideRule = 0 #0 - right, 1 - left

def getDistance(index):
    val = psarr[index].getValue()
    #print(index, val)
    return val


def setVelocity(left, right):
        leftWheel.setVelocity(left)
        rightWheel.setVelocity(right)

        
while robot.step(timestep) != -1:
    if receiver.getQueueLength() > 0:
        message = struct.unpack('i', receiver.getData())[0]
        if message not in checkpoints:
            print('adding checkpoint #', message)
            checkpoints.append(message)
        sideRule = message
        receiver.nextPacket()
        
    if sideRule % 2 == 0:
        if getDistance(0) > 100 or getDistance(7) > 100 or getDistance(1) > 250:
            setVelocity(0, MAX_SPEED)
        elif getDistance(2) < 150 and getDistance(1) < 80:
            setVelocity(MAX_SPEED, 0)
        elif getDistance(2) > 200:
            setVelocity(0, MAX_SPEED)
        else:
            setVelocity(MAX_SPEED, MAX_SPEED)
    else:
        if getDistance(0) > 100 or getDistance(7) > 100 or getDistance(6) > 250:
            setVelocity(MAX_SPEED, 0)
        elif getDistance(5) < 150 and getDistance(6) < 80:
            setVelocity(0, MAX_SPEED)
        elif getDistance(5) > 200:
            setVelocity(MAX_SPEED, 0)
        else:
            setVelocity(MAX_SPEED, MAX_SPEED)
        
setVelocity(0, 0)