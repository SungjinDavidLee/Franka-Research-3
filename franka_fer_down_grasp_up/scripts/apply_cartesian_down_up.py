#!/usr/bin/env python3
from pathlib import Path
import sys
import shutil

if len(sys.argv) != 2:
    raise SystemExit("Usage: apply_cartesian_down_up.py <cartesian_pose_example_controller.cpp>")

p = Path(sys.argv[1]).expanduser().resolve()
if not p.exists():
    raise SystemExit(f"ERROR: file not found: {p}")

backup = p.with_suffix(p.suffix + ".bak_down_grasp_up")
if not backup.exists():
    shutil.copy2(p, backup)
    print(f"Backup created: {backup}")

text = p.read_text()
markers = [
    "  double radius = 0.1;",
    "  // One smooth vertical round trip:",
    "  // Smooth vertical demo:",
]
start = None
for marker in markers:
    if marker in text:
        start = text.index(marker)
        break
if start is None:
    raise SystemExit("ERROR: known trajectory block not found")

end = text.index("  Eigen::Quaterniond new_orientation;", start)
new = '''  // Smooth vertical demo:
  // 0~3 s : 200 mm downward
  // 3~8 s : hold bottom pose
  // 8~11 s: return to the exact start pose
  // >11 s : hold start pose
  const double depth = 0.20;
  const double down_time = 3.0;
  const double hold_time = 5.0;
  const double up_time = 3.0;

  double delta_z = 0.0;

  if (elapsed_time_ <= down_time) {
    delta_z =
        -0.5 * depth *
        (1.0 - std::cos(M_PI * elapsed_time_ / down_time));
  } else if (elapsed_time_ <= down_time + hold_time) {
    delta_z = -depth;
  } else if (elapsed_time_ <= down_time + hold_time + up_time) {
    const double t = elapsed_time_ - down_time - hold_time;
    delta_z =
        -0.5 * depth *
        (1.0 + std::cos(M_PI * t / up_time));
  } else {
    delta_z = 0.0;
  }

'''
text = text[:start] + new + text[end:]

if "new_position(2) += delta_z;" not in text:
    old = """  new_position(0) -= delta_x;
  new_position(2) -= delta_z;
"""
    replacement = """  // Base-frame Z: negative direction = downward
  new_position(2) += delta_z;
"""
    if old not in text:
        raise SystemExit("ERROR: Cartesian position update block not found")
    text = text.replace(old, replacement, 1)

p.write_text(text)
print("Applied 200 mm DOWN -> 5 s HOLD -> UP trajectory")
