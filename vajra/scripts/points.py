#!/usr/bin/env python
import rospy
from sensor_msgs.msg import CameraInfo,Image
import cv2
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
import math
import sensor_msgs.point_cloud2 as pcl2
from sensor_msgs.msg import PointCloud2, PointField
import std_msgs.msg
import numpy as np
import std_msgs.msg 


rospy.loginfo("Hello ROS!")
bridge = CvBridge()
img_pub1 = rospy.Publisher('/pothole', Image, queue_size=10)
point_pub= rospy.Publisher('/pointcloud', PointCloud2, queue_size=10)

def image_callback2(data):
    global k
    temp = data.K
    k=np.reshape(temp, (3,3))
    print(k)


def image_callback(img_msg):
    global k
    try:
        cv_image = bridge.imgmsg_to_cv2(img_msg, "passthrough")
    except CvBridgeError:
        rospy.logerr("CvBridge Error: {0}".format(e))

    cv_image = cv2.rotate(cv_image, cv2.ROTATE_90_CLOCKWISE)
    imgray = cv2.cvtColor(cv_image,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(imgray,200,255,0)
    contours =  cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[-2]
    cv2.drawContours(cv_image, contours, -1, (0,255,0), 3)
    img_pub1.publish(bridge.cv2_to_imgmsg(cv_image, encoding="passthrough"))
    fields = [PointField('x', 0, PointField.FLOAT32, 1),
              PointField('y', 4, PointField.FLOAT32, 1),
              PointField('z', 8, PointField.FLOAT32, 1),
              PointField('rgb', 12, PointField.UINT32, 1),
              ]
    pts = []
    cp = math.cos(0.45)
    sp = math.sin(0.45)
    n = np.array([[0], [0], [1]]) 
    R = np.array([[1, 0, 0], [0, cp, sp], [0, -sp, cp]]) 
    nc = np.transpose(R.dot(n))
    kinv = np.linalg.inv(k)
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True)
        n = approx.ravel()
        i = 0
        
        for j in n:
            if(i % 2 == 0):
                x = n[i]
                y = n[i + 1]
                uv = np.array([[y], [x], [1]])
                mul1 = np.dot(kinv, uv)
                mul2 = np.dot(nc,mul1)
                cp = math.cos(0.45)
                sp = math.sin(0.45)
                R = np.array([[1, 0, 0], [0, cp, -sp], [0, sp, cp]])
                t = R.dot(1.18*mul1/mul2) 
                pts.append(t)
            i = i + 1
    Header = std_msgs.msg.Header()
    Header.stamp = rospy.Time.now()
    Header.frame_id = "camera_right"
    pc2 = pcl2.create_cloud_xyz32(Header, pts)
    point_pub.publish(pc2)

def camera():
    rospy.init_node('pothole', anonymous=True)
    rospy.Subscriber("/camera/right/image_raw", Image, image_callback)
    rospy.Subscriber("/camera/right/camera_info", CameraInfo,image_callback2)
    rospy.spin()


if __name__ == '__main__':
    k= None 
    camera()


    
    

    


