from math import ceil, log10
from typing import Dict
import matplotlib.pyplot as plt
import re
import xml.etree.ElementTree as ET


def get_average_vmaf_score(file_path: str) -> float:
    tree = ET.parse(file_path)
    root = tree.getroot()
    vmaf_tag = root.find('pooled_metrics').find('metric[@name="vmaf"]')
    mean_vmaf = float(vmaf_tag.attrib['mean'])
    return mean_vmaf


def get_average_psnr_score(file_path) -> float:
    mse_avgs = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.split()
            for part in parts:
                if part.startswith('mse_avg:'):
                    mse_avg = float(part.split(':')[1])
                    if mse_avg != 0.00:
                        mse_avgs.append(mse_avg)
                    break
    psnr_values = [20 * log10(255) - 10 * log10(mse) for mse in mse_avgs]
    return sum(psnr_values) / len(psnr_values) if len(psnr_values) > 0 else 60.0


def get_average_ssim_score(file_path: str) -> float:
    ssim_values = []
    with open(file_path, 'r') as file:
        for line in file:
            match = re.search(r'All:(\d+\.\d+)', line)
            if match:
                ssim = float(match.group(1))
                ssim_values.append(ssim)
    return sum(ssim_values) / len(ssim_values) if len(ssim_values) > 0 else 0.0


def draw_metrics_plot(metrics_folder: str) -> None:
    codecs = ["h264", "h265", "vp8", "vp9", "av1", "h264ha", "h265ha"]

    metrics_dict = dict(dict())
    for codec in codecs:
        metrics_dict[codec] = {
            "vmaf": get_average_vmaf_score(f"{metrics_folder}/vmaf_{codec}.xml"),
            "psnr": get_average_psnr_score(f"{metrics_folder}/psnr_{codec}.log"),
            "ssim": get_average_ssim_score(f"{metrics_folder}/ssim_{codec}.log"),
        }

    metrics = ["vmaf", "psnr", "ssim"]

    _, axs = plt.subplots(1, 3, figsize=(18, 10), dpi=300)

    for i, metric in enumerate(metrics):
        sorted_data = sorted(metrics_dict.items(), key=lambda x: x[1][metric])
        codecs = [item[0] for item in sorted_data]
        metric_values = [float(item[1][metric]) for item in sorted_data]

        axs[i].barh(codecs, metric_values, color='skyblue')
        axs[i].set_xlabel(metric.upper())
        axs[i].set_ylabel('Codec')
        axs[i].set_title(f'{metric.upper()} score for each video codec')
        axs[i].grid(axis='x')
        axs[i].set_xlim(min(metric_values) * 0.98, float(ceil(max(metric_values))))

    plt.subplots_adjust()
    plt.tight_layout()
    plt.savefig("plot_metrics.png")
