# htcondor

HTCondor configuration for GPU jobs

Tested with Ubuntu 16.04 and HTCondor v8.9.3.

## Installation

1. Clone.
2. Symlink to ```/etc/condor```
3. ```sudo systemctl restart condor```
4. Depending on the role of each machine, remove the unwanted role file from ```./config.d/```.
5. For exec's, copy [./scripts/gpu_classad.py](./scripts/gpu_classad.py) to ```$(LIBEXEC)/```.

## Examples

See examples [readme](./examples/examples.md).
