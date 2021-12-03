from controller import Robot, Motor
import struct

MAX_SPEED = 6.28 / 2

# Roboto iniciavimas
robot = Robot()

timestep = int(robot.getBasicTimeStep())
leftWheel = robot.getDevice('left wheel motor')
rightWheel = robot.getDevice('right wheel motor')
leftWheel.setPosition(float('inf'))
rightWheel.setPosition(float('inf'))

# Imtuvo konfiguracija
receiver = robot.getDevice('receiver')
receiver.enable(timestep)
receiver.setChannel(1)

# Artumo sensoriu konfiguracija
psarr = [robot.getDevice('ps' + str(i)) for i in range(8)]
[ps.enable(timestep) for ps in psarr]

sideRule = 0 #0 - right, 1 - left

# Atstumo gavimo funkcija
def getDistance(index):
    val = psarr[index].getValue()
    return val


# Varomuju ratu greicio nustatymo funkcija
def setVelocity(left, right):
        leftWheel.setVelocity(left)
        rightWheel.setVelocity(right)


# Roboto veikimo algoritmas
while robot.step(timestep) != -1:
    # Zinutes apdorojimas, jeigu ji gauta
    if receiver.getQueueLength() > 0:
        message = struct.unpack('i', receiver.getData())[0]
        sideRule = message
        receiver.nextPacket()
    
    # Jeigu siena sekama is desines
    if sideRule == 0:
        # Tikrinami priekineje dalyje esantys sensoriai
        if getDistance(0) > 100 or getDistance(7) > 100 or getDistance(1) > 250:
            setVelocity(0, MAX_SPEED)
        # Tikrinami soniniai sensoriai
        elif getDistance(2) < 150 and getDistance(1) < 80:
            setVelocity(MAX_SPEED, 0)
        # Tikrinamas soninis sensorius
        elif getDistance(2) > 200:
            setVelocity(0, MAX_SPEED)
        # Vaziuojama tiesiai
        else:
            setVelocity(MAX_SPEED, MAX_SPEED)
    # Jeigu siena sekama is kaires
    elif sideRule == 1:
        # Tikrinami priekineje dalyje esantys sensoriai
        if getDistance(0) > 100 or getDistance(7) > 100 or getDistance(6) > 250:
            setVelocity(MAX_SPEED, 0)
        # Tikrinami soniniai sensoriai
        elif getDistance(5) < 150 and getDistance(6) < 80:
            setVelocity(0, MAX_SPEED)
        # Tikrinamas soninis sensorius
        elif getDistance(5) > 200:
            setVelocity(MAX_SPEED, 0)
        # Vaziuojama tiesiai
        else:
            setVelocity(MAX_SPEED, MAX_SPEED)
    # Jeigu radome isejima
    else:
        break
        
setVelocity(0, 0)