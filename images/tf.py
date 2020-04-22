import modules.runas
import modules.ssh

def emit(writer, **kwargs):
    # everything is already installed, just add runas and ssh
    modules.runas.emit(writer)
    modules.ssh.emit(writer)
    assert 'TFMajorVersion' in kwargs
    tfp_install = 'tensorflow-probability'
    if kwargs['TFMajorVersion'] == 1:
        tfp_install = 'tensorflow-probability==0.7'
    writer.emit("""
        RUN pip install $tfp_install fs pendulum
    """, tfp_install=tfp_install)

def images():
    return {
        "tf:20.03": {
            "base": "nvcr.io/nvidia/tensorflow:20.03-tf2-py3 ",
            "TFMajorVersion": 2,
            "needsContext": True,
        },
        "tf1:20.03": {
            "base": "nvcr.io/nvidia/tensorflow:20.03-tf1-py3 ",
            "TFMajorVersion": 1,
            "needsContext": True,
        },
    }
