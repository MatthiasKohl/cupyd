from __future__ import absolute_import
import modules.runas
import modules.ssh
import modules.cmake

def emit(writer, **kwargs):
    if "cmakeVersionFull" not in kwargs:
        raise Exception("'cmakeVersionFull' is mandatory!")
    cmakeVersionFull = kwargs["cmakeVersionFull"]
    modules.runas.emit(writer)
    modules.ssh.emit(writer)
    modules.cmake.emit(writer, cmakeVersionFull)
    writer.packages(["ca-certificates", "doxygen", "clang-format-8"])
    writer.emit("""
        RUN update-alternatives --install /usr/bin/clang-format clang-format /usr/bin/clang-format-8 100
        ENV CUDA_ROOT /usr/local/cuda
    """)

def images():
    return {
        "cuda-dev-dt:10.2": {
            "cudaVersionFull": "10.2.89",
            "base": "gitlab-master.nvidia.com:5005/dt-compute-public/container/cuda-released/10.2-ubuntu18.04-gnu8:20200602",
            "needsContext": True,
            "cmakeVersionFull": "3.18.0-rc2"
        }
    }
