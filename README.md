# M1 PMU GEN

Python script to generate some tables for Apple Silicon Macs to profiling with Linux perf.

This script requires files from `/usr/share/kpep` in macOS to generate the file.

## Usage - Generate the Linux perf event JSON table

Assume you have copied `/usr/share/kpep` from macOS to Linux in the same directory.

And you have cloned the Linux kernel source code and set environment variable `PATH_TO_LINUX` to the path of the kernel source code.

A optional step is to download the [Apple Silicon CPU Optimization Guide](https://developer.apple.com/download/apple-silicon-cpu-optimization-guide/) to generate the event descriptions which require Apple Developer account. If you don't have this file, the script will use the event name as the description.

```bash
./gen_perf_patch.py -a ~/Downloads/Apple-Silicon-CPU-Optimization-Guide.pdf -w a14 a15 > $PATH_TO_LINUX/apple_pmu.patch
cd $PATH_TO_LINUX
patch -p1 < apple_pmu.patch
cd tools/perf
make -j `nproc`
```

Then you will get a perf in current folder with the new events:

```console
$ ./perf list
List of pre-defined events (to be used in -e or -M):

  cpu-cycles OR cycles                               [Hardware event]
  instructions                                       [Hardware event]
  alignment-faults                                   [Software event]
  bpf-output                                         [Software event]
  cgroup-switches                                    [Software event]
  context-switches OR cs                             [Software event]
  cpu-clock                                          [Software event]
  cpu-migrations OR migrations                       [Software event]
  dummy                                              [Software event]
  emulation-faults                                   [Software event]
  major-faults                                       [Software event]
  minor-faults                                       [Software event]
  page-faults OR faults                              [Software event]
  task-clock                                         [Software event]
  duration_time                                      [Tool event]
  user_time                                          [Tool event]
  system_time                                        [Tool event]
  cycles OR apple_firestorm_pmu/cycles/              [Kernel PMU event]
  instructions OR apple_firestorm_pmu/instructions/  [Kernel PMU event]
  cycles OR apple_icestorm_pmu/cycles/               [Kernel PMU event]
  instructions OR apple_icestorm_pmu/instructions/   [Kernel PMU event]

core imp def:
  atomic_xxxxxx
....
```

Enjoy profiling your Apple Silicon Macs in Linux!

## Usage - Generate the PMU Driver

On macOS:

```bash
./gen_driver.py /usr/share/kpep/a14.plist m1
```

You will get something like this:

```c
enum m1_pmu_events {
	M1_PMU_PERFCTR_...
...
	M1_PMU_CFG_COUNT_KERNEL					= BIT(9),
};
static const u16 m1_pmu_event_affinity[M1_PMU_PERFCTR_LAST + 1] = {
	[0 ... M1_PMU_PERFCTR_LAST]				= ANY_BUT_0_1,
	[M1_PMU_PERFCTR_...
...
	[M1_PMU_PERFCTR_UNKNOWN_fd]				= ONLY_2_4_6,
};
```

Note: This is only to generate register definitions and affinity for the events in PMU driver. When the affinity table in the kernel is correct, you don't need to generate it and compile the kernel.

## Why we need this?

The definition of the Apple PMU events is not in the Linux kernel source code, but we can find the event name, event code, and event affinity to each PMU counter in the `/usr/share/kpep` directory in macOS. The event descriptions are in the [Apple Silicon CPU Optimization Guide](https://developer.apple.com/download/apple-silicon-cpu-optimization-guide/).

However, because of the license issue, we can't directly submit this information to the Linux kernel source code. I have consulted the Apple Legal Team but haven't gotten a response yet.

Thus, for now, having a script to generate the event definitions and descriptions for the Linux PMU driver and perf tool will be helpful for the community.

## References

[Apple Silicon CPU Optimization Guide-Chapter 6. Performance Monitoring](https://developer.apple.com/download/apple-silicon-cpu-optimization-guide/)
