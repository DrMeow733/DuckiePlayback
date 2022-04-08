#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
from duckietown.dtros import DTROS, NodeType, TopicType
from duckietown_msgs.msg import Twist2DStamped, BoolStamped
from time import sleep

class MyPublisherNode(DTROS):
    def __init__(self, node_name):
        super(MyPublisherNode, self).__init__(
            node_name=node_name, node_type=NodeType.CONTROL)
        
        self.pub = rospy.Publisher('/meowbot/joy_mapper_node/car_cmd', 
                        Twist2DStamped, queue_size=1, dt_topic_type=TopicType.CONTROL)
        
        self.speed = 0.0
        self.omega = 0.0

        rospy.loginfo("Running...")

    def run(self):
        """
        rate = rospy.Rate(2)
        while not rospy.is_shutdown():
            msg = Twist2DStamped()
            msg.header.stamp = rospy.get_rostime()

            msg.v = self.speed
            msg.omega = self.omega

            rospy.loginfo("Publishing message")

            self.pub.publish(msg)
            rate.sleep()
        """
        prog = input("Input filename to repeat: ")
        if prog == "":
            prog = "rect.csv"
        with open(prog, "r") as f:
            for i, move in enumerate(f.readlines()):
                data = move.split(" //")[0].split(", ")
                v = float(data[0])
                omega = float(data[1])
                time = float(data[2])

                print(f"Instruction {i} - V: {v} Omega: {omega} Time: {time}")

                msg = Twist2DStamped()
                msg.header.stamp = rospy.get_rostime()

                msg.v = v
                msg.omega = omega

                self.pub.publish(msg)

                sleep(time)

if __name__ == '__main__':
    try:
        rospy.loginfo("Starting node")
        node = MyPublisherNode(node_name='my_publisher_node')
        while True:
            node.run()
    except rospy.ROSInterruptException:
        pass