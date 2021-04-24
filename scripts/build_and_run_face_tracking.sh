bazel build -c opt --define MEDIAPIPE_DISABLE_GPU=1 orangead:face_detection_tracking_desktop_live \
&& \
GLOG_logtostderr=1 bazel-bin/orangead/face_detection_tracking_desktop_live \
--calculator_graph_config_file=orangead/face_detection_tracking_desktop_live.pbtxt