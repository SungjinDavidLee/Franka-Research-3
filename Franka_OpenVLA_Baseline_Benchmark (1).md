# 실물 Franka 환경에서의 OpenVLA Baseline Benchmark

## 1. Benchmark 개요

본 Benchmark는 OpenVLA를 실물 Franka Manipulator에 적용했을 때의 기본
Manipulation 수행 성능을 분석하기 위해 수행하였다.

평가 Task는 공간 지시를 기반으로 목표인 검은색 그릇을 선택하고, 해당
그릇을 파지하여 접시 위에 배치하는 Pick-and-Place 작업이다.

전체 Manipulation 과정을 S1\~S10의 10개 단계로 구분하여 OpenVLA가 실제
로봇 환경에서 어느 단계까지 수행하는지 평가하였다. Baseline에는 별도의
Perception 보정, 객체 Segmentation, Action Smoothing 등의 성능 개선
방법을 적용하지 않았다.

본 결과는 이후 적용되는 성능 개선 방법과 비교하기 위한 Baseline
Benchmark로 사용한다.

------------------------------------------------------------------------

## 2. 단계별 평가 기준

```{=html}
<table>
```
```{=html}
<thead>
```
```{=html}
<tr>
```
```{=html}
<th align="center">
```
단계
```{=html}
</th>
```
```{=html}
<th align="left">
```
평가 항목
```{=html}
</th>
```
```{=html}
<th align="left">
```
성공 기준
```{=html}
</th>
```
```{=html}
</tr>
```
```{=html}
</thead>
```
```{=html}
<tbody>
```
```{=html}
<tr>
```
```{=html}
<td align="center">
```
S1
```{=html}
</td>
```
```{=html}
<td>
```
목표 물체 선택
```{=html}
</td>
```
```{=html}
<td>
```
언어 지시에서 지정된 목표 물체를 올바르게 선택하고 해당 방향으로 이동을
생성
```{=html}
</td>
```
```{=html}
</tr>
```
```{=html}
<tr>
```
```{=html}
<td align="center">
```
S2
```{=html}
</td>
```
```{=html}
<td>
```
목표 물체 접근
```{=html}
</td>
```
```{=html}
<td>
```
End-Effector가 목표 물체의 파지 가능한 접근 영역까지 도달
```{=html}
</td>
```
```{=html}
</tr>
```
```{=html}
<tr>
```
```{=html}
<td align="center">
```
S3
```{=html}
</td>
```
```{=html}
<td>
```
파지 전 자세 정렬
```{=html}
</td>
```
```{=html}
<td>
```
목표 물체를 파지할 수 있도록 End-Effector의 위치와 자세를 정렬
```{=html}
</td>
```
```{=html}
</tr>
```
```{=html}
<tr>
```
```{=html}
<td align="center">
```
S4
```{=html}
</td>
```
```{=html}
<td>
```
그리퍼 진입 및 접촉
```{=html}
</td>
```
```{=html}
<td>
```
목표 물체가 그리퍼 사이에 위치하고 유효한 접촉 발생
```{=html}
</td>
```
```{=html}
</tr>
```
```{=html}
<tr>
```
```{=html}
<td align="center">
```
S5
```{=html}
</td>
```
```{=html}
<td>
```
안정적 파지
```{=html}
</td>
```
```{=html}
<td>
```
그리퍼 폐쇄 후 목표 물체의 파지 상태를 안정적으로 유지
```{=html}
</td>
```
```{=html}
</tr>
```
```{=html}
<tr>
```
```{=html}
<td align="center">
```
S6
```{=html}
</td>
```
```{=html}
<td>
```
물체 들어 올리기
```{=html}
</td>
```
```{=html}
<td>
```
파지된 물체를 지지면에서 분리하여 안정적으로 상승
```{=html}
</td>
```
```{=html}
</tr>
```
```{=html}
<tr>
```
```{=html}
<td align="center">
```
S7
```{=html}
</td>
```
```{=html}
<td>
```
초기 영역 이탈
```{=html}
</td>
```
```{=html}
<td>
```
물체를 파지한 상태로 주변과 충돌 없이 초기 영역에서 이탈
```{=html}
</td>
```
```{=html}
</tr>
```
```{=html}
<tr>
```
```{=html}
<td align="center">
```
S8
```{=html}
</td>
```
```{=html}
<td>
```
목표 위치 이송
```{=html}
</td>
```
```{=html}
<td>
```
파지 상태를 유지하며 목표인 접시 영역까지 물체를 이동
```{=html}
</td>
```
```{=html}
</tr>
```
```{=html}
<tr>
```
```{=html}
<td align="center">
```
S9
```{=html}
</td>
```
```{=html}
<td>
```
접시 위 정렬 및 하강
```{=html}
</td>
```
```{=html}
<td>
```
물체를 접시의 유효 영역에 정렬한 후 안정적으로 하강
```{=html}
</td>
```
```{=html}
</tr>
```
```{=html}
<tr>
```
```{=html}
<td align="center">
```
S10
```{=html}
</td>
```
```{=html}
<td>
```
그리퍼 해제 및 최종 배치
```{=html}
</td>
```
```{=html}
<td>
```
그리퍼 해제 후 물체가 접시 위에 안정적으로 배치
```{=html}
</td>
```
```{=html}
</tr>
```
```{=html}
</tbody>
```
```{=html}
</table>
```

------------------------------------------------------------------------

## 3. OpenVLA Baseline 단계별 결과

```{=html}
<table>
```
```{=html}
<thead>
```
```{=html}
<tr>
```
```{=html}
<th align="center">
```
단계
```{=html}
</th>
```
```{=html}
<th align="left">
```
평가 항목
```{=html}
</th>
```
```{=html}
<th align="center">
```
결과
```{=html}
</th>
```
```{=html}
<th align="left">
```
주요 관찰
```{=html}
</th>
```
```{=html}
</tr>
```
```{=html}
</thead>
```
```{=html}
<tbody>
```
```{=html}
<tr>
```
```{=html}
<td align="center">
```
S1
```{=html}
</td>
```
```{=html}
<td>
```
목표 물체 선택
```{=html}
</td>
```
```{=html}
<td align="center">
```
성공
```{=html}
</td>
```
```{=html}
<td>
```
검은색 그릇 방향으로 초기 End-Effector 이동 생성
```{=html}
</td>
```
```{=html}
</tr>
```
```{=html}
<tr>
```
```{=html}
<td align="center">
```
S2
```{=html}
</td>
```
```{=html}
<td>
```
목표 물체 접근
```{=html}
</td>
```
```{=html}
<td align="center">
```
실패
```{=html}
</td>
```
```{=html}
<td>
```
목표를 향해 전진 및 하강하였으나 파지 가능 위치 도달 전 동작 종료
```{=html}
</td>
```
```{=html}
</tr>
```
```{=html}
<tr>
```
```{=html}
<td align="center">
```
S3
```{=html}
</td>
```
```{=html}
<td>
```
파지 전 자세 정렬
```{=html}
</td>
```
```{=html}
<td align="center">
```
\-
```{=html}
</td>
```
```{=html}
<td>
```
S2 실패로 미수행
```{=html}
</td>
```
```{=html}
</tr>
```
```{=html}
<tr>
```
```{=html}
<td align="center">
```
S4
```{=html}
</td>
```
```{=html}
<td>
```
그리퍼 진입 및 접촉
```{=html}
</td>
```
```{=html}
<td align="center">
```
\-
```{=html}
</td>
```
```{=html}
<td>
```
S2 실패로 미수행
```{=html}
</td>
```
```{=html}
</tr>
```
```{=html}
<tr>
```
```{=html}
<td align="center">
```
S5
```{=html}
</td>
```
```{=html}
<td>
```
안정적 파지
```{=html}
</td>
```
```{=html}
<td align="center">
```
\-
```{=html}
</td>
```
```{=html}
<td>
```
S2 실패로 미수행
```{=html}
</td>
```
```{=html}
</tr>
```
```{=html}
<tr>
```
```{=html}
<td align="center">
```
S6
```{=html}
</td>
```
```{=html}
<td>
```
물체 들어 올리기
```{=html}
</td>
```
```{=html}
<td align="center">
```
\-
```{=html}
</td>
```
```{=html}
<td>
```
S2 실패로 미수행
```{=html}
</td>
```
```{=html}
</tr>
```
```{=html}
<tr>
```
```{=html}
<td align="center">
```
S7
```{=html}
</td>
```
```{=html}
<td>
```
초기 영역 이탈
```{=html}
</td>
```
```{=html}
<td align="center">
```
\-
```{=html}
</td>
```
```{=html}
<td>
```
S2 실패로 미수행
```{=html}
</td>
```
```{=html}
</tr>
```
```{=html}
<tr>
```
```{=html}
<td align="center">
```
S8
```{=html}
</td>
```
```{=html}
<td>
```
목표 위치 이송
```{=html}
</td>
```
```{=html}
<td align="center">
```
\-
```{=html}
</td>
```
```{=html}
<td>
```
S2 실패로 미수행
```{=html}
</td>
```
```{=html}
</tr>
```
```{=html}
<tr>
```
```{=html}
<td align="center">
```
S9
```{=html}
</td>
```
```{=html}
<td>
```
접시 위 정렬 및 하강
```{=html}
</td>
```
```{=html}
<td align="center">
```
\-
```{=html}
</td>
```
```{=html}
<td>
```
S2 실패로 미수행
```{=html}
</td>
```
```{=html}
</tr>
```
```{=html}
<tr>
```
```{=html}
<td align="center">
```
S10
```{=html}
</td>
```
```{=html}
<td>
```
그리퍼 해제 및 최종 배치
```{=html}
</td>
```
```{=html}
<td align="center">
```
\-
```{=html}
</td>
```
```{=html}
<td>
```
S2 실패로 미수행
```{=html}
</td>
```
```{=html}
</tr>
```
```{=html}
</tbody>
```
```{=html}
</table>
```
> `-`는 선행 단계 실패로 인해 해당 단계가 수행되지 않았음을 의미한다.

------------------------------------------------------------------------

## 4. Baseline 결과 요약

```{=html}
<table>
```
```{=html}
<thead>
```
```{=html}
<tr>
```
```{=html}
<th align="left">
```
평가 항목
```{=html}
</th>
```
```{=html}
<th align="left">
```
결과
```{=html}
</th>
```
```{=html}
</tr>
```
```{=html}
</thead>
```
```{=html}
<tbody>
```
```{=html}
<tr>
```
```{=html}
<td>
```
VLA 모델
```{=html}
</td>
```
```{=html}
<td>
```
OpenVLA
```{=html}
</td>
```
```{=html}
</tr>
```
```{=html}
<tr>
```
```{=html}
<td>
```
로봇 플랫폼
```{=html}
</td>
```
```{=html}
<td>
```
Franka Manipulator
```{=html}
</td>
```
```{=html}
</tr>
```
```{=html}
<tr>
```
```{=html}
<td>
```
평가 환경
```{=html}
</td>
```
```{=html}
<td>
```
실물 로봇 환경
```{=html}
</td>
```
```{=html}
</tr>
```
```{=html}
<tr>
```
```{=html}
<td>
```
성공한 최종 단계
```{=html}
</td>
```
```{=html}
<td>
```
S1
```{=html}
</td>
```
```{=html}
</tr>
```
```{=html}
<tr>
```
```{=html}
<td>
```
최초 실패 단계
```{=html}
</td>
```
```{=html}
<td>
```
S2 - 목표 물체 접근
```{=html}
</td>
```
```{=html}
</tr>
```
```{=html}
<tr>
```
```{=html}
<td>
```
실패 유형
```{=html}
</td>
```
```{=html}
<td>
```
불완전 접근 (Incomplete Approach)
```{=html}
</td>
```
```{=html}
</tr>
```
```{=html}
<tr>
```
```{=html}
<td>
```
전체 Task 결과
```{=html}
</td>
```
```{=html}
<td>
```
실패
```{=html}
</td>
```
```{=html}
</tr>
```
```{=html}
</tbody>
```
```{=html}
</table>
```

------------------------------------------------------------------------

## 5. 결과 분석

OpenVLA Baseline은 S1에서 언어 명령으로 지정된 검은색 그릇 방향으로
End-Effector의 초기 이동을 생성하였다. 따라서 목표 물체를 선택하고 해당
방향으로 이동을 시작하는 단계는 성공한 것으로 판단하였다.

S2에서는 End-Effector가 목표 검은색 그릇을 향해 전진하면서 하강하였다.
그러나 실제로 그릇을 파지할 수 있는 접근 위치까지 도달하지 못한 상태에서
동작이 종료되었다. 이에 따라 S2를 최초 실패 단계로 판정하였으며, 실패
유형을 불완전 접근(Incomplete Approach)으로 분류하였다.

S2가 완료되지 않았기 때문에 S3\~S10의 파지, 들어 올리기, 이송 및 배치
과정은 수행되지 않았다.

------------------------------------------------------------------------

## 6. 결론

실물 Franka 환경에서 OpenVLA Baseline을 평가한 결과, 목표 물체
방향으로의 초기 이동은 생성되었으나 실제 파지가 가능한 위치까지 충분히
접근하지 못하였다.

따라서 Baseline의 주요 병목 지점은 목표 물체 선택 이후 파지가 가능한
접근 영역까지 이동하는 S2 단계로 분석하였다.

본 결과를 Baseline 기준으로 사용하며, 이후 성능 개선 방법에도 동일한
S1\~S10 평가 기준을 적용하여 각 방법이 Manipulation 수행 과정의 어느
단계까지 개선되는지 비교한다.
