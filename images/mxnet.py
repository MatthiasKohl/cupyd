import modules.runas
import modules.ssh

def emit(writer, **kwargs):
    # everything is already installed, just add runas and ssh
    modules.runas.emit(writer)
    modules.ssh.emit(writer)

def images():
    return {
        "mxnet:20.06": {
            "base": "nvcr.io/nvidia/mxnet:20.06-py3",
            "cudaVersionFull": "11.0.167",
            "needsContext": True,
        },
    }
