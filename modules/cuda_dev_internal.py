import re
import modules.cuda

def emit(writer, cudaVersionFull, cublasShort, requiredShort, baseImage="ubuntu:16.04"):
    osVer = re.sub(":", "", baseImage)
    osVer = re.sub("[.]", "", osVer)
    major, minor, subminor, versionShort, pkgVersion = modules.cuda.shortVersion(cudaVersionFull)

    # based on https://gitlab-master.nvidia.com/nv/ipp-docker/blob/master/linux-ub16-cuda-10.2-internal-gcc-7.3-dockerfile
    writer.packages(["wget"])
    writer.emit("""
        RUN if [ -d /usr/local/cuda ] ; then unlink /usr/local/cuda ; fi
        RUN if [ -d /usr/local/cuda-$versionShort ] ; then rm -rf /usr/local/cuda-$versionShort ; fi
        RUN mkdir /usr/local/cuda-$versionShort
        RUN wget -q https://sc-hw-artf.nvidia.com/compute-generic-local/cuda/$versionShort/x86_64/linux/generic/release-internal/cuda-$versionShort-latest.tgz
        RUN tar -xf cuda-$versionShort-latest.tgz -C /usr/local/cuda-$versionShort
        RUN rm -rf cuda-$versionShort-latest.tgz
        RUN ln -s /usr/local/cuda-$versionShort /usr/local/cuda

        RUN wget -q https://sc-hw-artf.nvidia.com/compute-generic-local/cublas/$cublasShort/x86_64/linux/generic/cuda-$cublasShort/release/cublas-$cublasShort-latest.tgz
        RUN tar -xf cublas-$cublasShort-latest.tgz -C /usr/local/cuda-$versionShort
        RUN rm -rf cublas-$cublasShort-latest.tgz

        RUN echo "/usr/local/cuda-$versionShort/lib64" >> /etc/ld.so.conf.d/cuda.conf && \\
        ldconfig
        
        ENV PATH /usr/local/cuda-$versionShort/bin:$${PATH}
        ENV LD_LIBRARY_PATH /usr/local/cuda-$versionShort/lib64:$${LD_LIBRARY_PATH}
        ENV LIBRARY_PATH /usr/local/cuda-$versionShort/lib64/stubs:$${LIBRARY_PATH}
        
        ENV CUDA_VERSION_SHORT $versionShort
        ENV CUDA_VERSION $cudaVersionFull

        ENV NVIDIA_REQUIRE_CUDA "cuda>=$requiredShort"
        LABEL com.nvidia.volumes.needed="nvidia_driver"

        ENV NVIDIA_VISIBLE_DEVICES all
        ENV NVIDIA_DRIVER_CAPABILITIES compute,utility
    """,
        versionShort=versionShort,
        requiredShort=requiredShort,
        cudaVersionFull=cudaVersionFull,
        cublasShort=cublasShort)
    