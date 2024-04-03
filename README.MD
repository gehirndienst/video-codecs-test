## Video-Codecs-Test
This is a simple project to test the video codecs made in Python. The project uses GStreamer pipelines to test the video codecs imitating the real-time communciation so that where possible there are options for minimizing latency or setting the real-time preset for the selected encoder. Also the bitrate is fixed to 2Mbps for all the codecs. 

As input file the project uses the Big Buck Bunny video file. The video file is available in different resolutions and formats. The project uses the 720p version of the input file. Then each GStreamer pipeline is tested and the output is saved in a matroska muxed container (.mkv). 

The output file is then compared with the original video file to check the quality of the video. I use three popular metrics to compare the video files: PSNR, SSIM and VMAF. The project uses the FFmpeg library to calculate the metrics.

The project is divided into two parts:
- The first part is the GStreamer pipelines to test the video codecs. It measures the encoding time and the encoded file size.
- The second part is the FFmpeg commands to calculate the metrics. It calculates the PSNR, SSIM and VMAF values for the encoded video files.

The project tests the following video codecs with corresponding GStreamer encoding plugins:
- H.264
- H.265
- VP8
- VP9
- AV1
- H264 hardware accelerated (NVENC)
- H265 hardware accelerated (NVENC)

As an output the project saves the intermediate logs and the final results. The results include the text file with encoding time and the encoded file size, and the plot with the PSNR, SSIM and VMAF values for each codec.

## Requirements
1) Some input video file. The project uses the Big Buck Bunny video file.
2) Python >= 3.10
3) H264, H265, VP8, VP9, AV1 codecs built to install appropriate GStreamer plugins.
4) CUDA support for the NVENC hardware encoders (optional)
5) VMAF library built
6) GStreamer >= 1.22
7) FFmpeg >= 5.0 built with --enable-libvmaf

For steps 3-6 you can refer to the Dockerfile from [my other repository](https://github.com/gehirndienst/gstwebrtcapp/blob/main/docker/Dockerfile-cuda)

For step 7 refer [to this guide](https://ottverse.com/vmaf-ffmpeg-ubuntu-compilation-installation-usage-guide/)

## Usage
Specify needed paths in the `encoding_test.py`, namely the input video file path, the path to the VMAF model and the path to save the intermediate logs. If you do not have NVIDIA hardware, comment out the hardware encoding pipelines in the list at the beginning of `encoding_test.py` file. Then run the script.

## Results
The results are saved in the `example` folder. You can see the intermediate logs there and the final resulting files

## Author
M.Sc. Nikita Smirnov, Intelligent Systems AG, Department of Computer Science, Kiel University, Germany.

Please contact me in case of any questions or bug reports: [Nikita Smirnov](mailto:nsm@informatik.uni-kiel.de)
