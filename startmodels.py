import os, math, subprocess


start = 1 # worker1 (for incrementing worker{n} folders)
end = 17 # start + n workers
step = 1
offset = 32 # start cpu (base0). If workers have been started on other disks (and therefore CPUs / affinities), increment this accordingly
# ^^ eg if 42 workers have already been loaded on cpus, this should be 42.
# But on big threadrippers (64core), there is benefit in only loading up some of node0 and node1 cpus
# - eg 12 or 14 of the 16 - I am still testing the break point)
# (this is assuming you are using numa nodes=4 in your bios, which is recommended).
# The reason for this is (I think) the larger distance from those node0/node1 cpus to the memory controller than that from nodes2 and 3. Nodes 0 and 1 seem to more easily choke.
# So for example, it is best (fastest parallel runs) to use say core2-->15 on node0, 18-->31 on node1,
# and then say 33-47 on node2 and 49-63 on node4. There appears to be some speed benefit in unloading nodes 2 and 3 by 1 each.

cpus = list(range(offset, end - start + offset, step))
print(cpus, len(cpus))
bind_per_core = True
for i,ii in enumerate(range(start, start + len(cpus))): #range(start,end,step):
    n = cpus[i] #i - 1 + offset
    if bind_per_core:
        print('cpu: ',n, 'hex: ', hex(2**n))
        print("executing", f"start /affinity {hex(2**n)[2:]} ##runWorker_local.bat")
        print(f"in ..\\..\\..\\Worker{ii}\\pest\\angv7tr12u_p2")
        subprocess.Popen(
            f"start /affinity {hex(2**n)[2:]} ##runWorker_local.bat",
            cwd=f'..\\..\\..\\Worker{ii}\\pest\\angv7tr12u_p2',
            shell=True,stdin=None,stdout=None,stderr=None,
            close_fds=True)
    else:
        print("executing", f"start  ##runWorker_local.bat")
        print(f"in ..\\..\\..\\Worker{ii}\\pest\\angv7tr12u_p2")
        subprocess.Popen(
            f"start  ##runWorker_local.bat",
            cwd=f'..\\..\\..\\Worker{ii}\\pest\\angv7tr12u_p2',
            shell=True,stdin=None,stdout=None,stderr=None,
            close_fds=True)
