# OpenVLA Task6 실물 Franka 실험

LIBERO-Spatial Task6를 실제 Franka 로봇에서 수행하는 실험 기록.

```
Pick up the black bowl next to the cookie box and place it on the plate.
```

시뮬레이션에서 성공하는 OpenVLA 체크포인트가 실물에서는 실패하는 원인을
단계별로 규명하고, 실사 데이터 파인튜닝으로 개선한 과정을 담았다.

---

## 환경

| 항목 | 값 |
|---|---|
| 로봇 | Franka FER, ROS2 Jazzy |
| 카메라 | Intel RealSense D405 (third-person, 848×480) |
| 베이스 모델 | `openvla-7b-finetuned-libero-spatial` |
| 제어 | Cartesian velocity streaming (`k_position_scale_` = 0.05) |
| 학습 | LoRA r32, lr 5e-4, RTX PRO 6000 Blackwell 96GB |
| 수집 방식 | 키보드 jog teleoperation |

---

## 실험 목록

| 문서 | 데이터 | 핵심 변경 | 결과 |
|---|---|---|---|
| [00_baseline.md](00_baseline.md) | — | 파인튜닝 없이 평가 | 실패 — 원인 분석 |
| [finetuning_v1.md](finetuning_v1.md) | 20 ep / 10,821 frame | 첫 파인튜닝 | 실패 — 액션 전부 0 |
| [finetuning_v2.md](finetuning_v2.md) | 20 ep / 9,003 frame | 액션을 실측 TCP delta로 재계산 | 부분 성공 — 접근·하강 학습, grasp 실패 |
| [finetuning_v3.md](finetuning_v3.md) | 신규 20 ep / 8,700 frame | grasp 대기 구간 제거 | 개선 — grasp 예측 등장, 일반화 부족 |

---

## 단계별 성과 요약

| 항목 | baseline | v1 | v2 | v3 |
|---|---|---|---|---|
| 관측 반응 | 없음 (Y 항상 양수) | 없음 (전부 0) | **있음** | 있음 |
| 타깃 접근 | 실패 | 실패 | **성공** | 성공 |
| 하강 전환 | 실패 | 실패 | **성공** | 성공 |
| grasp (CLOSE) | 실패 | 실패 | 실패 | **부분 성공** |
| 들어올리기 | 실패 | 실패 | 실패 | 미검증 |
| 접시로 이송 | 실패 | 실패 | 실패 | 미검증 |

---

## 핵심 발견

### 1. 전처리 크롭 버그

`center_crop_90`이 크롭 후 **원본 크기(848×480)로 되돌리고** 있었다.
LIBERO 평가 코드가 정사각형 입력을 전제로 작성된 탓이다.
모델은 학습 분포와 다른 종횡비 이미지를 받고 있었다.

```python
# 수정 전 — 848×480으로 복원됨
image = image.resize((w, h), Image.Resampling.BILINEAR)

# 수정 후 — 중앙 정사각형 크롭 후 256×256
side = min(w, h)
image = image.crop((left, top, left + side, top + side))
image = image.resize((256, 256), Image.Resampling.BILINEAR)
```

### 2. 어댑터 Y flip 누락

`Y_robot = -Y_OpenVLA` 규약이 pose 컨트롤러에는 구현돼 있었으나
velocity 컨트롤러에는 없었다.

```cpp
openvla_cartesian_pose_controller.cpp:74        -action[1]   // 반전 있음
openvla_smooth_6dof_cartesian_pose_controller   -action[1]   // 반전 있음
openvla_cartesian_velocity_controller.cpp:66     action[1]   // 누락
```

컨트롤러에 반전을 넣으면 `return_to_trial_start`가 깨진다.
그 스크립트는 이미 로봇 좌표계로 계산된 명령을 보내기 때문이다.
**OpenVLA 액션을 다루는 rollout 층에서 반전**하도록 수정했다.

### 3. 액션 이산화 실패

키보드 jog는 고정 크기 명령(`-0.3`, `0`, `+0.3`)만 기록해
축당 고유값이 2~3개뿐이었다. OpenVLA는 액션을 256단계로 이산화하므로
학습 신호가 사실상 없었고, 모델은 중앙 토큰(=0)으로 수렴했다.

명령값 대신 **실측 TCP delta로 역산**하니 고유값이 140~208개로 늘었다.

```python
action[0:3] = (dTCP / dt) / k_position_scale_
```

### 4. grasp 라벨 모호성

하강 완료 후 수 초간 정지한 뒤 그리퍼를 닫으면,
**같은 관측에 OPEN과 CLOSE가 모두 정답**으로 붙는다.
모델이 이 구간을 학습할 방법이 없다.

정지와 파지를 한 키(`h`)로 묶어 대기 구간을 제거했다.

| | 기존 20 ep | 신규 20 ep |
|---|---|---|
| CLOSE 직전 정지 프레임 | 평균 8.7 (최대 18) | 평균 0.0 |

### 5. sim-to-real 갭 확인

동일 checkpoint가 LIBERO 시뮬에서는 Task6를 성공한다.
모델 능력의 한계가 아니라 관측 도메인 차이가 원인임이 확정됐다.

---

## 남은 문제

**grasp 타이밍의 일반화.** v3에서 CLOSE 예측이 나오기 시작했으나
특정 물체 배치에서만 작동한다. 위치를 옮기면 하강만 계속한다.

원인 후보:

- **데이터 부족** — 20개로는 다양한 위치의 grasp 시점을 일반화하기 어려움
- **third-person 관측의 한계** — grasp 순간 로봇 팔이 타깃 그릇을 가림.
  깊이 판단이 픽셀 몇 개 차이로 나타남

다음 단계로 데이터 40개 확장(v4)과 wrist camera 도입을 검토 중이다.

---

## 디렉토리 구조

```
task6/
├── active/                    rollout, writer, 복귀 스크립트
│   ├── task6_rollout_velocity_streaming.py
│   ├── task6_openvla_writer.py
│   └── task6_return_trial_start.py
├── collect/
│   ├── scripts/jog_collect.py 키보드 jog 수집기
│   └── episodes/              ep_001 ~ ep_040
├── rlds/                      RLDS 빌더 (v1 ~ v4)
├── docs/                      실험 문서
└── FINDINGS.md                원본 실험 로그
```

## 실행 순서

```bash
# 1. 로봇
ros2 launch franka_bringup franka.launch.py \
  robot_type:=fer robot_ip:=172.16.0.2 load_gripper:=true \
  load_d405:=false use_fake_hardware:=false

# 2. 카메라
python3 d405_live_writer.py

# 3. 컨트롤러
./task6/collect/scripts/to_rollout.sh

# 4. 추론
python3 task6/task6_openvla_writer_ft_v3.py

# 5. 실행
python3 task6/active/task6_rollout_velocity_streaming.py
```
