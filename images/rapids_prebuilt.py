import modules.runas
import modules.ssh

def emit(writer, **kwargs):
    if "cudaVersionFull" not in kwargs:
        raise Exception("'cudaVersionFull' is mandatory!")
    if "rapidsVersion" not in kwargs:
        raise Exception("'rapidsVersion' is mandatory!")
    # everything is already installed, just add runas and ssh
    modules.runas.emit(writer)
    modules.ssh.emit(writer)


def images():
    return {
        "rapids-pre-0.11:10.0": {
            "base": "rapidsai/rapidsai-dev:0.11-cuda10.0-devel-ubuntu16.04-py3.7",
            "rapidsVersion": "0.11",
            "cudaVersionFull": "10.0.130",
            "needsContext": True,
        }
    }