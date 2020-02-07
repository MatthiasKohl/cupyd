import modules.runas
import modules.ssh
import modules.legate_dask

def emit(writer, **kwargs):
    if "cudaVersionFull" not in kwargs:
        raise Exception("'cudaVersionFull' is mandatory!")
    if "rapidsVersion" not in kwargs:
        raise Exception("'rapidsVersion' is mandatory!")
    # everything is already installed, just add runas and ssh
    modules.runas.emit(writer)
    modules.ssh.emit(writer)
    modules.legate_dask.emit(writer, **kwargs)

def images():
    return {
        "legate-dask:10.0": {
            "base": "rapidsai/rapidsai-dev:0.11-cuda10.0-devel-ubuntu16.04-py3.7",
            "rapidsVersion": "0.11",
            "cudaVersionFull": "10.0.130",
            "needsContext": True,
            "legate_branch": "dask_interop",
        },
        "legate-dask-debug:10.0": {
            "base": "rapidsai/rapidsai-dev:0.11-cuda10.0-devel-ubuntu16.04-py3.7",
            "rapidsVersion": "0.11",
            "cudaVersionFull": "10.0.130",
            "needsContext": True,
            "debug": True,
            "legate_branch": "dask_interop",
        }
    }
    