#!/usr/bin/env python3

import rospy
from duckietown_msgs.msg import Twist2DStamped

v = 0
omega = 0
t = 0

f = open("output.csv", "w")

def callback(data):
    global v
    global omega
    global t
    global f

    d_v = data.v
    d_omega = data.omega
    d_timestamp = data.header.stamp

    if d_v != v or d_omega != omega:
        if t == 0:
            t = d_timestamp
        
        d_t = d_timestamp - t
        
        t = d_timestamp

        print(f'[{d_t.to_sec()}] V: {round(d_v,4)} Omega: {round(d_omega,4)}')
        f.write(f"{round(d_v,4)}, {round(d_omega, 4)}, {d_t.to_sec()}\n")
        v = d_v
        omega = d_omega

def listener():

    rospy.init_node('recorder', anonymous=True)

    rospy.Subscriber('/meowbot/joy_mapper_node/car_cmd', 
                        Twist2DStamped, callback)

    rospy.spin()

if __name__ == '__main__':
    listener()
    f.close()
