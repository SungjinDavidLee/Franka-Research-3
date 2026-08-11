#!/usr/bin/env bash
set -e

source /opt/ros/jazzy/setup.bash
source "${HOME}/franka_ros2_ws/install/setup.bash"

echo "===== NETWORK ====="
ip route get 172.16.0.2 || true
ping -c 3 172.16.0.2 || true

echo
echo "===== HARDWARE ====="
ros2 control list_hardware_components | grep -E "state:|cartesian_pose_command" || true

echo
echo "===== CONTROLLERS ====="
ros2 control list_controllers || true

echo
echo "===== GRIPPER ACTIONS ====="
ros2 action list -t | grep fer_gripper || true

echo
echo "===== CURRENT POSE ====="
ros2 topic echo /franka_robot_state_broadcaster/current_pose --once || true

echo
echo "===== ROBOT ERRORS ====="
ros2 topic echo \
  /franka_robot_state_broadcaster/robot_state \
  --once | grep -A40 -E "^robot_mode:|^current_errors:" || true
