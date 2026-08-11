#!/usr/bin/env bash
set -euo pipefail

source /opt/ros/jazzy/setup.bash
source "${HOME}/franka_ros2_ws/install/setup.bash"

GRIPPER=/fer_gripper/franka_gripper/move

echo "===== OPEN -> DOWN -> CLOSE -> UP -> OPEN ====="

echo "[0] Gripper OPEN"
ros2 action send_goal -f \
  "$GRIPPER" \
  franka_msgs/action/Move \
  "{width: 0.08, speed: 0.05}"

sleep 0.5

(
  sleep 3.5
  echo "[CLOSE] Closing at bottom..."
  ros2 action send_goal -f \
    "$GRIPPER" \
    franka_msgs/action/Move \
    "{width: 0.00, speed: 0.05}"
) &
CLOSE_PID=$!

(
  sleep 11.1
  echo "[OPEN] Opening at top..."
  ros2 action send_goal -f \
    "$GRIPPER" \
    franka_msgs/action/Move \
    "{width: 0.08, speed: 0.05}"
) &
OPEN_PID=$!

echo "[ARM] Starting Cartesian motion..."
ros2 control switch_controllers \
  --activate cartesian_pose_example_controller &
ARM_PID=$!

wait "$ARM_PID" || true
wait "$CLOSE_PID"
wait "$OPEN_PID"

echo "===== FINISHED ====="
