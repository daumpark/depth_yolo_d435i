[![ROS1 VERSION](https://img.shields.io/badge/ROS-ROS%201%20Noetic-brightgreen)](http://wiki.ros.org/noetic)
&nbsp;
[![Ubuntu VERSION](https://img.shields.io/badge/Tested-Ubuntu%2020.04-green)](https://ubuntu.com/)
&nbsp;
[![LICENSE](https://img.shields.io/badge/license-GPL%203-informational)](https://github.com/0nhc/depth_yolo/blob/master/LICENSE)
&nbsp;

# Description
This is a package getting the 3D location of the objects detected.

It will automatically send tf transforms between the objects detected and d435i_link.

# Installation
## step1 Install dependencies
```bash
pip install ros_numpy
```
```bash
pip install ultralytics
```
https://dev.intelrealsense.com/docs/compiling-librealsense-for-linux-ubuntu-guide

https://github.com/pal-robotics/ddynamic_reconfigure.git

https://github.com/IntelRealSense/realsense-ros/tree/ros1-legacy

## step2 install depth_yolo
Then, you can continue installing depth_yolo
```bash
git clone https://github.com/daumpark/depth_yolo_d435i.git
cd ..
catkin_make -DCMAKE_BUILD_TYPE=Release
source devel/setup.bash
```
# Usage
```bash
roslaunch depth_v8 depth_yolo.launch
```
# Contributing
Contributions are welcome! Please read the [contributing guidelines](CONTRIBUTING.md) before submitting a pull request.



# License
This project is licensed under the GPL 3 License. See [LICENSE](LICENSE) for more information.
```
    Copyright (C) 2023  0nhc
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.If not, see <https://www.gnu.org/licenses/>.                               
```

# Acknowledgments 
I would like to thank the following people for their contributions to this project:

- **Herman Ye**  

  I would like to take a moment to express my sincere gratitude to Herman Ye for his invaluable contribution to this project's README. His attention to detail and clear communication have greatly improved the overall quality of the documentation, making it easier for others to understand and contribute to the project.  
  Herman Ye's dedication and hard work have not gone unnoticed, and I am truly grateful for his efforts. Thank you, Herman Ye, for your outstanding work and for being an integral part of this project's success.for implementing the search functionality.
