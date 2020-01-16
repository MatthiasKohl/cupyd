import modules.conda_ml_env
import modules.cudf


def emit(writer, rapidsVersion):
    modules.conda_ml_env.emit(writer)
    modules.cudf.emit(writer, rapidsVersion)
    writer.packages(["doxygen", "graphviz", "gzip",
                     "libopenblas-dev", "libpthread-stubs0-dev", "tar", "unzip",
                     "zlib1g-dev"])
    added_packages = []
    daskVersion, distributedVersion = "2.5.0", "2.5.1"
    numbaVersion = "0.45*"
    if rapidsVersion >= "0.11":
        added_packages.extend([
            "ucx-proc=*=gpu", "ucx", "ucx-py=$rapidsVersion.*",
            "protobuf=3.4.*"])
        daskVersion, distributedVersion = "2.8*", "2.8*"
    if rapidsVersion >= "0.12":
        numbaVersion = "0.46*"
    writer.condaPackages([
        "clangdev=8.0.0", "cmake=3.14.5", "numba=$numbaVersion",
        "cupy=6.6*", "rmm=$rapidsVersion.*",
        "cython=0.29", "pytest=4.6", "scikit-learn=0.21", 
        "umap-learn=0.3.9", "dask=$daskVersion", "distributed=$distributedVersion",
        "dask-ml", "nccl=2.4", "libcumlprims=$rapidsVersion.*",
        "statsmodels",] +
        added_packages,
        channels=["anaconda", "numba", "conda-forge",
                "nvidia/label/cuda$$CUDA_VERSION_SHORT",
                "rapidsai/label/cuda$$CUDA_VERSION_SHORT",
                "rapidsai-nightly/label/cuda$$CUDA_VERSION_SHORT",
                "defaults"],
        rapidsVersion=rapidsVersion,
        daskVersion=daskVersion,
        distributedVersion=distributedVersion,
        numbaVersion=numbaVersion)
    writer.emit("""ENV NUMBAPRO_NVVM=/usr/local/cuda/nvvm/lib64/libnvvm.so
ENV NUMBAPRO_LIBDEVICE=/usr/local/cuda/nvvm/libdevice/
ENV CONDA_PREFIX=/opt/conda
ENV CUML_HOME /opt/cuml
""")
    writer.emit("""RUN git clone --recursive "https://github.com/rapidsai/cuml" /opt/cuml && \\
    cd /opt/cuml && \\
    git checkout branch-$rapidsVersion && \\
    git submodule update --init --recursive && \\
    ./build.sh && \\
    cd cpp/build && \\
    cd /opt && \\
    rm -rf /opt/cuml""",
    rapidsVersion=rapidsVersion)
