import modules.conda_ml_env


def emit(writer, rapidsVersion):
    modules.conda_ml_env.emit(writer)
    added_packages = []
    daskVersion, distributedVersion = "2.5.0", "2.5.1"
    fsspecVersion, arrowVersion = "0.5*", "0.14.1"
    numbaVersion = "0.45*"
    if rapidsVersion >= "0.11":
        daskVersion, distributedVersion = "2.8*", "2.8*"
        fsspecVersion, arrowVersion = "0.6*", "0.15.0"
        added_packages.append("cupy=6.6*")
    if rapidsVersion >= "0.12":
        numbaVersion = "0.46*"
    writer.condaPackages([
        "rmm=$rapidsVersion.*", "cmake=3.14.5", "cmake_setuptools=0.1.*",
        "numba=$numbaVersion", "pandas=0.24.*", "pyarrow=$arrowVersion",
        "fastavro=0.22.*", "cython=0.29", "fsspec=$fsspecVersion",
        "pytest=4.6", "sphinx", "ipython", "pandoc=2.0.0", "pip",
        "flake8", "isort", "pre_commit", "dask=$daskVersion",
        "distributed=$distributedVersion", "streamz", "dlpack",
        "arrow-cpp=$arrowVersion", "boost", "double-conversion",
        "rapidjson", "flatbuffers", "hypothesis"] +
        added_packages,
        channels=["numba", "conda-forge",
                "nvidia/label/cuda$$CUDA_VERSION_SHORT",
                "rapidsai/label/cuda$$CUDA_VERSION_SHORT",
                "rapidsai-nightly/label/cuda$$CUDA_VERSION_SHORT",
                "defaults"],
        rapidsVersion=rapidsVersion,
        daskVersion=daskVersion,
        distributedVersion=distributedVersion,
        fsspecVersion=fsspecVersion,
        arrowVersion=arrowVersion,
        numbaVersion=numbaVersion)
    writer.emit("""ENV NUMBAPRO_NVVM=/usr/local/cuda/nvvm/lib64/libnvvm.so
ENV NUMBAPRO_LIBDEVICE=/usr/local/cuda/nvvm/libdevice/
ENV CONDA_PREFIX=/opt/conda
ENV CUDF_HOME /opt/cudf""")
    writer.emit("""RUN git clone --recursive "https://github.com/rapidsai/cudf" /opt/cudf && \\
    cd /opt/cudf && \\
    git checkout branch-$rapidsVersion && \\
    git submodule update --init --recursive && \\
    ./build.sh && \\
    cd /opt && \\
    rm -rf /opt/cudf""",
    rapidsVersion=rapidsVersion)
