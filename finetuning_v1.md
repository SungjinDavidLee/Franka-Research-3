# Fine-tuning v1 — 첫 파인튜닝

실사 데이터 20 에피소드로 첫 파인튜닝을 시도했다.
**액션 예측이 전부 0으로 붕괴**해 실패했다.

---

## 데이터 수집

### 방식 선택

세 가지를 검토했다.

| 방식 | 장점 | 단점 |
|---|---|---|
| Kinesthetic teaching | 자연스러운 궤적 | gravity compensation 예제가 토크 0만 보내 팔이 처짐 |
| 키보드 jog | 팔 처짐 없음, 액션이 곧 정답 | 궤적이 축별로 분절됨 |
| 스크립트 자동 궤적 | 빠름 | 카메라-로봇 캘리브레이션 필요 (16mm 오차로 실패) |

**키보드 jog**를 택했다. `gravity_compensation_example_controller`가
모든 조인트에 토크 0만 보내는 구조라 팔이 자세를 유지하지 못했고,
카메라 캘리브레이션은 그리퍼 바운딩 박스가 흔들려 정밀도가 부족했다.

### 수집기

`task6/collect/scripts/jog_collect.py`

```
w/s   +x / -x        (전 / 후)
a/d   +y / -y        (좌 / 우, 로봇 기준)
r/f   +z / -z        (상 / 하)
g     그리퍼 토글
0     시작 자세 복귀
1/2/3 기록 시작 / 저장 / 폐기
```

키를 누르면 velocity 컨트롤러로 액션을 보내고,
같은 액션을 관측(RGB)과 함께 5Hz로 기록한다.

**액션 규약**

```
실행: velocity_mps = action[0:3] × 0.05
기록: action[1]의 부호를 뒤집어 OpenVLA 좌표계로 저장
      (Y_robot = -Y_OpenVLA)
```

시작 자세는 매 에피소드 동일하게 복귀시켰다.

```
TCP = (0.43323, 0.01636, 0.29787)
```

### 수집 결과

20 에피소드 (`ep_001` ~ `ep_020`)

| 항목 | 값 |
|---|---|
| 총 프레임 | 10,821 |
| 에피소드당 | 439 ~ 669 |
| 액션 있는 프레임 | 8,729 (81%) |
| grasp 위치 x | 0.482 ~ 0.747 |
| 좌우 배치 | 왼쪽 13 / 오른쪽 7 |

물체 배치는 매 에피소드 바꿨고, 타깃이 쿠키박스 오른쪽에 오는 경우도 섞었다.

---

## RLDS 변환

`task6/rlds/task6_franka/`

LIBERO 형식에 맞춰 TFDS 빌더를 작성했다.

```python
observation:
  image  (256, 256, 3) uint8     # third-person, square crop
  state  (8,) float32            # EEF xyz + rpy (6) + gripper (2)
action   (7,) float32            # xyz, rpy, gripper (1=open, 0=close)
language_instruction  string
```

**wrist 없이 등록**했다. OpenVLA는 이미지 한 장만 받으므로
`configs.py`에서 `"wrist": None`으로 설정했다.

```python
"task6_franka": {
    "image_obs_keys": {"primary": "image", "secondary": None, "wrist": None},
    "state_obs_keys": ["EEF_state", None, "gripper_state"],
    "state_encoding": StateEncoding.POS_EULER,
    "action_encoding": ActionEncoding.EEF_POS,
}
```

**gripper 부호 유지**를 위해 커스텀 transform을 만들었다.
LIBERO transform은 `invert_gripper_actions`로 뒤집는데,
우리 데이터는 이미 `1=OPEN, 0=CLOSE`이기 때문이다.

```python
def task6_franka_dataset_transform(trajectory):
    trajectory["observation"]["EEF_state"] = trajectory["observation"]["state"][:, :6]
    trajectory["observation"]["gripper_state"] = trajectory["observation"]["state"][:, -2:]
    return trajectory
```

결과: 20 examples, 842 MiB

---

## 학습 환경 구축

로컬 Titan RTX 24GB에서 시도했으나 두 가지 문제가 있었다.

| 문제 | 원인 | 대응 |
|---|---|---|
| `bfloat16` 미지원 | Turing 아키텍처 | fp16으로 변경 |
| OOM (batch 4) | 24GB 부족 | 서버로 이전 |

**RTX PRO 6000 Blackwell 96GB × 2** 서버로 옮겼다.
Blackwell은 bf16을 지원해 원본 코드를 그대로 쓸 수 있었다.

환경 구축 시 겪은 문제:

- `pip install -e .`가 torch를 2.2.0+cu121로 덮어써 Blackwell에서 동작 불가
  → cu128 빌드로 재설치
- tensorflow 2.15가 numpy 2.x에서 깨짐 → tf 2.21로 업그레이드
- `huggingface_hub` 1.x가 transformers 4.40과 충돌 → 0.36으로 다운그레이드
- `wandb`가 protobuf 충돌로 import 실패 → `finetune.py`에서 무력화
- `~/.cache/huggingface/hub`가 root 소유 → 소유권 변경

---

## 학습 설정

```bash
torchrun --standalone --nnodes 1 --nproc-per-node 1 vla-scripts/finetune.py \
  --vla_path openvla-7b-finetuned-libero-spatial \
  --dataset_name task6_franka \
  --batch_size 8 \
  --max_steps 5000 \
  --save_steps 1000 \
  --shuffle_buffer_size 5000 \
  --learning_rate 5e-4 \
  --use_lora True \
  --lora_rank 32
```

| 항목 | 값 |
|---|---|
| 학습 파라미터 | 110,828,288 / 7,652,065,472 (1.45%) |
| 소요 시간 | 학습 25분 + 체크포인트 저장 45분 |
| 체크포인트 | 1000, 2000, 3000, 4000, 5000 |

---

## 결과: 실패

### 액션이 전부 0

```
ACTION: [0. 0. 0. 0. 0. 0. 0.996078]  gripper= OPEN
```

정지 씬 20 샘플:

| 항목 | 값 |
|---|---|
| Y | 20/20 near_zero (0.000000) |
| xyz 평균 | [0.0, 0.0, 0.0] |
| gripper | OPEN 20 / CLOSE 0 |

### 생성 토큰 분석

```
생성 토큰: [31872, 31872, 31872, 31872, 31872, 31872, 31872]
```

7개 액션 차원에 **모두 동일한 토큰**이 나왔다.
`31872`는 OpenVLA 액션 이산화의 정확히 가운데 값,
즉 정규화 범위 [-1, 1]에서 0에 해당한다.

모델이 모든 축에 대해 "아무것도 하지 마"를 예측하고 있다.

1000 스텝 체크포인트도 동일했다. 과적합이 아니다.

---

## 원인 분석

### 액션 이산화 실패

학습 데이터의 액션 통계:

```
q01 : [-0.3, -0.3, -0.3, 0.0, 0.0, 0.0, 0.0]
q99 : [ 0.3,  0.3,  0.3, 0.0, 0.0, 0.0, 1.0]
```

에피소드 1개를 열어보니:

| 축 | 고유값 개수 |
|---|---|
| x | 2 |
| y | 2 |
| z | 3 |

**키보드 jog가 고정 크기 명령만 보냈기 때문**이다.
키를 누르면 `-0.3`, 떼면 `0`, 반대 방향이면 `+0.3`.
그 세 값밖에 없다.

OpenVLA는 액션을 **256단계로 이산화**해 토큰으로 바꾼다.
우리 데이터가 그중 3개만 쓰니 학습 신호가 사실상 없었다.

게다가 한 번에 한 축만 움직였으므로 나머지 두 축은 항상 0이었고,
전체적으로 0이 압도적 다수였다.

크로스엔트로피 손실 하에서 `-1`과 `+1`이 비슷한 빈도로 나오면,
그 사이 중앙값을 고르는 것이 손실을 줄이는 방향이 된다.

### 회전 축이 상수 0

7차원 중 3개(rx, ry, rz)가 정보량 0이었다.
모델이 "중앙 토큰을 내면 최소 3개는 맞다"를 학습한 셈이다.

### 정지 프레임 19%

액션이 완전히 0인 프레임이 2,092개(19%)였다.
0 예측이 보상받는 구조였다.

---

## 다음 단계

액션 기록 방식을 바꾸기로 했다.

**명령값 대신 실측 TCP delta로 역산**하면 연속적인 값이 나온다.
가속·감속 구간에서 0.1, 0.2, 0.28처럼 점진적인 값이 생기고
정지 직전엔 작아진다. 256단계를 제대로 활용할 수 있다.

→ [finetuning_v2.md](finetuning_v2.md)
