from __future__ import absolute_import
import modules.cuda_dev
import modules.build_essential

def emit(writer, **kwargs):
    if "cudaVersionFull" not in kwargs:
        raise Exception("'cudaVersionFull' is mandatory!")
    if "rapidsVersion" not in kwargs:
        raise Exception("'rapidsVersion' is mandatory!")
    ncclVersion = "2.4"  # should be good for rapids 0.10+
    cudaVersionFull = kwargs["cudaVersionFull"]
    rapidsVersion = kwargs["rapidsVersion"]
    modules.cuda_dev.emit(writer, cudaVersionFull)
    modules.build_essential.emit(writer)
    # setup Python 3.6 (we use make install as we have no prior python)
    writer.packages(['ca-certificates', 'zlib1g-dev', 'libncurses5-dev', 'libgdbm-dev', 'libnss3-dev', 'libssl-dev', 'libreadline-dev', 'libffi-dev', 'wget'])
    writer.emit("""
    RUN wget --no-check-certificate https://www.python.org/ftp/python/3.6.9/Python-3.6.9.tgz && \\
        tar -xf Python-3.6.9.tgz && \\
        cd Python-3.6.9 && \\
        ./configure --enable-optimizations --enable-shared --prefix=/usr && \\
        make -j8 build_all && \\
        make -j8 altinstall
    RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.6 10
    RUN update-alternatives --install /usr/bin/pip pip /usr/bin/pip3.6 10
    RUN pip install --upgrade pip
    """)
    # TODO all tests (arrow, rmm, cudf, cuml)
    # TODO arrow build with clang (required for cuml anyway)
    # Dependencies up to here: Python3.6+, ca-certificates package, build-essential, wget, git, make, tar
    # potential problems for rmm/cudf: arrow-cpp, double-conversion
    # possible problems for rmm/cudf: ipython, pytest, hypothesis
    # TODO use cuda short version / python versions above

    writer.emit("""
    ENV CUDA_HOME /usr/local/cuda-10.0
    RUN pip install setuptools wheel scikit-build
    RUN pip install cmake pyarrow cython numba
    RUN git clone --recurse-submodules -b branch-0.12 https://github.com/rapidsai/rmm.git /opt/rmm && \\
        cd /opt/rmm && \\
        mkdir build && \\
        cd build && \\
        cmake .. -DCMAKE_INSTALL_PREFIX=/usr/local && \\
        make -j && \\
        make install && \\
        cd ../python && \\
        sed -i 's/f\"Invalid CUDA_HOME: \"//g' setup.py && \\
        python setup.py build_ext --inplace && \\
        python setup.py install
    """)
    writer.packages(['libboost-all-dev', 'libssl-dev', 'bison', 'flex'])
    # the linking is a hack to make FindCUDA (deprecated in Cmake) work
    writer.emit("""
    RUN ln -s /usr/local/cuda/lib64/stubs/libcuda.so /usr/local/cuda/lib64/libcuda.so
    RUN ldconfig
    RUN git clone https://github.com/apache/arrow.git /opt/arrow && \\
        cd /opt/arrow/cpp && \\
        mkdir release && \\
        cd release && \\
        cmake .. -DARROW_CUDA=ON -DCUDA_TOOLKIT_ROOT_DIR=/usr/local/cuda -DARROW_PARQUET=ON -DARROW_PLASMA=ON -DARROW_PYTHON=ON && \\
        make -j8 && \\
        make install
    """)
    writer.emit("""
    RUN pip install cmake_setuptools pandas fastavro dask[complete] streamz python-rapidjson fsspec flatbuffers
    RUN git clone https://github.com/dmlc/dlpack /opt/dlpack && \\
        cd /opt/dlpack && \\
        mkdir build && \\
        cd build && \\
        cmake .. && \\
        make && \\
        make install
    RUN git clone --recurse-submodules -b branch-0.12 https://github.com/rapidsai/cudf.git /opt/cudf && \\
        cd /opt/cudf && \\
        INSTALL_PREFIX=/usr/local ./build.sh
    """)
    # # MNMG will be impossible:
    # # hopefully, libcumlprims and nccl are not required with --singlegpu
    # writer.emit("""
    # RUN pip install cupy-cuda100 scikit-learn umap-learn dask-ml statsmodels
    # RUN git clone  --recurse-submodules -b branch-0.12 https://github.com/rapidsai/cuml.git /opt/cuml && \\
    #     cd /opt/cuml/cpp && \\
    #     mkdir build && \\
    #     cd build && \\
    #     cmake .. -DCMAKE_INSTALL_PREFIX=/usr/local -DBUILD_CUML_STD_COMMS=OFF -DWITH_UCX=OFF -DBUILD_CUML_MPI_COMMS=OFF -DBUILD_CUML_MG_TESTS=OFF && \\
    #     make -j && \\
    #     make install && \\
    #     cd /opt/cuml/python && \\
    #     python setup.py build_ext --inplace --singlegpu && \\
    #     python setup.py install
    # """)


def images():
    return {
        "rapids-scratch": {
            "cudaVersionFull": "10.0.130",
            "base": "ubuntu:16.04",
            "needsContext": True,
            "rapidsVersion": "0.12"
        },
    }
