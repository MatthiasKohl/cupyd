import modules.conda

def emit(writer, rapidsVersion, cumlPrimsVersion):
    modules.conda.emit(writer)
    writer.packages(["doxygen", "graphviz", "gzip",
                     "libopenblas-dev", "libpthread-stubs0-dev", "tar", "unzip",
                     "zlib1g-dev"])
    added_packages = []
    daskVersion, distributedVersion = "2.5.0", "2.5.1"
    fsspecVersion, arrowVersion = "0.5*", "0.14.1"
    numbaVersion = "0.45*"
    if rapidsVersion >= "0.11":
        added_packages.extend(["ucx-proc=*=gpu", "ucx",
            "ucx-py=$rapidsVersion.*", "\"protobuf>=3.4.1,<4.0.0\""])
        daskVersion, distributedVersion = "2.8*", "2.8*"
        fsspecVersion, arrowVersion = "0.6*", "0.15.0"
    if rapidsVersion >= "0.12":
        numbaVersion = "0.46*"
    writer.condaPackages([
        "libclang=8.0.0", "cmake=3.14.5", "cmake_setuptools=0.1.*",
        "numba=$numbaVersion", "pandas=0.24.*", "pyarrow=$arrowVersion",
        "fastavro=0.22.*", "fsspec=$fsspecVersion", "pandoc=2.0.0",
        "dask=$daskVersion", "distributed=$distributedVersion",
        "streamz", "dlpack", "arrow-cpp=$arrowVersion", "boost",
        "double-conversion", "rapidjson", "flatbuffers", "hypothesis",
        "cupy=6.6*", "rmm=$rapidsVersion.*",
        "cython=0.29", "pytest=4.6", "scikit-learn=0.21",
        "umap-learn=0.3.9", "dask=$daskVersion", "distributed=$distributedVersion",
        "dask-ml", "nccl=2.4", "libcumlprims=$cumlPrimsVersion",
        "statsmodels",] + added_packages,
        channels=["anaconda", "numba",
                "nvidia/label/cuda$$CUDA_VERSION_SHORT",
                "rapidsai/label/cuda$$CUDA_VERSION_SHORT",
                "rapidsai-nightly/label/cuda$$CUDA_VERSION_SHORT",
                "rapidsai/label/main",
                "rapidsai-nightly/label/main",
                "conda-forge", "defaults"],
        rapidsVersion=rapidsVersion,
        daskVersion=daskVersion,
        distributedVersion=distributedVersion,
        numbaVersion=numbaVersion,
        fsspecVersion=fsspecVersion,
        arrowVersion=arrowVersion,
        cumlPrimsVersion=cumlPrimsVersion)

    writer.emit("""ENV NUMBAPRO_NVVM=/usr/local/cuda/nvvm/lib64/libnvvm.so
    ENV NUMBAPRO_LIBDEVICE=/usr/local/cuda/nvvm/libdevice/
    ENV CONDA_PREFIX=/opt/conda
    ENV CUDF_HOME /opt/cudf
    ENV CUML_HOME /opt/cuml
    """)

    writer.emit("""RUN git clone --recursive "https://github.com/rapidsai/cudf" /opt/cudf && \\
    cd /opt/cudf && \\
    git checkout branch-$rapidsVersion && \\
    git submodule update --init --recursive && \\
    ./build.sh && \\
    cd /opt && \\
    rm -rf /opt/cudf""",
    rapidsVersion=rapidsVersion)

    writer.emit("""RUN git clone --recursive "https://github.com/rapidsai/cuml" /opt/cuml && \\
    cd /opt/cuml && \\
    git checkout branch-$rapidsVersion && \\
    git submodule update --init --recursive && \\
    ./build.sh && \\
    cd cpp/build && \\
    cd /opt && \\
    rm -rf /opt/cuml""",
    rapidsVersion=rapidsVersion)
