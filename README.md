# MecaRobot

The MecaRobot class provides a simple Python interface for sending commands to, and receiving responses from, the Meca500 robot from Mecademic.

# Interface

To use the MecaRobot class, create a MecaRobot object, with parameters specifying its IP address and port. This will open the connection to the robot, clear any errors that are present, activate the robot, and run the homing routine.

```
import MecaRobot
robot = MecaRobot("192.168.0.100", "10000")
```

To close the connection to the robot, use the ```disconnect``` function.

```
robot.disconnect()
```

To send commands, use the ```run``` function. If the command in question has arguments, pass them as a list.

```
robot.run('ResumeMotion')
robot.run('MoveJoints', [0, 0, 0, 0, 0, 0])
```

To wait for any response before continuing, use the ```get_response``` function. To wait for a specific response before continuing, use the ```wait_for``` function, with parameters of the expected answer and the error message to print if that answer is not received within a timeout window.

```
robot.wait_for('3012', 'Did not receive EOB')
```
