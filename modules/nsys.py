def emit(writer, version="2020.2.1"):
    # just taken from
    # https://devblogs.nvidia.com/nvidia-nsight-systems-containers-cloud/
    writer.emit("""
        RUN apt-get update -y && \
            DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
                apt-transport-https \
                ca-certificates \
                gnupg \
                wget && \
            rm -rf /var/lib/apt/lists/*
        RUN wget -qO - https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/7fa2af80.pub | apt-key add - && \
            echo "deb https://developer.download.nvidia.com/devtools/repo-deb/x86_64/ /" >> /etc/apt/sources.list.d/nsight.list && \
            apt-get update -y && \
            DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
                nsight-systems-${version} && \
            rm -rf /var/lib/apt/lists/* 
    """, version=version)
