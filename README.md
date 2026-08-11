# Franka Arm Setup & Operation Guide

> Franka Arm을 PC와 연결하여 수동 조작 또는 FCI/ROS 제어를 수행하기 위한 연구실용 기본 절차입니다.
>
> **주의:** 실제 로봇을 움직이기 전에는 주변 작업 공간, 비상정지 장치, 로봇 오류 상태를 반드시 확인하세요.

## 1. Network Configuration

실험실에서 사용하는 네트워크 설정:

- **Franka Arm**
  - IP: `192.168.0.1`
  - 용도: 별도로 기록된 Arm 측 IP

- **Arm + Control Box (FCI)**
  - IP: `172.16.0.2`
  - 용도: PC에서 Franka UI/FCI 접속 시 사용

- **Control PC**
  - IP: `172.16.0.1/24`
  - 용도: FCI 사용 시 PC Ethernet에 설정

FCI 제어에서는 **Control Box와 PC를 직접 Ethernet으로 연결**하는 구성을 권장합니다.

PC Ethernet 설정 예시:

```text
IP Address : 172.16.0.1
Netmask    : 255.255.255.0 (/24)
Robot/FCI  : 172.16.0.2
```

연결 확인:

```bash
ping 172.16.0.2
```

브라우저에서는 다음 주소로 Franka UI(Desk)에 접속합니다.

```text
https://172.16.0.2
```

자체 서명 인증서 때문에 브라우저 인증서 경고가 표시될 수 있습니다.

> **참고:** `172.16.0.1/24`와 `172.16.0.2/24`는 Franka 공식 문서에서도 FCI용 static IP 구성 예시로 사용됩니다. 실제 장비의 네트워크 설정이 변경되어 있다면 장비에 설정된 IP를 우선 사용하세요.

---

## 2. Power On & Initial Check

1. Franka Arm과 Control Box의 전원을 켭니다.
2. 부팅 및 self-test가 완료될 때까지 기다립니다.
3. PC에서 `172.16.0.2`에 접속되는지 확인합니다.
4. Franka UI에서 현재 오류 또는 Safety violation이 없는지 확인합니다.
5. 로봇 주변에 사람이나 장애물이 없는지 확인합니다.
6. 비상정지 장치를 바로 사용할 수 있는 상태인지 확인합니다.
7. 로봇을 움직여야 할 경우 **Joint Lock / Brake 상태를 확인하고 필요한 경우 해제(Open Brakes)** 합니다.

> **중요:** 단순히 LED 색상만 보고 로봇의 제어 가능 상태를 판단하지 말고 Franka UI의 상태도 함께 확인하세요.

---

## 3. Manual / Hand-Guiding Operation

로봇을 손으로 움직일 때는 Pilot-Grip의 Guiding 기능을 사용합니다.

Guiding-Mode Button을 이용해 다음 모드를 전환할 수 있습니다.

- **`Translation`**
  - End-Effector의 위치 이동 중심

- **`Rotation`**
  - End-Effector의 자세 회전 중심

- **`Free Move`**
  - Translation + Rotation을 포함한 자유로운 Hand-Guiding

- **`User-defined`**
  - 설정된 사용자 정의 Guiding Mode
  - 지원되는 구성에서 사용

수동 조작 절차:

1. 로봇의 Brake/Joint Lock 상태를 확인합니다.
2. 필요한 경우 Brake를 엽니다.
3. Pilot-Grip의 Guiding-Mode Button으로 원하는 모드를 선택합니다.
4. Guiding 입력을 활성화한 상태에서 로봇을 천천히 움직입니다.
5. 원하는 자세에 도달하면 Guiding 입력을 해제합니다.

> 기존 현장 기록의 **하얀색 LED = 수동 모드** 표시는 장비/시스템 이미지에 따라 의미가 달라질 수 있으므로, LED만으로 모드를 단정하지 않고 UI 상태와 Guiding Mode를 함께 확인하는 것을 권장합니다.

---

## 4. FCI / ROS External Control

FCI(Franka Control Interface)는 외부 PC에서 Franka를 실시간 제어하기 위한 인터페이스입니다.

### FCI 활성화

1. Franka UI에 접속합니다.
2. Brake가 열려 있고 외부 제어가 가능한 상태인지 확인합니다.
3. `Activate FCI`를 실행합니다.
4. FCI가 정상적으로 활성화되었는지 UI에서 확인합니다.
5. 그 후 PC에서 `libfranka`, `franka_ros`, 또는 `franka_ros2` 기반 프로그램을 실행합니다.

> `Activate FCI`는 Programming 상태, Brake가 닫힌 상태, Safety 관련 상태 등에 따라 거부될 수 있습니다.

### LED 상태에 대한 기록

실험실에서 관찰한 상태:

```text
Blue LED  -> 외부 제어 전 대기 상태로 관찰됨
Green LED -> FCI/ROS 외부 제어 활성 상태에서 관찰됨
White LED -> Hand-Guiding 과정에서 관찰됨
```

LED는 빠른 상태 확인용으로만 사용하고, **최종 상태 판단은 Franka UI 및 ROS/FCI 상태를 기준으로 합니다.**

---

## 5. ROS / FCI 실행 전 체크

실제 로봇 제어 프로그램을 실행하기 전에 다음을 확인합니다.

- [ ] Control Box 전원 ON
- [ ] PC Ethernet = `172.16.0.1/24`
- [ ] `ping 172.16.0.2` 성공
- [ ] Franka UI 접속 가능
- [ ] Robot error 없음
- [ ] Safety violation 없음
- [ ] Emergency Stop 상태 확인
- [ ] 작업 공간에 사람/장애물 없음
- [ ] End-Effector / Gripper 상태 확인
- [ ] Joint Lock / Brake 상태 확인
- [ ] FCI 활성화 상태 확인
- [ ] 사용할 Controller 및 명령 단위 확인
- [ ] 초기 자세가 안전한지 확인

---

## 6. Official Franka Examples

아래 내용은 **Franka Robotics 공식 `libfranka/pylibfranka` 및 `franka_ros2` 예제만** 정리한 것입니다.
사용자 정의 Pick-and-Place 예제는 포함하지 않습니다.

공식 예제는 크게 두 종류로 나눌 수 있습니다.

- **`pylibfranka` 예제**
  - Python에서 `libfranka`를 직접 사용
  - 로봇 상태 읽기, Joint Position, Joint Impedance, Gripper 등을 빠르게 확인할 때 유용
- **`franka_ros2` 예제**
  - ROS 2 + `ros2_control` 기반
  - Controller 구조, Cartesian 제어, IK, Gravity Compensation 등을 확인할 때 유용

> **주의:** `print_robot_state.py`처럼 상태만 읽는 예제를 제외하면 실제 Arm 또는 Gripper가 움직일 수 있습니다. 실행 전 Section 5의 Safety Checklist를 다시 확인하세요.

---

### 6.1 pylibfranka Official Examples

`pylibfranka`는 `libfranka`의 공식 Python binding입니다.

공식 README 기준 설치:

```bash
pip install pylibfranka
```

소스 저장소 안의 예제를 실행하는 경우:

```bash
cd pylibfranka/examples
```

---

#### Example 1 — Print Robot State

**공식 파일**

```text
print_robot_state.py
```

**목적**

Franka와 PC가 정상적으로 통신하는지 확인하고, 현재 Robot State를 읽습니다.

이 예제는 Arm에 motion command를 보내는 예제가 아니기 때문에 **처음 연결 테스트에 가장 적합한 예제**입니다.

**실행 예시**

```bash
python3 print_robot_state.py \
  --ip 172.16.0.2
```

출력 주기를 지정할 수도 있습니다.

```bash
python3 print_robot_state.py \
  --ip 172.16.0.2 \
  --rate 1 \
  --count 10
```

옵션 의미:

```text
--ip      Robot IP
--rate    상태 출력 주파수 [Hz]
--count   출력 횟수
          0이면 계속 출력
```

**예제 내부 동작**

```text
PC
 ↓
pylibfranka Robot 연결
 ↓
Robot State 읽기
 ↓
Terminal에 상태 출력
```

주요 확인 항목:

- Joint position
- Joint velocity
- Joint torque
- End-Effector pose
- End-Effector velocity
- External force / torque
- Robot mode
- Current error state
- Mass / inertia information

**이 예제로 확인할 것**

```text
[ ] Robot IP 연결 성공
[ ] FCI 통신 오류 없음
[ ] 7개 Joint 값 정상 출력
[ ] Robot mode 확인
[ ] Error state 없음
```

**기대 결과**

로봇은 움직이지 않고 Terminal에 Robot State가 출력됩니다.

---

#### Example 2 — Joint Position Control

**공식 파일**

```text
joint_position_example.py
```

**목적**

Python의 외부 control loop에서 7개 Joint의 목표 위치를 전달하여 Franka를 움직이는 기본 Joint Position Control 예제입니다.

**실행 예시**

```bash
python3 joint_position_example.py \
  --ip 172.16.0.2
```

**예제 내부 동작**

공식 예제는 대략 다음 흐름으로 동작합니다.

```text
Robot 연결
   ↓
Collision behavior 설정
   ↓
Joint Position Control 시작
   ↓
현재 Joint 상태 확인
   ↓
시간에 따라 Joint Position command 생성
   ↓
선택된 Joint를 부드럽게 이동
   ↓
Motion 종료
```

공식 설명상 이 예제는:

- Collision behavior를 설정
- Joint Position Control을 시작
- 외부 control loop에서 command를 생성
- 선택된 Joint를 이용해 단순 motion을 수행

합니다.

**핵심 개념**

Joint Position Control은 End-Effector의 XYZ를 직접 지정하는 것이 아니라 다음처럼 Joint 각도를 목표값으로 제어합니다.

```text
q = [q1, q2, q3, q4, q5, q6, q7]
```

즉,

```text
현재 Joint Position
        ↓
목표 Joint Position 생성
        ↓
Franka Controller
        ↓
7개 Joint 이동
```

구조입니다.

**실행 전 확인**

```text
[ ] Arm 주변 작업 공간 확보
[ ] Brake Open
[ ] FCI 활성화
[ ] 현재 자세가 Joint Limit 근처가 아님
[ ] Emergency Stop 사용 가능
```

**기대 결과**

로봇의 일부 Joint가 공식 예제에서 정의한 작은 trajectory를 따라 움직입니다.

> 이 예제는 실제 motion을 발생시키므로 처음 실행할 때는 반드시 로봇 가까이에서 상태를 확인하고 즉시 중지할 수 있도록 합니다.

---

#### Example 3 — Joint Impedance Control

**공식 파일**

```text
joint_impedance_example.py
```

**목적**

Joint Position을 강제로 정확히 따라가게 하는 방식이 아니라, Joint마다 **Spring-Damper 형태의 compliant control**을 적용하는 Joint Impedance Control 예제입니다.

**실행 예시**

```bash
python3 joint_impedance_example.py \
  --ip 172.16.0.2
```

**기본 개념**

Joint Impedance Controller는 개념적으로 다음과 같은 구조를 가집니다.

```text
목표 Joint Position
        ↓
현재 Joint Position과 차이 계산
        ↓
Spring 항
+
Joint Velocity 기반 Damping 항
        ↓
Joint Torque Command
```

따라서 로봇이 목표 자세를 향해 움직이면서도 Position Control보다 compliant한 동작을 만들 수 있습니다.

**공식 예제의 동작**

공식 문서 기준으로 다음과 같은 predefined joint configuration을 순서대로 이동합니다.

```text
Home Position
      ↓
Extended Forward Position
      ↓
Right Position
      ↓
Left Position
      ↓
Home Position
```

또한:

- Minimum-jerk trajectory generator 사용
- Spring-Damper 기반 Joint Impedance
- 각 자세 사이 dwell time 적용
- Coriolis compensation 사용

등의 구조를 포함합니다.

**이 예제로 공부할 부분**

```text
Joint Position Error
Joint Velocity
Stiffness
Damping
Coriolis Compensation
Torque Command
```

**기대 결과**

Arm이 여러 predefined Joint configuration 사이를 비교적 부드럽게 이동합니다.

---

#### Example 4 — Gripper Control

**공식 파일**

```text
move_gripper.py
```

**목적**

Franka Hand의 Homing, 현재 상태 읽기, Grasp, 성공 여부 확인, Release 과정을 확인합니다.

**실행 예시**

```bash
python3 move_gripper.py \
  --robot_ip 172.16.0.2 \
  --width 0.005 \
  --homing 1 \
  --speed 0.1 \
  --force 60
```

옵션 의미:

```text
--robot_ip   Robot IP
--width      잡을 물체의 목표 폭 [m]
--homing     Homing 수행 여부 (0 또는 1)
--speed      Gripper 이동 속도
--force      Grasp force [N]
```

위 예시에서:

```text
width = 0.005 m = 5 mm
force = 60 N
```

입니다.

**예제 내부 동작**

```text
Gripper 연결
    ↓
Homing
    ↓
Gripper State 읽기
    ↓
현재 Width 확인
    ↓
Grasp Command
    ↓
Grasp 성공 여부 확인
    ↓
Release
```

공식 예제가 표시하는 주요 Gripper State:

- Current width
- Maximum width
- Grasp status
- Temperature
- Timestamp

**주의**

`--width`는 물체의 실제 폭과 관계가 있으므로 물체 없이 임의로 큰 Force를 사용하지 않는 것이 좋습니다.

**기대 결과**

Gripper가 Homing 후 지정한 폭으로 닫히고, grasp 결과를 출력한 뒤 다시 release합니다.

---

#### Example 5 — Async Joint Position Control

**공식 파일**

```text
async_position_control.py
```

**목적**

Blocking control loop 대신 비동기 API를 이용하여 Joint Position setpoint를 전달하는 예제입니다.

**실행 예시**

```bash
python3 async_position_control.py \
  --ip 172.16.0.2
```

공식 문서에서는 약 `50 Hz`와 같은 비교적 낮은 rate에서 setpoint를 전달하는 사용 예를 설명합니다.

**개념 비교**

일반적인 active control:

```text
Control Loop 시작
    ↓
read/update/write
    ↓
다음 cycle
```

Async API:

```text
Application
    ↓
Joint Position Setpoint 전달
    ↓
다른 작업 수행 가능
    ↓
다음 Setpoint 전달
```

**이 예제로 확인할 것**

- Blocking control과 async control의 차이
- Low-rate command interface 사용법
- Joint Position setpoint 전송 방식

---

### 6.2 franka_ros2 Official Example Controllers

`franka_ros2`는 Franka의 공식 ROS 2 integration입니다.

현재 공식 저장소는 ROS 2 Humble을 기반으로 하며, 최근 버전에서는 여러 Example Controller를 **공통 launch 파일**로 실행하는 구조를 사용합니다.

기본 실행 형식:

```bash
ros2 launch franka_bringup example.launch.py \
  controller_name:=<controller_name>
```

또는 버전에 따라:

```bash
ros2 launch franka_bringup example.launch.py \
  controller_names:="<controller_name>"
```

실제 Robot IP, Robot Type, Namespace 등의 설정은:

```text
franka_bringup/config/franka.config.yaml
```

과 같은 공식 configuration 파일에서 설정합니다.

> `franka_ros2`는 변경이 빠른 프로젝트이므로 실제 실행 명령의 argument 이름은 설치된 버전의 README와 launch 파일을 우선 확인하세요.

---

#### Example 6 — Move to Start

**공식 Controller**

```text
move_to_start_example_controller
```

**목적**

다른 example controller를 실행하기 전에 Franka를 predefined start configuration으로 이동합니다.

**실행 개념**

```bash
ros2 launch franka_bringup example.launch.py \
  controller_name:=move_to_start_example_controller
```

**동작 흐름**

```text
현재 Joint Position 확인
        ↓
Start Joint Configuration 확인
        ↓
Trajectory 생성
        ↓
Start Pose로 이동
```

**왜 필요한가?**

Cartesian 또는 Impedance example은 특정 시작 자세를 가정할 수 있습니다.
따라서 예제 테스트 전 Start Position으로 이동하면 예상하지 못한 큰 움직임을 줄이는 데 도움이 됩니다.

---

#### Example 7 — Joint Position Example Controller

**공식 Controller**

```text
joint_position_example_controller
```

**목적**

ROS 2 `ros2_control` command interface를 이용하여 Joint Position Command를 전달하는 기본 예제입니다.

**구조**

```text
ROS 2 Controller
       ↓
Joint Position Command Interface
       ↓
franka_hardware
       ↓
libfranka / FCI
       ↓
Franka Arm
```

`pylibfranka`의 `joint_position_example.py`와 개념은 비슷하지만 ROS 2 Controller lifecycle과 hardware interface를 사용한다는 차이가 있습니다.

**확인하면 좋은 명령**

실행 중 Controller 상태:

```bash
ros2 control list_controllers
```

Hardware interface 확인:

```bash
ros2 control list_hardware_interfaces
```

---

#### Example 8 — Joint Impedance Example Controller

**공식 Controller**

```text
joint_impedance_example_controller
```

**목적**

ROS 2에서 Joint Impedance Control 구조를 확인하는 공식 예제입니다.

**핵심 입력**

```text
Joint Position
Joint Velocity
Robot Model
```

**Controller 출력**

```text
Joint Torque
```

Joint Position error와 velocity를 사용해 Spring-Damper 형태의 torque를 계산하는 구조를 이해하는 데 적합합니다.

---

#### Example 9 — Joint Impedance with IK

**공식 Controller**

```text
joint_impedance_with_ik_example_controller
```

**목적**

Cartesian 목표를 직접 Joint 목표로 입력하는 대신 **Inverse Kinematics(IK)** 를 이용해 목표 Joint configuration을 계산한 뒤 Joint Impedance Control과 결합합니다.

**전체 흐름**

```text
Target End-Effector Pose
          ↓
Inverse Kinematics
          ↓
Target Joint Position
          ↓
Joint Impedance Controller
          ↓
Joint Torque
          ↓
Franka Arm
```

이 예제는 이후 MoveIt, Cartesian manipulation, Visual Servoing 등을 이해할 때 중요한 구조입니다.

---

#### Example 10 — Gravity Compensation

**공식 Controller**

```text
gravity_compensation_example_controller
```

**목적**

로봇 자체 링크의 중력 영향을 보상하여 사용자가 Arm을 손으로 움직이기 쉬운 상태를 확인하는 예제입니다.

**개념**

```text
Robot Model
    ↓
Gravity Torque 계산
    ↓
Gravity Compensation
    ↓
Arm 자체 무게 영향 감소
```

실행하면 일반 Position Controller처럼 특정 위치로 이동시키는 것이 목적이 아니라, 외부에서 힘을 가했을 때 Arm이 비교적 쉽게 움직이는 상태를 확인하는 데 사용됩니다.

> 로봇이 자유롭게 움직일 수 있는 상태가 될 수 있으므로 주변 장애물과 사용자의 손 위치에 특히 주의해야 합니다.

---

#### Example 11 — Gripper Example Controller

**공식 Controller**

```text
gripper_example_controller
```

**목적**

ROS 2에서 Franka Hand를 제어하는 공식 예제입니다.

구조:

```text
ROS 2
 ↓
Gripper Controller / Action
 ↓
franka_gripper
 ↓
Franka Hand
```

ROS 2 환경에서 Arm 제어와 Gripper 제어를 함께 구성하기 전에 먼저 이 예제로 Gripper 통신을 검증하는 것이 좋습니다.

---

#### Example 12 — Cartesian Pose

**공식 Controller**

```text
cartesian_pose_example_controller
```

**목적**

7개 Joint 각도를 직접 지정하는 대신 End-Effector의 Cartesian pose를 command로 전달합니다.

Cartesian Pose는 일반적으로 다음으로 구성됩니다.

```text
Position
 ├─ X
 ├─ Y
 └─ Z

Orientation
 ├─ Rotation Matrix
 └─ Quaternion 등
```

**전체 흐름**

```text
Desired End-Effector Pose
            ↓
Cartesian Command Interface
            ↓
Franka Controller
            ↓
Arm Motion
```

이 예제는 Pick-and-Place, Visual Servoing, End-Effector path control을 이해하는 데 중요한 공식 예제입니다.

---

#### Example 13 — Cartesian Orientation

**공식 Controller**

```text
cartesian_orientation_example_controller
```

**목적**

End-Effector의 위치 이동보다 **orientation 변화**를 중심으로 Cartesian 제어를 확인합니다.

예를 들어 TCP의:

```text
Roll
Pitch
Yaw
```

와 관련된 자세 변화를 이해하는 데 도움이 됩니다.

---

#### Example 14 — Cartesian Elbow

**공식 Controller**

```text
cartesian_elbow_example_controller
```

**목적**

Franka처럼 7-DoF의 redundant robot에서 같은 End-Effector pose를 유지하면서도 여러 Joint configuration이 가능하다는 특성을 확인하는 예제입니다.

개념:

```text
같은 TCP Pose
     ↓
여러 가능한 Arm Configuration
     ↓
Elbow Configuration 선택
```

따라서 Cartesian Position만으로 결정되지 않는 **redundancy / elbow configuration**을 이해할 때 유용합니다.

---

### 6.3 ROS 2 Example 실행 전 확인 명령

Example Controller를 실행하기 전에 다음 명령으로 환경을 확인할 수 있습니다.

ROS 2 package 확인:

```bash
ros2 pkg list | grep franka
```

Controller 확인:

```bash
ros2 control list_controllers
```

Hardware Interface 확인:

```bash
ros2 control list_hardware_interfaces
```

Robot State 관련 Topic 확인:

```bash
ros2 topic list | grep -Ei "franka|joint|state"
```

실행 후 Controller가 `active` 상태인지 반드시 확인합니다.

---

### 6.4 Recommended Official Example Order

처음 Franka 공식 예제를 실제 로봇에서 확인한다면 아래 순서를 권장합니다.

```text
1. Network / Franka UI 확인
        ↓
2. print_robot_state.py
   └─ Robot motion 없음
        ↓
3. move_to_start_example_controller
        ↓
4. joint_position_example.py
   또는 joint_position_example_controller
        ↓
5. joint_impedance_example.py
   또는 joint_impedance_example_controller
        ↓
6. gravity_compensation_example_controller
        ↓
7. move_gripper.py
   또는 gripper_example_controller
        ↓
8. cartesian_orientation_example_controller
        ↓
9. cartesian_pose_example_controller
        ↓
10. joint_impedance_with_ik_example_controller
```

처음부터 Cartesian / IK 예제를 실행하기보다 **State → Joint → Impedance → Gripper → Cartesian → IK** 순서로 올라가는 것이 각 제어 방식의 차이를 이해하기 쉽습니다.

---

### 6.5 Example별 핵심 차이

**Robot State**

```text
Robot을 움직이지 않고 상태만 읽음
```

**Joint Position**

```text
목표 Joint Angle을 직접 제어
```

**Joint Impedance**

```text
Joint를 Spring-Damper처럼 compliant하게 제어
```

**Gravity Compensation**

```text
Robot 자체 무게를 보상하여 Hand-Guiding과 유사한 compliant 상태 확인
```

**Gripper**

```text
Franka Hand Open / Close / Grasp
```

**Cartesian Pose**

```text
Joint가 아닌 TCP Position + Orientation을 기준으로 제어
```

**IK + Impedance**

```text
TCP 목표
 ↓
IK
 ↓
Joint 목표
 ↓
Impedance Control
```

**Cartesian Elbow**

```text
같은 TCP Pose에서 7-DoF redundancy를 이용해 Elbow configuration을 다룸
```

---


## 7. Recommended First-Test Order

새 PC 또는 새로운 ROS 환경에서 Franka를 처음 연결할 때 권장 순서:

```text
Power ON
   ↓
PC ↔ Control Box Ethernet 연결
   ↓
PC IP = 172.16.0.1/24
   ↓
ping 172.16.0.2
   ↓
Franka UI 접속
   ↓
Error / Safety 상태 확인
   ↓
Brake / Joint Lock 상태 확인
   ↓
Robot State 읽기 테스트
   ↓
Activate FCI
   ↓
ROS / libfranka 연결 확인
   ↓
안전한 초기 자세 확인
   ↓
저속 Example Controller 테스트
   ↓
사용자 제어 프로그램 실행
```

---

## 8. Shutdown Procedure

작업이 끝난 뒤 바로 전원을 차단하지 않습니다.

1. ROS/FCI에서 실행 중인 motion controller를 정지합니다.
2. 로봇이 완전히 정지했는지 확인합니다.
3. 외부 제어가 종료되었는지 확인합니다.
4. Franka UI에서 오류가 없는지 확인합니다.
5. **Joint Lock / Brake를 잠금 상태로 전환합니다.**
6. Joint가 정상적으로 잠긴 것을 확인합니다.
7. Franka 시스템의 정상 종료 절차에 따라 전원을 끕니다.

> **중요:** 전원을 끄기 전에 로봇이 정지되어 있고 Joint/Brake가 안전한 상태인지 반드시 확인하세요.

---

## 9. Quick Reference

1. **Power ON**
2. PC IP를 `172.16.0.1/24`로 설정
3. `ping 172.16.0.2`로 연결 확인
4. Franka UI 접속
5. Error / Safety 상태 확인
6. Joint Lock / Brake 상태 확인
7. 다음 중 사용할 제어 방식 선택
   - Hand-Guiding
     - Translation
     - Rotation
     - Free Move
     - User-defined
   - External Control
     - Activate FCI
     - libfranka / ROS / ROS 2 실행
8. 작업 종료 후 Controller 정지
9. Joint Lock / Brake 잠금
10. **Power OFF**

---

## References

- Franka Robotics — Franka Research 3 Operating Manual
- Franka Robotics — Franka Research 3 Hardware/Product Manual
- Franka Robotics — FCI / Development documentation
- `frankarobotics/franka_ros2`
- `frankarobotics/libfranka`


---
