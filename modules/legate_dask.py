import os

# We expect a docker with rapids installed here already
# This means cuda and conda are installed.
# We don't add those requirements explicitely so we can use the rapids
# docker as base (this is a bit faster for our purposes, but we can
# change this later such that the whole build is containerized)
def emit(writer, **kwargs):
    writer.packages(['zlib1g-dev'])
    writer.emit("""
        RUN source activate rapids && \\
            echo "change for re-build!" && \\
            git clone -b dask https://gitlab-master.nvidia.com/mkohl/Legate.git \\
            /opt/legate && \\
            cd /opt/legate && \\
            python ./install.py \\
            --cuda --with-cuda /usr/local/cuda --arch volta
        WORKDIR /home""",
        user=os.getuid())
