# Script to automate the process of building and running examples
# See https://google.github.io/mediapipe/getting_started/cpp.html to see how complicated the commands are

import argparse
import subprocess
import os

parser = argparse.ArgumentParser()
parser.add_argument("-e", "--example", type=str, choices=["detection", "tracking"],
                    help="Example to run.", required=True)
parser.add_argument("-m", "--model", type=str, choices=["back", "front"],
                    help="Model to use. (default: back)", default="back")
parser.add_argument("--cpu", action='store_true', default=False,
                    help="By default, model runs on gpu. Add this flag to run on cpu instead.")
parser.add_argument("--build", action='store_true', default=False,
                    help="Build example before running. The way mediapipe is built, can't have cached both cpu and gpu versions, so we can't just \
                            call bazel build, it will recompile many many files when switching from cpu to gpu or vice versa.")

args = parser.parse_args()

##################### Data structures and helper functions ########################
targets = {
    "detection_front_cpu": "mediapipe/examples/desktop/face_detection:face_detection_cpu",
    "detection_front_gpu": "mediapipe/examples/desktop/face_detection:face_detection_gpu",
    "detection_back_cpu": "mediapipe/examples/desktop/face_detection:face_detection_back_cpu",
    "detection_back_gpu": "mediapipe/examples/desktop/face_detection:face_detection_back_gpu",
}

def get_target(example, model, cpu: bool, build: bool):
    if example == "detection":
        example_name = "face_detection"
    else: #tracking
        raise NotImplementedError
    model_name = "_back" if model=="back" else ""
    cpu_or_gpu = "cpu" if cpu else "gpu"
    if build:
        target = f"mediapipe/examples/desktop/{example_name}:{example_name}{model_name}_{cpu_or_gpu}"
    else:
        target = f"bazel-bin/mediapipe/examples/desktop/{example_name}/{example_name}{model_name}_{cpu_or_gpu}"
    return target

graphs = {
    "detection": {
        "front": {
            True: "mediapipe/graphs/face_detection/face_detection_desktop_live.pbtxt",
            False: "mediapipe/graphs/face_detection/face_detection_mobile_gpu.pbtxt"
        },
        "back": {
            True: "mediapipe/graphs/face_detection/face_detection_back_desktop_live.pbtxt",
            False: "mediapipe/graphs/face_detection/face_detection_back_mobile_gpu.pbtxt"
        }
    }
}

def get_build_flags(use_cpu):
    if use_cpu:
        return ["--define", "MEDIAPIPE_DISABLE_GPU=1"]
    else:
        return ["--copt", "-DMESA_EGL_NO_X11_HEADERS", "--copt", "-DEGL_NO_X11"]

################################### Build and Run #############################################

### Example command:
###  bazel build -c opt --copt -DMESA_EGL_NO_X11_HEADERS --copt -DEGL_NO_X11 \
###  mediapipe/examples/desktop/hand_tracking:hand_tracking_gpu
if args.build:
    cmd = ["bazel", "build", "-c", "opt"] + get_build_flags(args.cpu) + [get_target(args.example, args.model, args.cpu, args.build)]
    subprocess.run(cmd)

### Example command:
###  GLOG_logtostderr=1 bazel-bin/mediapipe/examples/desktop/hand_tracking/hand_tracking_gpu \
###  --calculator_graph_config_file=mediapipe/graphs/hand_tracking/hand_tracking_mobile.pbtxt
if args.example == "detection":
    cmd = [get_target(args.example, args.model, args.cpu, False)] + ["--calculator_graph_config_file={}".format(graphs[args.example][args.model][args.cpu])]
    my_env = os.environ.copy()
    my_env["GLOG_logtostderr"] = "1"
    subprocess.run(cmd, env=my_env)
