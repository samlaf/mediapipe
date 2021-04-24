// This takes two images as input and concatenates them to play side-by-side

#include "mediapipe/framework/calculator_framework.h"

#include "mediapipe/framework/formats/image_frame.h" //ImageFrame
#include "mediapipe/framework/port/opencv_imgproc_inc.h"
#include "mediapipe/framework/formats/image_frame_opencv.h" //formats
#include <opencv2/opencv.hpp>

# define PRINT(x) std::cout << x << std::endl

namespace mediapipe {

// Example config:
// node {
//   calculator: "VideoMultiplexer"
//   input_stream: "IMAGE:0:image0"
//   input_stream: "IMAGE:1:image1"
//   output_stream: "IMAGE:concat_image"
// }
//
class VideoMultiplexer : public CalculatorBase {

public:
  static absl::Status GetContract(CalculatorContract* cc) {
    cc->Inputs().Get("IMAGE", 0).Set<ImageFrame>();
    cc->Inputs().Get("IMAGE", 1).Set<ImageFrame>();
    cc->Outputs().Tag("IMAGE").Set<ImageFrame>();

    return absl::OkStatus();
  }

  absl::Status Process(CalculatorContext* cc) final {
    // Resize an ImageFrame:
    const ImageFrame& imgframe1 = cc->Inputs().Get("IMAGE",0).Get<ImageFrame>();
    const ImageFrame& imgframe2 = cc->Inputs().Get("IMAGE",1).Get<ImageFrame>();
    cv::Mat img1 = formats::MatView(&imgframe1);
    cv::Mat img2 = formats::MatView(&imgframe2);

    std::unique_ptr<ImageFrame> outimgfp = std::make_unique<ImageFrame>(imgframe1.Format(),
                                            imgframe1.Width() + imgframe2.Width(),
                                            imgframe1.Height());
    cv::Mat outimg = formats::MatView(outimgfp.get());
    cv::hconcat(img1, img2, outimg);
    
    cc->Outputs().Tag("IMAGE").Add(outimgfp.release(), cc->InputTimestamp());
    return absl::OkStatus();
  }

};

REGISTER_CALCULATOR(VideoMultiplexer);
}  // namespace mediapipe

