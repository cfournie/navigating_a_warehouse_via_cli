import navigate_warehouse_via_cli.schedule as schedule


# pylint: disable=invalid-name
if __name__ == '__main__':
    # Write table to stdout
    flows = schedule.generate_schedule(seed=2)
    for flow in flows:
        for job in flow.jobs:
            print('\t'.join((
                flow.name,
                str(flow.frequency),
                job.name,
                job.resource_class.value,
                job.output
            )))
