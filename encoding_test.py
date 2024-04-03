import os
import subprocess
import time

from process_results import draw_metrics_plot

# paths
input_file = "bbb720p.mp4"
output_containers = [
    "output_h264.mkv",
    "output_h265.mkv",
    "output_vp8.mkv",
    "output_vp9.mkv",
    "output_av1.mkv",
    "output_h264ha.mkv",
    "output_h265ha.mkv",
]
vmaf_model_path = "/home/vmaf/model/vmaf_v0.6.1.json"
resulting_dir = "/home/logs"

# GStreamer encoding pipelines for each encoder with optimized parameters imitating RTC
encoders = [
    # H.264 software encoding
    "gst-launch-1.0 filesrc location={} ! decodebin ! videoconvert ! video/x-raw,framerate=24/1 ! x264enc bitrate=2000 speed-preset=superfast tune=zerolatency ! matroskamux ! filesink location={}",
    # H.265 software encoding
    "gst-launch-1.0 filesrc location={} ! decodebin ! videoconvert ! video/x-raw,framerate=24/1 ! x265enc bitrate=2000 speed-preset=superfast tune=zerolatency ! h265parse ! matroskamux ! filesink location={}",
    # VP8 software encoding
    "gst-launch-1.0 filesrc location={} ! decodebin ! videoconvert ! video/x-raw,framerate=24/1 ! vp8enc deadline=1 target-bitrate=2000000 ! matroskamux ! filesink location={}",
    # VP9 software encoding
    "gst-launch-1.0 filesrc location={} ! decodebin ! videoconvert ! video/x-raw,framerate=24/1 ! vp9enc deadline=1 target-bitrate=2000000 ! matroskamux ! filesink location={}",
    # AV1 software encoding
    "gst-launch-1.0 filesrc location={} ! decodebin ! videoconvert ! video/x-raw,framerate=24/1 ! av1enc target-bitrate=2000 usage-profile=realtime ! av1parse ! matroskamux ! filesink location={}",
    # H.264 hardware encoding
    "gst-launch-1.0 filesrc location={} ! decodebin ! videoconvert ! video/x-raw,framerate=24/1 ! nvh264enc bitrate=2000 preset=low-latency-hq ! h264parse ! matroskamux ! filesink location={}",
    # H.265 hardware encoding
    "gst-launch-1.0 filesrc location={} ! decodebin ! videoconvert ! video/x-raw,framerate=24/1 ! nvh265enc bitrate=2000 preset=low-latency-hq ! h265parse ! matroskamux ! filesink location={}",
]

os.makedirs(resulting_dir, exist_ok=True)

with open("results.txt", "w") as file:
    for encoder, output_container in zip(encoders, output_containers):
        print(f"testing encoder: {encoder}")
        start_time = time.time()
        subprocess.run(encoder.format(input_file, output_container), shell=True)
        end_time = time.time()

        encoding_time = end_time - start_time

        output_size = subprocess.check_output(["du", "-b", output_container]).split()[0].decode("utf-8")

        codec_name = output_container.split("_")[1].split(".")[0]

        # VMAF
        vmaf_cmd = f"ffmpeg -r 24 -i {input_file} -r 24 -i {output_container} -lavfi libvmaf=log_path={resulting_dir}/vmaf_{codec_name}.xml:log_fmt=xml:model='path={vmaf_model_path}' -f null -"
        vmaf_output = subprocess.check_output(vmaf_cmd, shell=True).decode("utf-8")

        # PSNR
        psnr_cmd = f"ffmpeg -r 24 -i {input_file} -r 24 -i {output_container} -lavfi psnr=stats_file={resulting_dir}/psnr_{codec_name}.log -f null -"
        psnr_output = subprocess.check_output(psnr_cmd, shell=True).decode("utf-8")

        # SSIM
        ssim_cmd = f"ffmpeg -r 24 -i {input_file} -r 24 -i {output_container} -lavfi ssim=stats_file={resulting_dir}/ssim_{codec_name}.log -f null -"
        ssim_output = subprocess.check_output(ssim_cmd, shell=True).decode("utf-8")

        # write general results to the text file
        file.write(f"Codec: {codec_name}\n")
        file.write(f"Encoding time: {encoding_time}\n")
        file.write(f"Output size: {output_size}\n")
        file.write(f"\n")

# process and draw the final metrics plot
draw_metrics_plot(resulting_dir)
