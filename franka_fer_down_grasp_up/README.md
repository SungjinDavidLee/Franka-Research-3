# Franka FER Down-Grasp-Up Demo

ROS 2 Jazzy 기반 Franka FER 실제 로봇 데모입니다.

동작 순서:

1. Gripper OPEN
2. End-effector를 Base-frame Z 방향으로 200 mm 하강
3. 바닥에서 Gripper CLOSE
4. 닫힌 상태로 잠시 유지
5. End-effector를 원래 위치로 복귀
6. 원위치 도착 직후 Gripper OPEN

검증된 환경:

- Workspace: `~/franka_ros2_ws`
- Robot type: `fer`
- Robot IP: `172.16.0.2`
- PC Franka NIC: `172.16.0.1/24`
- NIC: `enp3s0`
- Cartesian descent: `0.20 m`
- Down time: `3.0 s`
- Hold time: `5.0 s`
- Up time: `3.0 s`
- Gripper close trigger: arm start 후 `3.5 s`
- Gripper open trigger: arm start 후 `11.1 s`

> 실제 로봇을 움직입니다. 실행 전 작업공간, E-stop, 네트워크, Franka error 상태를 반드시 확인하세요.

## 1. Franka 전용 Ethernet

```bash
sudo nmcli connection add \
  type ethernet \
  ifname enp3s0 \
  con-name franka \
  ipv4.method manual \
  ipv4.addresses 172.16.0.1/24 \
  ipv4.never-default yes \
  ipv6.method disabled

sudo nmcli connection modify franka \
  connection.autoconnect yes \
  connection.autoconnect-priority 100

sudo nmcli connection up franka
```

확인:

```bash
ip -br addr show enp3s0
ip route get 172.16.0.2
ping -c 5 172.16.0.2
```

## 2. Cartesian controller 수정

기존 파일:

```text
~/franka_ros2_ws/src/franka_ros2/franka_example_controllers/src/fr3/cartesian_pose_example_controller.cpp
```

패치 적용:

```bash
python3 scripts/apply_cartesian_down_up.py \
  ~/franka_ros2_ws/src/franka_ros2/franka_example_controllers/src/fr3/cartesian_pose_example_controller.cpp
```

빌드:

```bash
cd ~/franka_ros2_ws
source /opt/ros/jazzy/setup.bash

colcon build \
  --packages-select franka_example_controllers \
  --symlink-install \
  --allow-overriding franka_example_controllers
```

빌드 후 arm bringup을 재시작해야 새 controller library가 로드됩니다.

## 3. Arm bringup

터미널 1:

```bash
cd ~/franka_ros2_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash

ros2 launch franka_bringup franka.launch.py \
  robot_type:=fer \
  robot_ip:=172.16.0.2 \
  load_gripper:=false \
  use_fake_hardware:=false
```

## 4. Gripper bringup

터미널 2:

```bash
cd ~/franka_ros2_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash

ros2 launch franka_gripper gripper.launch.py \
  robot_ip:=172.16.0.2 \
  robot_type:=fer \
  namespace:=fer_gripper \
  use_fake_hardware:=false
```

처음 사용 시 homing:

```bash
ros2 action send_goal \
  /fer_gripper/franka_gripper/homing \
  franka_msgs/action/Homing \
  "{}"
```

## 5. Cartesian controller 준비

터미널 3:

```bash
cd ~/franka_ros2_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash

ros2 control load_controller cartesian_pose_example_controller
ros2 control set_controller_state cartesian_pose_example_controller inactive
```

확인:

```bash
ros2 control list_controllers
ros2 control list_hardware_components | grep "state:"
```

정상 기준:

```text
cartesian_pose_example_controller  inactive
joint_state_broadcaster            active
franka_robot_state_broadcaster     active
state: id=3 label=active
```

## 6. 실행 전 점검

```bash
./scripts/check_status.sh
```

`current_errors`가 모두 `false`인지 확인하고, TCP 아래 200 mm + tool/finger 길이만큼 충돌 여유가 있는지 확인합니다.

## 7. 통합 데모 실행

```bash
./scripts/run_down_grasp_up.sh
```

시간 흐름:

```text
OPEN
  ↓
0~3 s    DOWN 200 mm
  ↓
3.5 s    CLOSE 시작
  ↓
3~8 s    bottom HOLD
  ↓
8~11 s   UP
  ↓
11.1 s   OPEN
```

재실행 전 controller를 다시 inactive로 내립니다.

```bash
ros2 control switch_controllers \
  --deactivate cartesian_pose_example_controller
```

## 8. Gripper 단독 테스트

OPEN:

```bash
ros2 action send_goal -f \
  /fer_gripper/franka_gripper/move \
  franka_msgs/action/Move \
  "{width: 0.08, speed: 0.05}"
```

CLOSE:

```bash
ros2 action send_goal -f \
  /fer_gripper/franka_gripper/move \
  franka_msgs/action/Move \
  "{width: 0.00, speed: 0.05}"
```


https://github.com/user-attachments/assets/a43f54b2-4a10-4caf-b590-83ca2c636663



