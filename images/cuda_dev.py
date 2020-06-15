from __future__ import absolute_import
import modules.cuda_dev
import modules.runas
import modules.ssh
import modules.build_essential
import modules.cmake
import modules.gcc7


def emit(writer, **kwargs):
    if "cudaVersionFull" not in kwargs:
        raise Exception("'cudaVersionFull' is mandatory!")
    cudaVersionFull = kwargs["cudaVersionFull"]
    if "cmakeVersionFull" not in kwargs:
        raise Exception("'cmakeVersionFull' is mandatory!")
    if "cudaVersionExt" not in kwargs:
        kwargs["cudaVersionExt"] = cudaVersionFull
    cmakeVersionFull = kwargs["cmakeVersionFull"]
    cudaVersionExt = kwargs["cudaVersionExt"]
    modules.cuda_dev.emit(writer, cudaVersionFull, cudaVersionExt, kwargs["base"])
    modules.runas.emit(writer)
    modules.ssh.emit(writer)
    modules.build_essential.emit(writer)
    modules.cmake.emit(writer, cmakeVersionFull)
    writer.packages(["ca-certificates", "doxygen", "clang-format-8"])
    writer.emit("""
        RUN update-alternatives --install /usr/bin/clang-format clang-format /usr/bin/clang-format-8 100
    """)
    modules.gcc7.emit(writer)


def images():
    return {
        "cuda-dev:10.0": { "cudaVersionFull": "10.0.130",
                           "base": "ubuntu:16.04",
                           "needsContext": True,
                           "cmakeVersionFull": "3.14.7" },
        "cuda-dev:10.1": { "cudaVersionFull": "10.1.105",
                           "base": "ubuntu:16.04",
                           "needsContext": True,
                           "cmakeVersionFull": "3.14.7" },
        "cuda-dev:10.1-1804": { "cudaVersionFull": "10.1.105",
                                "base": "ubuntu:18.04",
                                "needsContext": True,
                                "cmakeVersionFull": "3.14.7" },
        "cuda-dev:10.2": { "cudaVersionFull": "10.2.89",
                           "cudaVersionExt": "10.2.2.89",
                           "base": "ubuntu:18.04",
                           "needsContext": True,
                           "cmakeVersionFull": "3.16.2" },
        "cuda-dev:11.0": { "cudaVersionFull": "11.0.191",
                           "cudaVersionExt": "11.0.0.191",
                           "base": "ubuntu:18.04",
                           "needsContext": True,
                           "cmakeVersionFull": "3.16.2" },
    }
