import modules.runas
import modules.ssh

def emit(writer, **kwargs):
    # everything is already installed, just add runas and ssh
    modules.runas.emit(writer)
    modules.ssh.emit(writer)
    writer.packages(['graphviz'])
    assert 'containerSource' in kwargs

def images():
    return {
        "torch:20.03": {
            "base": "nvcr.io/nvidia/pytorch:20.03-py3",
            "containerSource": "NGC",
            "needsContext": True,
        },
        "torch:20.08": {
            "base": "nvcr.io/nvidia/pytorch:20.08-py3",
            "containerSource": "NGC",
            "needsContext": True,
        },
        "torch:cuda-graphs-master": {
            "base": "gitlab-master.nvidia.com:5005/dl/dgx/pytorch:cuda-graphs-master-py3-devel",
            "containerSource": "gitlab",
            "needsContext": True
        },
        "torch:cuda-graphs-master-56": {
            "base": "gitlab-master.nvidia.com:5005/dl/dgx/pytorch:cuda-graphs-master-py3.1956997-devel",
            "containerSource": "gitlab",
            "needsContext": True
        }
    }
