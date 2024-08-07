#!/usr/bin/env python3

# Copyright (C) 2023  0nhc
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.If not, see <https://www.gnu.org/licenses/>.

import rospy
import pcl
from sensor_msgs.msg import PointCloud2
import ros_numpy
import numpy as np
import math
import tf
from sensor_msgs.msg import Image
from ultralytics import YOLO

height = 480
width = 640
if_pcl_ready = 0
parent_frame = "camera_color_optical_frame"
detection_model = YOLO("yolov8m.pt")
det_image_pub = rospy.Publisher("/ultralytics/detection/image", Image, queue_size=5)
class_names = detection_model.names

def image_callback(data):
    global p,if_pcl_ready

    array = ros_numpy.numpify(data)
    if det_image_pub.get_num_connections():
        det_result = detection_model(array)
        det_annotated = det_result[0].plot(show=False)
        det_image_pub.publish(ros_numpy.msgify(Image, det_annotated, encoding="rgb8"))
        obj_tf = tf.TransformBroadcaster()
        if(if_pcl_ready):
            bounding_boxes = det_result[0].boxes
            id = 0
            for i in bounding_boxes:
                x = 0
                y = 0
                z = 0
                valid_num = 0
                xmin, ymin, xmax, ymax = i.xyxy[0]
                class_id = int(i.cls)
                class_name = class_names[class_id]
                length = xmax - xmin
                height = ymax - ymin
                for ix in range(int(xmin+length/4),int(xmax-length/2)):
                    for iy in range(int(ymin+height/4),int(ymax-height/4)):
                        index = int((iy-1)*width+ix)
                        position = p[index]
                        if not(math.isnan(position[2])):
                            x = x + position[0]
                            y = y + position[1]
                            z = z + position[2]
                            valid_num = valid_num + 1
                if(valid_num):
                    x = x/valid_num
                    y = y/valid_num
                    z = z/valid_num
                obj_tf.sendTransform((x, y, z),tf.transformations.quaternion_from_euler(0, -math.pi/2, math.pi/2),rospy.Time.now(),class_name+str(id),parent_frame)
                id = id + 1

def depth_callback(data):
    global p,if_pcl_ready
    pc = ros_numpy.numpify(data)
    np_points = np.zeros((height * width, 3), dtype=np.float32)
    np_points[:, 0] = np.resize(pc['x'], height * width)
    np_points[:, 1] = np.resize(pc['y'], height * width)
    np_points[:, 2] = np.resize(pc['z'], height * width)
    p = pcl.PointCloud(np.array(np_points, dtype=np.float32))
    if_pcl_ready = 1

def listener():
    rospy.init_node('depth_combination', anonymous=True)
    rospy.Subscriber("/camera/depth_registered/points", PointCloud2, depth_callback)
    rospy.Subscriber("/camera/color/image_rect_color", Image, image_callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        p = np.zeros((height * width, 3), dtype=np.float32)
        listener()
    except Exception as e:
        rospy.logerr(f"Error in main: {e}")
