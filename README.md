# vajra_simulation_task

### Urdf:
This folder contains 2 files vajra.xacro and vajra.gazebo, vajra.xacro contains the links and joints for the body, tier,castor wheel, and camera (The mesh files used are located in the mesh folder).
Vajra.gazebo has plugins used by the urdf files, like differential drive plugin and camera controller plugin.

### Worlds:
This folder conatains a .world file that has the green ground (my_ground_plane) and pothole models.

### Scripts:
Contains a points.py file that which subscribes to the camera image, detects the contours for the white potholes and converts it into points, it subscribes to the camera_info topic to get the value for the intinsic camera matrix k. Then it performs rotation and translation operation on the contour points and makes a point cloud using them, then these point clouds are published as /pointcloud topic and can be subscribed in rviz to view it.

### Launch:
Contains the world.launch file which can be used to launch rviz,robot and world.

# Point cloud being displayed in Rviz
![Screenshot from 2022-08-09 20-20-07](https://user-images.githubusercontent.com/82026214/183683099-ff93880d-0ada-4ecb-980e-ac5a770d6701.png)

# The model in gazebo
![Screenshot from 2022-08-09 20-21-33](https://user-images.githubusercontent.com/82026214/183683148-1f0a8d54-5031-4861-afc5-0716caf8b41d.png).

To move the model with teleop we need to run the script "rosrun teleop_twist_keyboard teleop_twist_keyboard.py"

