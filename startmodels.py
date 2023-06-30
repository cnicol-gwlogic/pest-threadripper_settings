import os, math, subprocess


start = 1 # worker1
end = 22 # n workers+1
step = 1
offset = 0 # if workers have been started on other disks on the same PC (and therefore on certain CPUs / affinities), increment this accordingly
# ^^ eg if 42 workers have already been loaded on cpus on the same machine, this should be 42.
#cpus = list(range((offset)*2,(end-1+offset)*2, 2)) # <-- this every 2nd thing is BS info. There are only 64 cores reported in win11.
cpus = list(range((offset),(end-1+offset), step))
print(cpus, len(cpus))
bind_per_core = True
for i in range(1, len(cpus)+1): #range(start,end,step):
    n = cpus[i-1] #i - 1 + offset
    if bind_per_core:
        print('cpu: ',n, 'hex: ', hex(2**n))
        print("executing", f"start /affinity {hex(2**n)[2:]} runmodel.bat")
        print(f"in Worker{i}\\input\\angv7tr12u")
        subprocess.Popen(
            f"start /affinity {hex(2**n)[2:]} runmodel.bat",
            cwd=f'Worker{i}\\input\\angv7tr12u',
            shell=True,stdin=None,stdout=None,stderr=None,
            close_fds=True)
    else:
        print("executing", f"start runmodel.bat")
        print(f"in Worker{i}\\input\\angv7tr12u")
        subprocess.Popen(
            f"start runmodel.bat",
            cwd=f'Worker{i}\\input\\angv7tr12u',
            shell=True,stdin=None,stdout=None,stderr=None,
            close_fds=True)
