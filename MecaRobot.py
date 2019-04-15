#!/usr/bin/python3

import time
import sys
from threading import Timer
import socket

# ----------- communication class ------------- #
class MecaRobot:
    """Robot class for programming Meca500 robots"""
    def __init__(self, ip, port):
        self.BUFFER_SIZE = 512  # bytes
        self.TIMEOUT = 60       # seconds
        self.ip = ip
        self.port = port
        #self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.sock.settimeout(self.TIMEOUT)
        self.sock = None
        print('Connecting to robot %s:%i' % (ip, port))
        sys.stdout.flush()
        start_time = time.perf_counter()
        while True:
            print('Waiting for connection...')
            self.connect()
            response = self.return_response()
            print("Startup response: ", response)
            if response[1:5] == "3000":
                break
            elif time.perf_counter() - start_time >= self.TIMEOUT:
                raise TimeoutError("Waited too long for the port {} on host {} to start accepting connections".format(port, ip))
            else:
                time.sleep(0.5)
        
        # Reset, activate and home the robot
        self.run('ResetError')
        self.get_response()
        self.run('ActivateRobot')
        self.get_response()
        self.run('Home')
        self.get_response()
    
    def connect(self):
        start_time = time.perf_counter()
        while True:
            try:
                self.sock = socket.create_connection((self.ip, self.port), timeout=self.TIMEOUT)
                break
            except OSError as ex:
                time.sleep(0.01)
                if time.perf_counter() - start_time >= self.TIMEOUT:
                    raise TimeoutError("Waited too long for the port {} on host {} to start accepting connections".format(port, ip)) from ex
        

    def send_str(self, msg):
        sent = self.sock.send(bytes(msg+'\0', 'ascii'))
        if sent == 0:
            raise RuntimeError("Robot connection broken")

    def receive_str(self):
        byte_data = self.sock.recv(self.BUFFER_SIZE)
        if byte_data == b'':
            raise RuntimeError("Robot connection broken")
        return byte_data.decode('ascii')
        
    def run(self, cmd, values=None):
        if isinstance(values, list):
            str_send = cmd + '(' + (','.join(format(vi, ".6f") for vi in values)) + ')'
        elif values is None:
            str_send = cmd
        else:
            str_send = cmd + '(' + str(values) + ')'

        # Send command to robot
        self.send_str(str_send)

        print('Running: ' + str_send)
        sys.stdout.flush()

    def get_response(self):
        robot_answer = ""
        while robot_answer == "":
            robot_answer = self.receive_str()

        print('Received: %s' % robot_answer)
        sys.stdout.flush()

    def return_response(self):
        robot_answer = ""
        while robot_answer == "":
            robot_answer = self.receive_str()
        return robot_answer

    def wait_for(self, answer, error_message):
        answer_timer = Timer(10, self.answer_not_found, args=error_message)
        robot_answer = ""

        # loop to find answer, if answer is not found after 10 seconds print error message
        while robot_answer != answer:
            robot_output = self.receive_str()

            if robot_output.find(answer) == -1 & answer_timer.is_alive() is False:
                answer_timer.start()
                answer_timer.join()

            elif robot_output.find(answer) != -1:
                robot_answer = answer

        answer_timer.cancel()
        print('Received: %s' % robot_answer)
        sys.stdout.flush()

    @staticmethod
    def answer_not_found(error_message):
        print(error_message)
        exit(0)
		
    def disconnect(self):
        self.sock.close()

