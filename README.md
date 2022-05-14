# GPU-PV-Scripts
N卡的驱动文件好找，A卡不太好找。索性直接全部提取出来。
1. 创建好虚拟机, 如果还没有虚拟机可以使用CreateVmAndAddGPU-partition.ps1脚本创建
2. 获取 devcon.exe https://docs.microsoft.com/en-us/windows-hardware/drivers/devtest/devcon
3. 把devcon.exe放置到get_gpu_driver_files.py脚本目录
4. 执行 get_gpu_driver_files.py
```
python get_gpu_driver_files.py
```
5. 然后覆盖获取到的驱动文件到虚拟机的Windows目录