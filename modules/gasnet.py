# TODO possibly add conduit option to restrict to that.
# not trivial on first sight, probably just need to run make in the conduit dir
def emit(writer, conduit='mpi'):
    writer.emit("""
        RUN mkdir -p /opt/GASNet && cd /opt/GASNet && \
        wget https://gasnet.lbl.gov/EX/GASNet-2020.3.0.tar.gz && \
        tar -zxf GASNet-*.tar.gz && \
        cd GASNet-* && \
        ./configure && make all && make install
        ENV LIBRARY_PATH="/usr/local/gasnet/lib:$${LIBRARY_PATH}"
        ENV LD_LIBRARY_PATH="/usr/local/gasnet/lib:$${LD_LIBRARY_PATH}"
        ENV CONDUIT=$conduit
    """, conduit=conduit)
