import modules.runas
import modules.ssh


def emit(writer, **kwargs):
    # everything is already installed, just add runas and ssh
    modules.runas.emit(writer)
    modules.ssh.emit(writer)
    writer.packages(['graphviz'])
    assert 'TFVersion' in kwargs
    tfp_install = 'tensorflow-probability'
    if kwargs['TFVersion'] <= '1.15.2':
        tfp_install = 'tensorflow-probability==0.7'
    elif kwargs['TFVersion'] <= "1.15.4":
        tfp_install = 'tensorflow-probability==0.8'
    elif kwargs['TFVersion'] <= '2.2.0':
        tfp_install = 'tensorflow-probability==0.10.1'
    else:
        tfp_install = 'tensorflow-probability'
    writer.emit("""
        RUN pip install $tfp_install fs pendulum Pillow
    """, tfp_install=tfp_install)


def images():
    return {
        "tf:20.03": {
            "base": "nvcr.io/nvidia/tensorflow:20.03-tf2-py3",
            "TFVersion": "2.1.0",
            "needsContext": True,
        },
        "tf1:20.03": {
            "base": "nvcr.io/nvidia/tensorflow:20.03-tf1-py3",
            "TFVersion": "1.15.2",
            "needsContext": True,
        },
        "tf1:20.08": {
            "base": "nvcr.io/nvidia/tensorflow:20.08-tf1-py3",
            "TFVersion": "1.15.3",
            "needsContext": True,
        },
        "tf:20.08": {
            "base": "nvcr.io/nvidia/tensorflow:20.08-tf2-py3",
            "TFVersion": "2.2.0",
            "needsContext": True,
        },
        "tf1:19.09": {
            "base": "nvcr.io/nvidia/tensorflow:19.09-py3",
            "TFVersion": "1.14.0",
            "needsContext": True,
        },
        "tf1:20.11": {
            "base": "nvcr.io/nvidia/tensorflow:20.11-tf1-py3",
            "TFVersion": "1.15.4",
            "needsContext": True,
        },
        "tf1:20.12": {
            "base": "gitlab-master.nvidia.com:5005/dl/dgx/tensorflow:20.12-tf1-py3-devel",
            "TFVersion": "1.15.4",
            "needsContext": True,
        },
        "tf1:20.12-master": {
            "base": "gitlab-master.nvidia.com:5005/dl/dgx/tensorflow:master-tf1-py3.1854369-devel",
            "TFVersion": "1.15.4",
            "needsContext": True,
        },
    }
