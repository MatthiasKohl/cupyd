import os

# We expect a docker with rapids installed here already
# This means cuda and conda are installed.
# We don't add those requirements explicitely so we can use the rapids
# docker as base (this is a bit faster for our purposes, but we can
# change this later such that the whole build is containerized)
def emit(writer, **kwargs):
    is_debug = kwargs.get('debug', False)
    legate_branch = kwargs.get('legate_branch', 'dask')
    print('Using debug build: ', is_debug, ' legate branch: ', legate_branch)
    writer.packages(['zlib1g-dev'])
    writer.condaPackages(['gxx_linux-64=7.3.0', 'gcc_linux-64=7.3.0', 'gfortran_linux-64=7.3.0', 'openblas-devel'],
        channels=['anaconda', 'conda-forge'],
        installOpts='-n rapids')
    writer.emit("""
        RUN git clone --branch v1.0.1 https://github.com/NVIDIA/cutlass.git /opt/cutlass
    """)
    writer.emit("""
        RUN ln -s /opt/conda/envs/rapids/bin/x86_64-conda_cos6-linux-gnu-gcc /usr/local/cuda/bin/gcc
        RUN ln -s /opt/conda/envs/rapids/bin/x86_64-conda_cos6-linux-gnu-g++ /usr/local/cuda/bin/g++
        RUN ln -s /opt/conda/envs/rapids/bin/x86_64-conda_cos6-linux-gnu-gfortran /usr/local/cuda/bin/gfortran
        RUN source activate rapids && \\
            echo "Change this message for re-build!" && \\
            git clone -b $legate_branch https://gitlab-master.nvidia.com/mjoux/Legate.git \\
            /opt/legate && \\
            cd /opt/legate && \\
            python ./install.py $debug \\
            --cuda --with-cuda /usr/local/cuda --arch volta \\
            --with-openblas /opt/conda/envs/rapids/
        WORKDIR /home""",
        # TODO arch!!
        user=os.getuid(),
        debug='--debug' if is_debug else '',
        legate_branch=legate_branch)
