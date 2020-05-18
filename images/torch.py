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
    }
