from __future__ import absolute_import
import modules.cuda_dev
import modules.runas
import modules.ssh
import modules.conda
import modules.rapids
import modules.xgboost


def emit(writer, **kwargs):
    if "cudaVersionFull" not in kwargs:
        raise Exception("'cudaVersionFull' is mandatory!")
    if "rapidsVersion" not in kwargs:
        raise Exception("'rapidsVersion' is mandatory!")
    if "cumlPrimsVersion" not in kwargs:
        raise Exception("'cumlPrimsVersion' is mandatory!")
    ncclVersion = "2.4"  # should be good for rapids 0.10+
    cudaVersionFull = kwargs["cudaVersionFull"]
    rapidsVersion = kwargs["rapidsVersion"]
    modules.cuda_dev.emit(writer, cudaVersionFull)
    modules.conda.emit(writer)
    modules.runas.emit(writer)
    modules.ssh.emit(writer)
    modules.rapids.emit(writer,
        rapidsVersion=rapidsVersion,
        cumlPrimsVersion=kwargs["cumlPrimsVersion"])

    # include the below for xgboost and NSight added

#     modules.xgboost.emit(writer, ncclVersion=ncclVersion)
#     writer.emit("""RUN git clone https://github.com/JohnZed/cuml-samples /opt/cuml-samples && \\
#     chmod a+x /opt/cuml-samples/*.py""")
#     writer.emit("""WORKDIR /opt/cuml-samples""")
#     writer.emit("""RUN wget https://developer.nvidia.com/rdp/assets/Nsight_Systems_2019_3_Linux_installer && \\
#     chmod +x Nsight_Systems_2019_3_Linux_installer && \\
#     ./Nsight_Systems_2019_3_Linux_installer --accept --quiet && \\
#     mv NsightSystems-* /usr/local/cuda/NsightSystems && \\
#     rm -f Nsight_Systems_2019_3_Linux_installer""")
#     writer.emit("""ENV PATH=/usr/local/cuda/NsightSystems/Target-x86_64/x86_64/:$${PATH}
# ENV PATH=/usr/local/cuda/NsightSystems/Host-x86_64/:$${PATH}
# ENV LD_LIBRARY_PATH=/usr/local/cuda/NsightSystems/Target-x86_64/x86_64/:$${LD_LIBRARY_PATH}
# ENV LD_LIBRARY_PATH=/usr/local/cuda/NsightSystems/Host-x86_64/:$${LD_LIBRARY_PATH}""")


def images():
    return {
        "rapids-0.11:9.2": { "cudaVersionFull": "9.2.88",
                            "base": "ubuntu:16.04",
                            "needsContext": True,
                            "rapidsVersion": "0.11",
                            "cumlPrimsVersion": "0.11.*" },
        "rapids-0.11:10.0": { "cudaVersionFull": "10.0.130",
                             "base": "ubuntu:16.04",
                             "needsContext": True,
                             "rapidsVersion": "0.11",
                             "cumlPrimsVersion": "0.11.*" },
        "rapids-0.12:10.0": { "cudaVersionFull": "10.0.130",
                             "base": "ubuntu:16.04",
                             "needsContext": True,
                             "rapidsVersion": "0.12",
                             "cumlPrimsVersion": "0.12.0a200121" }
    }
