$isopath = "System Install Iso Path"
$vhdpath = "VMVhdx Save Path"
$vmpath = "Vm Save Path"
$vmname = "VmName"
New-VM -Name $vmname -MemoryStartupBytes 8GB -BootDevice VHD -NewVHDPath $vhdpath -Path $vmpath -NewVHDSizeBytes 128GB -Generation 2 -Switch "Default Switch"
Set-VM -Name  $vmname -CheckpointType Disabled
Set-VMMemory $vmname -DynamicMemoryEnabled $true
Add-VMDvdDrive -VMName  $vmname -Path $isopath
Set-VMFirmware -VMName $vmname -EnableSecureBoot Off -FirstBootDevice (Get-VMDvdDrive -VMName $vmname)[0]
Add-VMGpuPartitionAdapter -VMName $vmname
Set-VMGpuPartitionAdapter -VMName $vmname -MinPartitionVRAM 80000000 -MaxPartitionVRAM 100000000 -OptimalPartitionVRAM 100000000 -MinPartitionEncode 80000000 -MaxPartitionEncode 100000000 -OptimalPartitionEncode 100000000 -MinPartitionDecode 80000000 -MaxPartitionDecode 100000000 -OptimalPartitionDecode 100000000 -MinPartitionCompute 80000000 -MaxPartitionCompute 100000000 -OptimalPartitionCompute 100000000
Set-VM -GuestControlledCacheTypes $true -VMName $vmname
Set-VM -LowMemoryMappedIoSpace 1Gb -VMName $vmname
Set-VM -HighMemoryMappedIoSpace 32GB -VMName $vmname
Start-VM -Name $vmname