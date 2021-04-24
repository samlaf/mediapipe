# Copyright 2021 Orangead Media

load(
    "//mediapipe/framework/tool:mediapipe_graph.bzl",
    "mediapipe_simple_subgraph",
)

######## Meta-graph which runs 2 subgraphs in parallel ###
######## and displays their outputs side-by-side       ###
# face_detection_vs_tracking_desktop_live.pbtxt
cc_binary(
    name = "face_detection_vs_tracking_desktop_live",
    deps = [
        "//mediapipe/examples/desktop:demo_run_graph_main",
        "//mediapipe/calculators/core:pass_through_calculator",
        "//orangead/calculators:video_mux",
        ":face_detection_desktop_live_subgraph",
        ":face_detection_tracking_desktop_live_subgraph"
    ]
)
mediapipe_simple_subgraph(
    name = "face_detection_desktop_live_subgraph", # used in bazel BUILD files
    graph = "//mediapipe/graphs/face_detection:face_detection_desktop_live.pbtxt",
    register_as = "FaceDetectionDesktopLiveSubgraph", # used in supergraph .pbtxt files
    deps = [
        "//mediapipe/calculators/core:flow_limiter_calculator",
        "//mediapipe/modules/face_detection:face_detection_front_cpu",
        "//mediapipe/calculators/util:annotation_overlay_calculator",
        "//mediapipe/calculators/util:detections_to_render_data_calculator",
    ],
)
mediapipe_simple_subgraph(
    name = "face_detection_tracking_desktop_live_subgraph",
    graph = "face_detection_tracking_desktop_live.pbtxt",
    register_as = "FaceDetectionTrackingDesktopLiveSubgraph",
    deps = [
        "//mediapipe/calculators/core:packet_resampler_calculator",
        "//mediapipe/modules/face_detection:face_detection_front_cpu",
        "//mediapipe/graphs/tracking/subgraphs:object_tracking_cpu",
        "//mediapipe/graphs/tracking/subgraphs:renderer_cpu",
    ],
)
###########################################


### Not sure if this is the right way to do it... compare with holistic face tracking!
# face_detection_tracking_desktop_live.pbtxt
cc_binary(
    name = "face_detection_tracking_desktop_live",
    deps = [
        # main file: source code
        "//mediapipe/examples/desktop:demo_run_graph_main",
        # calculators and subgraphs
        "//mediapipe/calculators/core:packet_resampler_calculator",
        "//mediapipe/modules/face_detection:face_detection_front_cpu",
        "//mediapipe/graphs/tracking/subgraphs:object_tracking_cpu",
        "//mediapipe/graphs/tracking/subgraphs:renderer_cpu",
    ],
)