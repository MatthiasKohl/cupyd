import modules.runas
import modules.ssh
import modules.legate_dask
import modules.openmpi
import modules.gasnet
import modules.nsys

def emit(writer, **kwargs):
    if "cudaVersionFull" not in kwargs:
        raise Exception("'cudaVersionFull' is mandatory!")
    if "rapidsVersion" not in kwargs:
        raise Exception("'rapidsVersion' is mandatory!")
    # everything is already installed, just add runas and ssh
    modules.runas.emit(writer)
    modules.ssh.emit(writer)
    modules.legate_dask.emit(writer, **kwargs)
    modules.openmpi.emit(writer, devBuild=False, ompiVersion="4.0.2")
    modules.gasnet.emit(writer, conduit="mpi")
    modules.nsys.emit(writer, version="2020.2.1")
    writer.emit("""
        ENV OPT_DIR=/opt
        ENV LEGATE_DIR=/home/scratch.mjoux_gpu/dev/legate.core/install
        ENV LIBRARY_PATH="$${LEGATE_DIR}/lib:$${LIBRARY_PATH}"
        ENV LD_LIBRARY_PATH="$${LEGATE_DIR}/lib:$${LD_LIBRARY_PATH}"
    """)

def images():
    return {
        "legate-dask:10.0": {
            "base": "rapidsai/rapidsai-dev:0.12-cuda10.0-devel-ubuntu16.04-py3.7",
            "rapidsVersion": "0.12",
            "cudaVersionFull": "10.0.130",
            "needsContext": True,
        },
        "legate-dask-0.14:10.0": {
            "base": "rapidsai/rapidsai-dev-nightly:0.14-cuda10.0-devel-ubuntu16.04-py3.7",
            "rapidsVersion": "0.14",
            "cudaVersionFull": "10.0.130",
            "needsContext": True,
        },
        "legate-dask-0.15:10.2": {
            "base": "rapidsai/rapidsai-dev-nightly:0.15-cuda10.2-devel-ubuntu16.04-py3.7",
            "rapidsVersion": "0.15",
            "cudaVersionFull": "10.2.89",
            "needsContext": True,
        },
        "legate-dask-0.18:11.0": {
            "base": "rapidsai/rapidsai-core-dev-nightly:0.18-cuda11.0-devel-ubuntu18.04-py3.7",
            "rapidsVersion": "0.18",
            "cudaVersionFull": "11.0.1",
            "needsContext": True,
        },
        "legate-dask-debug:10.0": {
            "base": "rapidsai/rapidsai-dev:0.12-cuda10.0-devel-ubuntu16.04-py3.7",
            "rapidsVersion": "0.12",
            "cudaVersionFull": "10.0.130",
            "needsContext": True,
            "debug": True,
        }
    }
