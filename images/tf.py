import modules.runas
import modules.ssh

def emit(writer, **kwargs):
    # everything is already installed, just add runas and ssh
    modules.runas.emit(writer)
    modules.ssh.emit(writer)
    writer.emit("""
        RUN pip install --upgrade tensorflow-probability
    """)

def images():
    return {
        "tf:20.03": {
            "base": "nvcr.io/nvidia/tensorflow:20.03-tf2-py3 ",
            "needsContext": True,
        },
    }
