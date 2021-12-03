from controller import Robot
import struct

# Roboto iniciavimas
robot = Robot()
timestep = int(robot.getBasicTimeStep())

# Siustuvo konfiguracija
emitter = robot.getDevice('emitter')
emitter.setChannel(1)
emitter.setRange(0.05)

# Nuolatinis pranesimo siuntimas
while robot.step(timestep) != -1:
    # Krypties paemimas is "custom data" parametro
    cpi = int(robot.getCustomData())
    # Zinutes issiuntimas
    emitter.send(struct.pack('i', cpi))