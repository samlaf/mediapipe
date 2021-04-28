#!/bin/bash

if [[ $1 == "cpu" ]]; then
    echo "Running on CPU"
    sleep 1
    GLOG_logtostderr=1 bazel-bin/mediapipe/examples/desktop/face_detection/face_detection_cpu \
    --calculator_graph_config_file=mediapipe/graphs/face_detection/face_detection_desktop_live.pbtxt
else
    echo "Running on GPU"
    sleep 1
    GLOG_logtostderr=1 bazel-bin/mediapipe/examples/desktop/face_detection/face_detection_gpu \
    --calculator_graph_config_file=mediapipe/graphs/face_detection/face_detection_mobile_gpu.pbtxt
fi