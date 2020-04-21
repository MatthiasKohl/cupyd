import os


def emit(writer, **kwargs):
    # We expect a docker with rapids installed here already
    # This means cuda and conda are installed.
    # We don't add those requirements explicitely so we can use the rapids
    # docker as base (this is a bit faster for our purposes, but we can
    # change this later such that the whole build is containerized)
    is_debug = kwargs.get('debug', False)
    legate_branch = kwargs.get('legate_branch', 'dask')
    print('Using debug build: ', is_debug, ' legate branch: ', legate_branch)
    writer.emit("""
        RUN mkdir -p "$${CONDA_PREFIX}/etc/conda/activate.d" && mkdir -p "$${CONDA_PREFIX}/etc/conda/deactivate.d/"
        COPY contexts/conda/activate_dev_env.sh "$${CONDA_PREFIX}/etc/conda/activate.d/dev_env.sh"
        COPY contexts/conda/deactivate_dev_env.sh "$${CONDA_PREFIX}/etc/conda/deactivate.d/dev_env.sh"
    """)
    writer.packages(['software-properties-common', 'zlib1g-dev', 'tmux'])
    writer.emit("""
        RUN add-apt-repository ppa:ubuntu-toolchain-r/test
    """)
    writer.packages(['gcc-7', 'g++-7'])
    writer.emit("""
        RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-7 90 --slave /usr/bin/g++ g++ /usr/bin/g++-7
        ENV CC gcc-7
        ENV CXX g++-7
    """)
    writer.condaPackages(['openblas-devel', 'graphviz'],
                         channels=['anaconda', 'conda-forge'], installOpts='-n rapids')
    writer.emit("""
        RUN source activate rapids && pip install graphviz
        RUN git clone --branch v1.0.1 https://github.com/NVIDIA/cutlass.git /opt/cutlass
        RUN git clone --branch v1.8.0 https://github.com/NVlabs/cub.git /opt/cub
    """)
    # writer.emit("""
    #    RUN source activate rapids && \\
    #        echo "Change this message for re-build!" && \\
    #        git clone -b $legate_branch https://gitlab-master.nvidia.com/mjoux/Legate.git \\
    #        /opt/legate && \\
    #        cd /opt/legate && \\
    #        python ./install.py $debug \\
    #        --cuda --with-cuda /usr/local/cuda --arch volta \\
    #        --with-openblas $CONDA_PREFIX
    #    WORKDIR /home""",
    #             # TODO arch!!
    #             user=os.getuid(),
    #             debug='--debug' if is_debug else '',
    #             legate_branch=legate_branch)
    # writer.emit("""
    #     RUN mkdir /home/mjoux/.ssh
    #     RUN echo 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDCGkaBear/Y0HH8qry0WgV4CbOcKUZZWkS3q7jDrR9xKdxoGjvmyALUfh08ANXTO27kCpZ6d+ExVJ7yhtoMoYakpIt1xvV/+/26CcGtfrZCnM8Lq7YTsWIld6MezPLi9IcbziKp6cF73RkI7WRH0TufWJ527ja4YjB0lxz3o/UaXyDkvI5nllyyC1ULnXvFyyVzUaqfEWhmsBb2Vj7CnsljSAyMhpJeVuDUoq88xShUpUn/1iHCgU4VDVUxo7IiSgVcpXY3kJhsP7p59WTdIlkwxDJpp4gi7sQmStsBIotHcj6ibTrByWAiBJEyYTgRyqsFNgKdo8bB9FTf3dVLu8Ule+MX673Wm/CUk1UbK5K33hl58FYpOu+jthbWKU6+k01UJ3D/+7qFJw81KMRfj/NPDbe6x3r68+muvKSYRM4ggv25qkqQcos2WcrNNOMSIbZUpdtECHZAUYeV3PbqAUiSKSfK0YwwswdSrcQL52emXPF8kWh7gJmDJUq2lg2ZnMVWurVj+AUAmgGfXMghwa+/eGgQefnvZL0ioyyHOJ/1zksU3hjRDDWQpTUbLSFpf7wpBJ6JDsYrkiIJXndm9++J9eB6/JN00/nYlOVlP57vOBpZCkFK/YQLeh5iOHxDYspIFbSSKIXwKx/0eaTi3ruBAFnuIAysNIj5Y0ifihjZQ== mjoux@dlcluster' >> /home/mjoux/.ssh/authorized_keys
    # """)
