#!/usr/bin/env python


#Este programa e testado no Gazebo Simulator
#Este script usa o pacote cv_bridge (funciona via OpenCV) para converter imagens relacionadas ao topico
# sensor_msgs / Imagem em mensagens OpenCV e depois converta suas cores de RGB para HSV
#a seguir, aplica um limite para matizes proximos a cor amarela para obter a imagem binaria
#para poder ver apenas a linha amarela e seguir essa linha
#utliza-se uma abordagem chamada proporcional e simplesmente medias

import rospy, cv2, cv_bridge, numpy, math
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

class Follower:

        def __init__(self):

                self.bridge = cv_bridge.CvBridge()
                cv2.namedWindow("window", 1)

                self.image_sub = rospy.Subscriber('/p3dx/front_camera/image_raw',
                        Image, self.image_callback)

                self.cmd_vel_pub = rospy.Publisher('p3dx/cmd_vel',
                        Twist, queue_size=1)

                self.odom_sub = rospy.Subscriber('p3dx/odom',Odometry,self.callback_odom)  

                self.twist = Twist()

        def callback_odom(self,msg): 
                xr=msg.pose.pose.position.x
                yr=msg.pose.pose.position.y
                print("%f %f" %(xr,yr))

        def image_callback(self, msg):

                image = self.bridge.imgmsg_to_cv2(msg,desired_encoding='bgr8')
                hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
                lower_yellow = numpy.array([ 10, 10, 10])
                upper_yellow = numpy.array([255, 255, 250])
                mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

                h, w, d = image.shape
                search_top = int(3*h/4)
                search_bot = int(3*h/4 + 20)
                mask[0:search_top, 0:w] = 0
                mask[search_bot:h, 0:w] = 0

                M = cv2.moments(mask)
                if M['m00'] > 0:
                        cx = int(M['m10']/M['m00'])
                        cy = int(M['m01']/M['m00'])
                        cv2.circle(image, (cx, cy), 20, (0,0,255), -1)
#O controlador proporcional e implementado nas quatro linhas seguintes, que
#e repossivel da escala linear de um erro para acionar a saida de controle.

                        err = math.sqrt(abs(cx**2 - cy**2)) - w/2
                        self.twist.linear.x = 1
                        self.twist.angular.z = -float(err) / 100
                        self.cmd_vel_pub.publish(self.twist)
                cv2.imshow("window", image)
                cv2.waitKey(3)

rospy.init_node('seguidor_linha')
follower = Follower()
rospy.spin()

