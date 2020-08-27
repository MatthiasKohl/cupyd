from __future__ import absolute_import
import modules.cuda_dev_internal
import modules.cuda
import modules.runas
import modules.ssh
import modules.build_essential
import modules.cmake
import modules.gcc7
from datetime import datetime, timedelta


def emit(writer, **kwargs):
    if "cudaVersionFull" not in kwargs:
        raise Exception("'cudaVersionFull' is mandatory!")
    if "cublasShort" not in kwargs:
        raise Exception("'cublasShort' is mandatory!")
    cudaVersionFull = kwargs["cudaVersionFull"]
    cublasShort = kwargs["cublasShort"]
    if "requiredShort" not in kwargs:
        major, minor, subminor, versionShort, pkgVersion = modules.cuda.shortVersion(cudaVersionFull)
        requiredShort = versionShort
        print("Warning: using {} as required CUDA version, this may not work with the latest CUDA / driver combo")
    else:
        requiredShort = kwargs["requiredShort"]
    if "cmakeVersionFull" not in kwargs:
        raise Exception("'cmakeVersionFull' is mandatory!")
    cmakeVersionFull = kwargs["cmakeVersionFull"]
    modules.runas.emit(writer)
    modules.ssh.emit(writer)
    modules.build_essential.emit(writer)
    modules.cmake.emit(writer, cmakeVersionFull)
    writer.packages(["ca-certificates", "doxygen", "clang-format-8"])
    writer.emit("""
        RUN update-alternatives --install /usr/bin/clang-format clang-format /usr/bin/clang-format-8 100
        ENV CUDA_ROOT /usr/local/cuda
    """)
    modules.gcc7.emit(writer)
    modules.cuda_dev_internal.emit(
        writer, cudaVersionFull, cublasShort, requiredShort, baseImage=kwargs["base"])


def images():
    return {
        "cuda-internal:11.1": { 
            "cudaVersionFull": "11.1." + (datetime.now() - timedelta(days=1)).strftime("%Y%m%d"),
            "requiredShort": "11.0",
            "cublasShort": "11.0",
            "base": "ubuntu:18.04",
            "needsContext": True,
            "cmakeVersionFull": "3.17.3" 
        },
        "cuda-internal:11.0": { 
            "cudaVersionFull": "11.0." + (datetime.now() - timedelta(days=1)).strftime("%Y%m%d"),
            "cublasShort": "11.0",
            "base": "ubuntu:18.04",
            "needsContext": True,
            "cmakeVersionFull": "3.17.3" 
        },
    }
