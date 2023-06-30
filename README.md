# PEST Threadripper Settings
Notes on optimal AMD threadripper bios settings for fully loaded parallel single thread [PESTPP](https://github.com/usgs/pestpp) workloads

## The Issue
Brand new very expensive PC aimed at allowing me to run more MODFLOW models simultaneously via PESTPP got unbearably bogged down under loads of more than about 20 instances. To the point of uselessness. I badly needed to optimise the hardware for this workload.

## Test Setup Details
* Motherboard: ASUS Pro WS WRX80E-SAGE SE WiFi
* CPU: AMD Threadripper Pro 5995WX (64 core)
* RAM: All 8 slots (channels) filled (any less, we potentially choke the system):
  - Four Kingston Fury Beast 64GB (2x32GB) PC4-25600 (3200Mhz) DDR4, CL16, 16-20-20, 1.35v, XMP 2.0, 2R Dual Rank, Dual Channel Kit, Black Heatsink. Model: Model: KF432C16BBK2/64
  - Four Kingston KF432C16BBK2/32 FURY Beast Black 32GB (2x16GB) PC4-25600 (3200Mhz) DDR4, CL16, 16-20-20, 1.35v, 1Rx8 Single Rank, Dual Channel Kit, Black Heat Spreader. Model: KF432C16BBK2/32. Bought these after I started realsing I had bottleneck issues. Now I have way more ram than I need, but so be it.
* Cooling: Noctua NH-U14S TR4-SP3 (air  only). Oriented vertically, single fan pushingup  through cooler to top of case.
* Case: Fractal Design Define 7 XL E-ATX Case (tower). Nice and big, lots of space and lots of air flow. Top cover removed to allow cpu heat to be blown up out of vents on top of case (rear case fan moved to here, pulling from directly above CPU).
* Storage: 3 x Kingston KC3000 2TB PCIe 4.0 NVMe M.2 SSD. Split PESTPP workers across these evenly (ish).

## BIOS Settings
* Update to the latest available.
* Enable DOCP (xmp 2.0 equivalent). Otherwise ram runs at stock jeda settings. Can make a big difference. Bios: Ai Tweaker Menu --> DOCP --> choose your profile (max the mobo can take / your chips can do).
* Disable virtualization (unless you need it) - Bios: Advanced --> CPU Configuration --> SVM Mode = Disabled
* Disable multi-threading (SMT in asus lingo). This is quite important to PESTPP worker speed. See [here](https://www.ansys.com/content/dam/company/technology-and-solution-partners/workstation-p620-ansys-white-paper.pdf). Bios: Advanced tab --> AMD CBS-> CPU Common Options-> Performance-> CCD/Core/Thread Enablement ->Accept-> SMT control->Disabled
* NUMA per core: 4 (This is the single most critical setting! Effectively divides the 64 cores up into 4 blocks, each having dedicated memory channel access.). There's a decent explanation of this [here](https://www.ansys.com/content/dam/company/technology-and-solution-partners/workstation-p620-ansys-white-paper.pdf), and [here](https://www.anandtech.com/show/11697/the-amd-ryzen-threadripper-1950x-and-1920x-review/3). In bios: Advanced tab --> AMD CBS (down the bottom) --> DF Common Options --> Memory Addressing --> NUMA Nodes per socket --> 4
* disable BUS power saving: APBDIS set to 1 (from auto); seemed to automatically set P-State to P0 (which apparently is also wanted with APBDIS==1). Not sure this helped with PESTPP worker speed or not, but it certainly didn't slow things down. Bios: Advanced tab --> AMD CBS-> NBIO Common Options-> SMU common options --> APBDIS=1
* Enable BMC (board management interface); this allows you to set board / case fan controls, to manage temperatures. Need to plug in lan cable, then go into "Server Management" --> BMC Enabled --> BMC Network Configuration and here you will find the IP address of the BMC interface (ideally set this as a fixed IP addresss on your router too). In the OS, open a browser, and go to https://\<your BMC ip address>. Default login is admin/admin; suggest you change this once in there the first time. Set fan control to full speed (or play around with ramping curves if you want; I just jacked mine up, and it kept temps about 67 degrees at flat out loads across all cores).
  - Make sure you update the firmware from this interface to the latest (I was getting all sorts of weird alerts/noin-functioning sensors originally; now I get none and it all works nicely).

## Chipset drivers
* update to the latest. I installed Asus Armory Crate to do this.

## Process Execution (Windows 11 Pro, but applicable to Win10 etc too, and probably similar options in Linux)
When launching your PESTPP workers, use the "start /affinity <hex mask>" method, where the hex mask for each worker is one of your 64 cores. This is called "thread pinning" (see [here](https://www.ansys.com/content/dam/company/technology-and-solution-partners/workstation-p620-ansys-white-paper.pdf) for a decent description).

You could either do this upon each worker launch into a new command window (eg. "start /affinity \<your per-cpu hex mask> fire_up_a_worker.bat"), or via your PESTPP model command workflow (i.e., feed in the hex string argument upon modflow execution, eg: "start /affinity \<your per-cpu hex mask> modflow pretty_average_model.nam"). Example worker launcher with cpu hex mask affinity option [here](https://github.com/cnicol-gwlogic/pest-threadripper_settings/blob/main/startmodels.py).
