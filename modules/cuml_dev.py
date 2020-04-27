import modules.cuda
import os
import shutil
import subprocess
import tempfile


# very naive yaml parser because we cannot install any python packages directly on machines
def load_env(filename):
    with open(filename) as f:
        lines = [x.rstrip() for x in f.readlines()]
    i_channels = next(i for i, line in enumerate(lines) if line == 'channels:')
    channels = []
    while True:
        i_channels += 1
        if i_channels >= len(lines):
            break
        line = lines[i_channels]
        if not line.startswith('- '):
            break
        channels.append('"{}"'.format(line[2:]))
    i_deps = next(i for i, line in enumerate(lines) if line == 'dependencies:')
    deps, pip_packages = [], []
    while True:
        i_deps += 1
        if i_deps >= len(lines):
            break
        line = lines[i_deps]
        line_s = line.strip()
        if not line_s.startswith('- '):
            break
        if 'pip:' in line:
            continue
        if line_s != line:
            pip_packages.append(line_s[2:])
            continue
        deps.append('"{}"'.format(line[2:]))
    return channels, deps, pip_packages


def emit(writer, **kwargs):
    if "rapidsVersion" not in kwargs:
        raise Exception("'rapidsVersion' is mandatory!")
    rapidsVersion = kwargs["rapidsVersion"]
    cudaVersion = '.'.join(kwargs["cudaVersionFull"].split('.')[:2])
    with tempfile.TemporaryDirectory() as cuml_dir:
        print('Cloning rapidsai/cuml to', cuml_dir, '. This may take a while...')
        subprocess.check_call(
            ['git', 'clone', '-b', 'branch-{}'.format(rapidsVersion), 'https://github.com/rapidsai/cuml.git', cuml_dir])
        print('Cloning rapidsai/cuml done.')
    channels, deps, pip_packages = load_env(
        os.path.join(cuml_dir, 'conda', 'environments', 'cuml_dev_cuda{}.yml'.format(cudaVersion)))
    writer.condaPackages(deps, channels=channels)
    writer.emit("""ENV CONDA_PREFIX=/opt/conda""")
    if pip_packages:
        writer.emit("""RUN pip install {}""".format(' '.join(pip_packages)))
