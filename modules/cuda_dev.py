import re
import modules.cuda


def emit(writer, cudaVersionFull, cudaVersionExt, nsysVersion="2019.5.2", baseImage="ubuntu:16.04"):
    major, minor, subminor, versionShort, pkgVersion = modules.cuda.shortVersion(cudaVersionFull)
    extVersion = "%s-%s=%s-1" % (major, minor, cudaVersionExt)
    modules.cuda.emit(writer, cudaVersionFull, cudaVersionExt, baseImage)
    if versionShort == "9.2":
        writer.packages(["cuda-compiler-$pkgVersion",
                         "cuda-cupti-$pkgVersion",
                         "cuda-nvcc-$pkgVersion"],
                        pkgVersion=pkgVersion)
    short = float(versionShort)
    pkgs = [
        "cuda-command-line-tools-$pkgVersion",
        "cuda-cudart-dev-$pkgVersion",
        "cuda-driver-dev-$pkgVersion",
        "cuda-nvml-dev-$pkgVersion",
        "cuda-nvrtc-dev-$pkgVersion"
    ]
    if short >= 11.0:
        pkgs = [
            "cuda-command-line-tools-$major-$minor",
            "cuda-cudart-dev-$major-$minor",
            "cuda-driver-dev-$major-$minor",
            "cuda-nvml-dev-$major-$minor",
            "cuda-nvrtc-dev-$major-$minor"
        ]
    if short < 10.1:
        pkgs.append("cuda-cublas-dev-$pkgVersion")
    elif short < 11.0:
        pkgs.append("libcublas-dev=$cudaVersionExt-1")
    else:
        pkgs.append("libcublas-dev-$extVersion")
    if short < 11.0:
        pkgs.extend([
            "cuda-core-$pkgVersion",
            "cuda-cufft-dev-$pkgVersion",
            "cuda-curand-dev-$pkgVersion",
            "cuda-cusolver-dev-$pkgVersion",
            "cuda-cusparse-dev-$pkgVersion",
            "cuda-misc-headers-$pkgVersion",
            "cuda-npp-dev-$pkgVersion",
            "cuda-nvgraph-dev-$pkgVersion",
        ])
    else:
        pkgs.extend([
            "libcufft-dev-$major-$minor",
            "libcurand-dev-$major-$minor",
            "libcusolver-dev-$major-$minor",
            "libcusparse-dev-$extVersion",
            "libnpp-dev-$extVersion",
        ])
    if short >= 10.1:
        pkgs.append("cuda-cupti-dev-11-0")
        pkgs.append("cuda-nsight-compute-$major-$minor")
        pkgs.append("cuda-nsight-systems-$major-$minor")
        if short == 10.2:
            pkgs.append("nsight-systems-2019.5.2")
        elif short == 11.0:
            pkgs.append("nsight-systems-2020.2.5")
    writer.packages(
        pkgs, pkgVersion=pkgVersion, extVersion=extVersion, major=major,
        minor=minor, cudaVersionExt=cudaVersionExt, nsysVersion=nsysVersion,
        installOpts="--allow-downgrades")
