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
        RUN mkdir -p "/opt/conda/envs/rapids/etc/conda/activate.d" && mkdir -p "/opt/conda/envs/rapids/etc/conda/deactivate.d/"
        COPY contexts/conda/activate_dev_env.sh "/opt/conda/envs/rapids/etc/conda/activate.d/dev_env.sh"
        COPY contexts/conda/deactivate_dev_env.sh "/opt/conda/envs/rapids/etc/conda/deactivate.d/dev_env.sh"
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
    writer.condaPackages(['python-graphviz'],
                         channels=['conda-forge'], installOpts='-n rapids')
    writer.emit("""
        RUN source activate rapids && pip install graphviz
        RUN git clone --branch v1.0.1 https://github.com/NVIDIA/cutlass.git /opt/cutlass
        RUN git clone --branch v1.8.0 https://github.com/NVlabs/cub.git /opt/cub
    """)
