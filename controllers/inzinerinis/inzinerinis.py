"""Sample Webots controller for the wall following benchmark."""

from controller import Robot, Motor


def getDistance(sensor):
    """
    Return the distance of an obstacle for a sensor.

    The value returned by the getValue() method of the distance sensors
    corresponds to a physical value (here we have a sonar, so it is the
    strength of the sonar ray). This function makes a conversion to a
    distance value in meters.
    """
    r = ((100 - sensor.getValue()) / 100) * 3
    print(r)
    return r


# Maximum speed for the velocity value of the wheels.
# Don't change this value.
MAX_SPEED = 5.24

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

# Get and enable the distance sensors.
sensor0 = robot.getDevice("ps6")
sensor0.enable(timestep)
sensor1 = robot.getDevice("ps7")
sensor1.enable(timestep)
sensor2 = robot.getDevice("ps0")
sensor2.enable(timestep)
sensor3 = robot.getDevice("ps1")
sensor3.enable(timestep)
sensor4 = robot.getDevice("ps4")
sensor4.enable(timestep)

sensor15 = robot.getDevice("ps5")
sensor15.enable(timestep)

# Move forward until we are 50 cm away from the wall.
leftWheel.setVelocity(MAX_SPEED)
rightWheel.setVelocity(MAX_SPEED)
while robot.step(timestep) != -1:
    if getDistance(sensor3) < 0.5:
        break

# Rotate clockwise until the wall is to our left.
leftWheel.setVelocity(MAX_SPEED)
rightWheel.setVelocity(-MAX_SPEED)
while robot.step(timestep) != -1:
    # Rotate until there is a wall to our left, and nothing in front of us.
    if getDistance(sensor0) < 1:
        break

# Main loop.
while robot.step(timestep) != -1:
    if getDistance(sensor0) < 0.15 or getDistance(sensor15) < 0.15 or getDistance(sensor1) < 0.15 or (getDistance(sensor2) < 0.15) or (getDistance(sensor3) < 0.15) or (getDistance(sensor4) < 0.15):
        if (getDistance(sensor0) < 0.15):
            leftWheel.setVelocity(MAX_SPEED)
            rightWheel.setVelocity(MAX_SPEED - (1 - getDistance(sensor0)) * 7)
        elif (getDistance(sensor1) < 0.15):
            leftWheel.setVelocity(MAX_SPEED)
            rightWheel.setVelocity(MAX_SPEED - (1 - getDistance(sensor1)) * 7)
        elif (getDistance(sensor2) < 0.15):
            leftWheel.setVelocity(MAX_SPEED)
            rightWheel.setVelocity(MAX_SPEED - (1 - getDistance(sensor2)) * 7)
        elif (getDistance(sensor3) < 0.15):
            leftWheel.setVelocity(MAX_SPEED)
            rightWheel.setVelocity(MAX_SPEED - (1 - getDistance(sensor3)) * 7)
        elif (getDistance(sensor4) < 0.15):
            leftWheel.setVelocity(MAX_SPEED)
            rightWheel.setVelocity(MAX_SPEED - (1 - getDistance(sensor4)) * 7)
        elif (getDistance(sensor15) < 0.15):
            leftWheel.setVelocity(MAX_SPEED)
            rightWheel.setVelocity(MAX_SPEED - (1 - getDistance(sensor15)) * 7)
        # Too far from the wall, we need to turn left.
    elif ((getDistance(sensor0) / 2 + getDistance(sensor15) / 2) > 0.18):
        leftWheel.setVelocity(MAX_SPEED * 0.6)
        rightWheel.setVelocity(MAX_SPEED)
    # We are in the right direction.
    else:
        leftWheel.setVelocity(MAX_SPEED)
        rightWheel.setVelocity(MAX_SPEED)

# Stop the robot when we are done.
leftWheel.setVelocity(0)
rightWheel.setVelocity(0)