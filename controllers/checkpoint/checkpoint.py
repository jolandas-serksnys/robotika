from controller import Robot
import struct

robot = Robot()
timestep = int(robot.getBasicTimeStep())

emitter = robot.getDevice('emitter')
emitter.setChannel(1)
emitter.setRange(0.05)

while robot.step(timestep) != -1:
    cpi = int(robot.getCustomData())
    emitter.send(struct.pack('i', cpi))