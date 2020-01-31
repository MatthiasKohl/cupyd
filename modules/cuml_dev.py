import modules.cuda

def emit(writer, **kwargs):
    if "rapidsVersion" not in kwargs:
        raise Exception("'rapidsVersion' is mandatory!")
    rapidsVersion = kwargs["rapidsVersion"]
    numbaVersion, ucxVersion = "0.45*", "$rapidsVersion.*"
    if rapidsVersion >= "0.12":
        numbaVersion, ucxVersion = "0.46*", "0.11"
    writer.packages(["doxygen", "graphviz", "gzip", "libopenblas-dev",
                     "libpthread-stubs0-dev", "tar", "unzip", "zlib1g-dev"])
    writer.condaPackages(["boost", "cmake=3.14.5", "cudf=$rapidsVersion.*",
                          "cython", "dask", "dask-cuda=$rapidsVersion.*",
                          "dask-cudf=$rapidsVersion.*", "dask-ml",
                          "distributed", "flake8", "libclang=8.0.0",
                          "libcumlprims=$rapidsVersion.*", "nccl>=2.4",
                          "numba=$numbaVersion", "protobuf", "pytest",
                          "rmm=$rapidsVersion.*", "scikit-learn", "scipy",
                          "statsmodels", "umap-learn",
                          "ucx-proc=*=gpu", "ucx", "ucx-py=$ucxVersion",],
                         channels=["rapidsai", "nvidia", "rapidsai-nightly",
                                   "conda-forge", "anaconda", "defaults"],
                         rapidsVersion=rapidsVersion,
                         numbaVersion=numbaVersion,
                         ucxVersion=ucxVersion)
    writer.emit("""ENV CONDA_PREFIX=/opt/conda""")
