# M1 PMU GEN

Python script to generate some tables in `drivers/perf/apple_m1_cpu_pmu.c` file for Linux PMU Driver.

This script requires files from `/usr/share/kpep` in macOS to generate the file.

## Usage

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

## References

[Apple Silicon CPU Optimization Guide-Chapter 6. Performance Monitoring](https://developer.apple.com/download/apple-silicon-cpu-optimization-guide/)