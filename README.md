# Achar a saída de uma sala com OpenCV em ROS <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcQdgBEX9U3kDSvXtCVyDqfA1uIlomS8rwJQCw&usqp=CAU" width="40" />

## Visão geral

Este projeto simula um robô que usa **[opencv](https://pypi.org/project/opencv-python/)** para achar a saída de uma sala. O robô usado, o [P3DX, disponível no ROS](http://wiki.ros.org/Robots/AMR_Pioneer_Compatible), tem uma câmera e um escaneador a laser. 
Neste projeto, o robô gira em torno do eixo Z até achar a porta, então segue o caminho até lá.

![SLAM no ROS](https://github.com/marcos-moura97/find_exit_opencv_ros/vista_cima.png  "vista_cima")

Ao captar as imagens, realizam-se 3 operações:

  - Achar os cantos;
  ![Cantos](https://github.com/marcos-moura97/find_exit_opencv_ros/paredes.png  "paredes")
  - Binarizar a imagem, dentro das paredes fica preto e onde não tem parede fica branco;
  ![monocromatico](https://github.com/marcos-moura97/find_exit_opencv_ros/blob/master/parede_monocromatica.png "parede_monocromatica")
  - Focalizar o branco em 3/4 da tela, o que evita que o céu, por exemplo, entre no equacionamento;
  ![foco](https://github.com/marcos-moura97/find_exit_opencv_ros/seguir_linha.png  "rvi2")

O robô usa um simples controle proporcional, para apenas apontar o robô para a entrada com velocidade constante.


## Requisitos

  - ROS Melodic
  - Catkin
  - Rviz
  - Gazebo
  
## Construir

Você deve seguir no terminal:

- Criar o espaço de trabalho catkin:

``` sh
$ mkdir catkin_ws
$ cd catkin_ws
$ mkdir src
$ catkin_make
```

- Clonar o repositório e a construí-lo:

``` sh
$ cd ~/catkin_ws/src
$ git clone https://github.com/marcos-moura97/find_exit_opencv_ros.git
$ cd ..
$ catkin_make
```

## Para rodar

Para executar o projeto e ver o mundo do gazebo e o rviz, execute as seguintes etapas:



- Executar o roscore

``` sh
$ cd ~/catkin_ws/
$ source devel/setup.bash
$ roscore
```

- Lançar do programa

``` sh
$ roslaunch labirinto sala.launch
```

- Executar o código para achar a saída

``` sh
$ rosrun labirinto achacantos.py
```




# A example of SLAM in ROS <img src="https://www.championprofessional.com/wp-content/uploads/2015/07/en-icon.png" width="40" />

## Overview

This project simulates a robot that uses **[opencv](https://pypi.org/project/opencv-python/)** to find the exit from a room. The robot used, the [P3DX, available on ROS] (http://wiki.ros.org/Robots/AMR_Pioneer_Compatible), has a camera and a laser scanner.
In this project, the robot rotates around the Z axis until it finds the door, then follows the path there.

![SLAM no ROS](https://github.com/marcos-moura97/find_exit_opencv_ros/vista_cima.png  "rvi2")

When capturing images, 3 operations are performed:

  - Find the corners;
  ![Cantos](https://github.com/marcos-moura97/find_exit_opencv_ros/paredes.png  "rvi2")
  - To binarize the image, inside the walls it is black and where there is no wall it is white;
  ![monocromatico](https://github.com/marcos-moura97/find_exit_opencv_ros/parede_monocromatica.png  "rvi2")
  - Focus white on 3/4 of the screen, which prevents the sky, for example, from entering the equation;
  ![foco](https://github.com/marcos-moura97/find_exit_opencv_ros/seguir_linha.png  "rvi2")

The robot uses a simple proportional control, to just point the robot towards the entrance with constant speed.


## Dependencies

  - ROS Melodic
  - Catkin
  - Rviz
  - Gazebo
  
## To build

You must follow in terminal:

- Create the catkin workspace:

```sh
$ mkdir catkin_ws
$ cd catkin_ws
$ mkdir src
$ catkin_make
```

- Cloning the repository and building:

```sh
$ cd ~/catkin_ws/src
$ git clone https://github.com/marcos-moura97/find_exit_opencv_ros.git
$ cd ..
$ catkin_make
```

## To Run

To run the project and see the gazebo world and the rviz, execute the following steps:



- Running roscore

```sh
$ cd ~/catkin_ws/
$ source devel/setup.bash
$ roscore
```

- Launching the program

```sh
$ roslaunch labirinto bot_model.launch
```

- Execute the program that find teh exit
```sh
$ rosrun labirinto achacantos.py
```
