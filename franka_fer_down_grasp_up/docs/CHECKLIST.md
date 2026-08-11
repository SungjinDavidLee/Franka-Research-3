# Pre-run checklist

- [ ] `enp3s0` = `172.16.0.1/24`
- [ ] `ping 172.16.0.2` packet loss 0%
- [ ] Franka hardware = `active`
- [ ] `joint_state_broadcaster` = `active`
- [ ] `franka_robot_state_broadcaster` = `active`
- [ ] `cartesian_pose_example_controller` = `inactive`
- [ ] `/fer_gripper/franka_gripper/*` actions visible
- [ ] `current_errors` all false
- [ ] TCP 아래 200 mm + tool/finger 공간 확보
- [ ] E-stop 접근 가능
- [ ] 사람/장애물 없음
