from __future__ import absolute_import
import modules.cuda_dev
import modules.cuml_dev
import modules.conda_ml_env
import modules.runas
import modules.ssh
import modules.openmpi
from itertools import product


def emit(writer, **kwargs):
    if "cudaVersionFull" not in kwargs:
        raise Exception("'cudaVersionFull' is mandatory!")
    cudaVersionFull = kwargs["cudaVersionFull"]
    modules.cuda_dev.emit(writer, cudaVersionFull, kwargs["base"])
    modules.runas.emit(writer)
    modules.ssh.emit(writer)
    modules.conda_ml_env.emit(writer)
    modules.openmpi.emit(writer, devBuild=False, ompiVersion="4.0.2")
    modules.cuml_dev.emit(writer, **kwargs)


def get_params(rapidsVersion, cudaVersionFull):
    return {"cudaVersionFull": cudaVersionFull,
            "base": "ubuntu:16.04",
            "needsContext": True,
            "rapidsVersion": rapidsVersion}


def images():
    return {'ml-dev-{}:{}'.format(rapidsVersion, '.'.join(cudaFull.split('.')[:2])): get_params(rapidsVersion, cudaFull)
            for rapidsVersion, cudaFull in product(
                ['0.12', '0.13', '0.14'],
                ['10.0.130', '10.1.105', '10.2.89'])
            }
