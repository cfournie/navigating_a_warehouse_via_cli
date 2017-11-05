import navigate_warehouse_via_cli.lib as lib


# pylint: disable=invalid-name,duplicate-code
if __name__ == '__main__':
    flows = lib.generate_schedule(seed=2)
    for flow in flows.values():
        for name, job in flow.jobs.items():
            print('\t'.join((
                name,
                job.resource_class.value,
                job.executable,
                job.output
            )))
