#!/usr/bin/env python

"""
Insert GPU attributes to ClassAd.

Uses nvidia-ml-py3 to query GPU stats such as load and memory usage.

Uses daemon ClassAd hooks:
https://htcondor.readthedocs.io/en/v8_9_3/misc-concepts/hooks.html#daemon-classad-hooks


For an execute machine with 4 GPUs, example insertion:

GPUsLoad=0.9 # 1.0 == 100%
GPUsMemory=0.1 # GPU memory in MB available
SlotId=1
-s1
...etc...
-s2
...etc...
-s3
...etc...
-s4
- update:true

Jobs can now use the requirements field to select a GPU:

requirements = (GPUsLoad <= 0.75)
requirements = (GPUsMemory >= 2048)

where GPUsLoad is GPU utilization. 1.0 is 100% load
and GPUsMemory is memory free in MB.
"""


from __future__ import absolute_import, division, print_function

import sys

try:
    from pynvml import *
except ImportError:
    print("Is nvidia-ml-py3 installed? pip3 install nvidia-ml-py3")
    print("Ref: https://docs.fast.ai/dev/gpu.html#accessing-nvidia-gpu-info-programmatically")
    sys.exit(1)


def info():
    """
    Reference: 
    - https://forums.fast.ai/t/show-gpu-utilization-metrics-inside-training-loop-without-subprocess-call/26594
    - https://forums.fast.ai/t/show-gpu-utilization-metrics-inside-training-loop-without-subprocess-call/26594/6
    """
    nvmlInit()
    try:
        deviceCount = nvmlDeviceGetCount()
        
        load = []
        memory = []
        for i in range(deviceCount):
            handle = nvmlDeviceGetHandleByIndex(i)
            #print("Device", i, ":", nvmlDeviceGetName(handle))

            res = nvmlDeviceGetUtilizationRates(handle)
            load.append(int(res.gpu)) # GPU load from (int) 0 to 100
            #load.append(res.gpu / 100.0)
            #print(f'gpu: {res.gpu}%, gpu-mem: {res.memory}%')

            mem_res = nvmlDeviceGetMemoryInfo(handle)
            memory.append(int((mem_res.total - mem_res.used) / (1024**2))) # Available GPU memory in (int) MiB
            #memory.append(mem_res.used / mem_res.total) # 0 ... 1.0
            #print(f'mem: {mem_res.used / (1024**2)} (GiB)') # usage in GiB
            #print(f'mem: {100 * (mem_res.used / mem_res.total):.3f}%') # percentage usage

        return load, memory
    except NVMLError as error:
        print(error)


load, memory = info()
#print(type(load))
#print(type(memory))

for k, v in enumerate(load):
    print("GPUsLoad={}".format(v))
    print("GPUsMemory={}".format(memory[k]))
    print("SlotId={}".format(k+1))
    print("-s{}".format(k+1))

# Default 100% load and no available memory
print("GPUsLoad=100")
print("GPUsMemory=0")

print("- update:true")
