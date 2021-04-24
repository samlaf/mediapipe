bazel build -c opt --define MEDIAPIPE_DISABLE_GPU=1 mediapipe/examples/desktop/face_detection:face_detection_cpu \
&& \
GLOG_logtostderr=1 bazel-bin/mediapipe/examples/desktop/face_detection/face_detection_cpu \
--calculator_graph_config_file=mediapipe/graphs/face_detection/face_detection_desktop_live.pbtxt