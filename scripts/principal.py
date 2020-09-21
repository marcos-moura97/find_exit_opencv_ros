#!/usr/bin/env python


#Este programa  testado no Gazebo Simulator
#Este script usa o pacote cv_bridge para converter imagens vindas do tpico
#sensor_msgs/Image para mensagens OpenCV para serem analizadas pelo pacote
#pyzbar, a procura de QR Codes. Um cdigo bem simples, em que o rob p3dx
#ir girar em torno do eixo Z at encontrar uma parede que tenha um QR Code.
#Os valores das coordenadas de posio do rob so captadas usando odometria

import rospy, cv2, cv_bridge, numpy, math, argparse
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

from pyzbar import pyzbar



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
                self.canto = 0

        def callback_odom(self,msg): 
                xr=msg.pose.pose.position.x
                yr=msg.pose.pose.position.y

        def image_callback(self, msg):

                image = self.bridge.imgmsg_to_cv2(msg,desired_encoding='bgr8')
                gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

                _,threshold = cv2.threshold(gray, 110, 255,cv2.THRESH_BINARY) 
                


                #if self.canto==0:
                #        self.twist.angular.z = math.pi/10
                #        self.cmd_vel_pub.publish(self.twist)

                #else:
                #        self.twist.angular.z = 0
                        
                #        self.cmd_vel_pub.publish(self.twist)

                contours,_=cv2.findContours(threshold, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2:]

#                for canto in cantos:
#                        x, y = canto.ravel()
#                        cv2.circle(image,(x,y),3,255,-1)

                for cnt in contours : 
                         area = cv2.contourArea(cnt)
                         canto = 1
                         if area > 400:  
                                  approx = cv2.approxPolyDP(cnt,0.009 * cv2.arcLength(cnt, True), True) 
   
# Checking if the no. of sides of the selected region is 7. 
                                  #if(len(approx) == 7):  
                                  cv2.drawContours(image, [approx], 0, (0,255,255), 5) 
   


		#hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
                lower_yellow = numpy.array([ 10, 10, 10])
                upper_yellow = numpy.array([255, 2550, 250])

		# Mask red pixels
                mask = cv2.inRange(image, lower_yellow, upper_yellow)

		## enchendo as paredes
		
		# Calculate x,y coordinate of centre of red pixels
                M = cv2.moments(mask)
                if M['m00'] > 0:
                        cx = int(M['m10']/M['m00'])
                        cy = int(M['m01']/M['m00'])
                        #cv2.circle(image, (cx, cy), 20, (0,0,255), -1)
			# Flood fill with white starting from centroid
		        cv2.floodFill(mask,mask=None,seedPoint=(cx,cy),newVal=(0,0,0))

                cv2.imshow("mask", mask)
		# Achar o branco
		h, w, d = image.shape
                search_top = int(3*h/4 - 40)
                search_bot = int(3*h/4)
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

		elif M['m00'] == 0:

			self.twist.linear.x = 0
                        self.twist.angular.z = math.pi/3 #giro de 60 graus
                        self.cmd_vel_pub.publish(self.twist)

		## MOSTRANDO AS IMAGENS
                cv2.imshow("window", image)
                cv2.imshow("Imagem", mask)
                #cv2.imshow("Imagem2", mask_invertido)
                cv2.waitKey(3)
		##

rospy.init_node('seguidor_linha')
follower = Follower()
rospy.spin()

