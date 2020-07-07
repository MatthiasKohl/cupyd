def emit(writer):
    writer.packages(["software-properties-common", "python-software-properties"])
    writer.emit("""
        RUN add-apt-repository ppa:ubuntu-toolchain-r/test
    """)
    writer.packages(['gcc-7', 'g++-7'])
    writer.emit("""
        RUN update-alternatives --remove-all gcc &&                             \
            update-alternatives --remove-all g++ &&                             \
            update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-7 90 && \
            update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-7 90 && \
            update-alternatives --install /usr/bin/cc cc /usr/bin/gcc 90 &&     \
            update-alternatives --set cc /usr/bin/gcc &&                        \
            update-alternatives --install /usr/bin/c++ c++ /usr/bin/g++ 90 &&   \
            update-alternatives --set c++ /usr/bin/g++
        ENV CC gcc-7
        ENV CXX g++-7
    """)
