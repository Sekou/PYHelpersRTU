#2026, S. Diane, example of iiwa-manipulator control
import math, time, os, numpy as np
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

print('Program started')
client = RemoteAPIClient()
sim = client.getObject('sim')
# Run a simulation in synchronous mode:
client.setStepping(True)
sim.startSimulation(), print('sim.start')

def move_to_config(handles,max_vel,max_accel,max_jerk,target_conf):
    params = { "joints" : handles, "targetPos" : target_conf, "maxVel" : max_vel,
        "maxAccel" : max_accel, "maxJerk" : max_jerk }
    sim.moveToConfig(params)

# идентификаторы звеньев робота
joint_handles=[sim.getObject('/LBRiiwa7R800/joint', {"index":i}) for i in range(7)]
print(joint_handles)

kPI=math.pi/180

vel, accel, jerk=180, 40, 80
max_vel=[vel*kPI]*7
max_accel=[accel*kPI]*7
max_jerk=[jerk*kPI]*7

phase=0
while (t := sim.getSimulationTime()) < 30:
    print(f"t={t:.2f}")
    if t>1 and phase==0:
        # 1
        target_pos1 = [90 * kPI, 90 * kPI, 170 * kPI, -90 * kPI, 90 * kPI, 90 * kPI, 0]
        move_to_config(joint_handles, max_vel, max_accel, max_jerk, target_pos1)
        phase+=1
    if t>5 and phase==1:
        # 2
        target_pos2 = [-90 * kPI, 90 * kPI, 180 * kPI, -90 * kPI, 90 * kPI, 90 * kPI, 0]
        move_to_config(joint_handles, max_vel, max_accel, max_jerk, target_pos2)
        phase+=1
    if t>10 and phase==2:
        # 3
        target_pos3 = [0, 0, 0, 0, 0, 0, 0]
        move_to_config(joint_handles, max_vel, max_accel, max_jerk, target_pos3)
        phase+=1

    angs=[sim.getJointPosition(h) for h in joint_handles]
    print( [f"{float(a):.3f}" for a in angs] )
    sim.step()

#stop
sim.stopSimulation(), print('Program ended')
