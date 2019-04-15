#!/usr/bin/python3
"""Connect to a Meca500 robot, activate and home it,
send a small program and then close the connection.

Usage:
    python RobotSampleProgram.py
"""
import time
import sys

ROBOT_IP = "192.168.0.100"   # IP of the robot
ROBOT_PORT = 10000           # Communication port

robot = MecaRobot(ROBOT_IP, ROBOT_PORT)
print("Running program main_program...")
sys.stdout.flush()
# Set parameters
robot.run('SetCartAngVel', [80])
robot.run('SetCartLinVel', [100])
robot.run('SetJointVel', [10])
robot.run('SetCartAcc', [10])
robot.run('SetJointAcc', [10])
robot.run('SetBlending', [10])
robot.run('SetAutoConf', [1])
robot.run('ResumeMotion')
robot.get_response()
robot.run('SetEOB', [1])
robot.get_response()
# This will move the head of the robot in a square
robot.run('MoveJoints', [-20.000, 10.000, -10.000, 20.000, -10.000, -10.000])
robot.run('MoveJoints', [20.000, -10.000, 10.000, -20.000, 20.000, -10.000])
robot.run('MoveJoints', [-20.000, 10.000, -10.000, 20.000, -10.000, -10.000])
robot.run('MoveJoints', [0.000, -20.000, 20.000, 0.000, 20.000, 0.000])
robot.wait_for('3012', 'Did not receive EOB')
robot.run('GetJoints')
robot.get_response()
robot.run('Delay', [1])
robot.run('DeactivateRobot')
print("Main_program done")
sys.stdout.flush()

# Pause execution before closing process (allows users to read last message)
time.sleep(2)
