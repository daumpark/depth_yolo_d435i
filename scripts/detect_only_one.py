#!/usr/bin/env python3

import rospy
import pcl
from sensor_msgs.msg import PointCloud2
import ros_numpy
import numpy as np
import math
from sensor_msgs.msg import Image
from ultralytics import YOLO
from geometry_msgs.msg import PointStamped

class ObjectDetector():
    def __init__(self):
        self.height = 480
        self.width = 640
        self.if_pcl_ready = 0
        self.parent_frame = "camera_color_optical_frame"
        # detection_model = YOLO(os.path.join(os.path.dirname(__file__), 'crystal.pt'))
        self.detection_model = YOLO('yolov8m.pt')
        self.class_names = self.detection_model.names
        self.p = np.zeros((self.height * self.width, 3), dtype=np.float32)
        self.if_pcl_ready = 0
        self.objectPose = PointStamped()
        self.objectName = "bottle"
        self.stack = 0

        self.point_sub = rospy.Subscriber("/camera/depth_registered/points", PointCloud2, self.depth_callback)
        self.image_sub = rospy.Subscriber("/camera/color/image_raw", Image, self.image_callback)
        self.det_image_pub = rospy.Publisher("/ultralytics/detection/image", Image, queue_size=5)
        self.obj_pub = rospy.Publisher("object_detector/position", PointStamped, queue_size=5)

    def image_callback(self, data):
        array = ros_numpy.numpify(data)
        if self.det_image_pub.get_num_connections():
            det_result = self.detection_model(array)
            det_annotated = det_result[0].plot(show=False)
            self.det_image_pub.publish(ros_numpy.msgify(Image, det_annotated, encoding="rgb8")) #rgb8
            # obj_tf = tf.TransformBroadcaster()
            if(self.if_pcl_ready):
                bounding_boxes = det_result[0].boxes
                for i in bounding_boxes:
                    x = 0
                    y = 0
                    z = 0
                    valid_num = 0
                    xmin, ymin, xmax, ymax = i.xyxy[0]
                    class_id = int(i.cls)
                    class_name = self.class_names[class_id]
                    if class_name == self.objectName:
                        length = xmax - xmin
                        height = ymax - ymin
                        for ix in range(int(xmin+length/4),int(xmax-length/2)):
                            for iy in range(int(ymin+height/4),int(ymax-height/4)):
                                index = int((iy-1)*self.width+ix)
                                position = self.p[index]
                                if not(math.isnan(position[2])):
                                    x = x + position[0]
                                    y = y + position[1]
                                    z = z + position[2]
                                    valid_num = valid_num + 1
                        if(valid_num):
                            x = x/valid_num
                            y = y/valid_num
                            z = z/valid_num
                        # obj_tf.sendTransform((x, y, z),tf.transformations.quaternion_from_euler(0, -math.pi/2, math.pi/2),rospy.Time.now(),class_name+str(id),parent_frame)
                        self.objectPose.header.stamp = rospy.get_rostime()
                        self.objectPose.point.x = x
                        self.objectPose.point.y = y
                        self.objectPose.point.z = z
                        self.objectPose.header.frame_id = self.parent_frame
                        self.obj_pub.publish(self.objectPose)
                        # print(self.objectPose)

    def depth_callback(self, data):
        pc = ros_numpy.numpify(data)
        np_points = np.zeros((self.height * self.width, 3), dtype=np.float32)
        np_points[:, 0] = np.resize(pc['x'], self.height * self.width)
        np_points[:, 1] = np.resize(pc['y'], self.height * self.width)
        np_points[:, 2] = np.resize(pc['z'], self.height * self.width)
        self.p = pcl.PointCloud(np.array(np_points, dtype=np.float32))
        self.if_pcl_ready = 1

if __name__ == '__main__':
    rospy.init_node('detect_only_one', anonymous=True)
    try:
        objectdetector = ObjectDetector()
    except Exception as e:
        rospy.logerr(f"Error in main: {e}")
    rospy.spin()
