#!/bin/bash

if [[ $1 == "cpu" ]]; then
    echo "Running on CPU"
    sleep 1
    bazel build -c opt --define MEDIAPIPE_DISABLE_GPU=1 mediapipe/examples/desktop/face_detection:face_detection_cpu \
    && \
    GLOG_logtostderr=1 bazel-bin/mediapipe/examples/desktop/face_detection/face_detection_cpu \
    --calculator_graph_config_file=mediapipe/graphs/face_detection/face_detection_desktop_live.pbtxt
else
    echo "Running on GPU"
    sleep 1
    bazel build -c opt --copt -DMESA_EGL_NO_X11_HEADERS --copt -DEGL_NO_X11 mediapipe/examples/desktop/face_detection:face_detection_gpu \
    && \
    GLOG_logtostderr=1 bazel-bin/mediapipe/examples/desktop/face_detection/face_detection_gpu \
    --calculator_graph_config_file=mediapipe/graphs/face_detection/face_detection_mobile_gpu.pbtxt
fi
