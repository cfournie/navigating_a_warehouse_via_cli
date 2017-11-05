import navigate_warehouse_via_cli.lib as lib


# pylint: disable=invalid-name,duplicate-code
if __name__ == '__main__':
    flows = lib.generate_schedule(seed=2)
    for flow in flows:
        for job in flow.jobs:
            print(
                flow.name,
                flow.frequency,
                job.name,
                job.resource_class.value,
                job.executable,
                job.inputs,
                job.output
            )
