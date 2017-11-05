import navigate_warehouse_via_cli.lib as lib


# pylint: disable=invalid-name,duplicate-code
if __name__ == '__main__':
    flows = lib.generate_schedule(seed=2)
    for flow_name, flow in flows.items():
        for job_name, job in flow.jobs.items():
            print(
                flow_name,
                flow.frequency,
                job_name,
                job.resource_class.value,
                job.executable,
                job.inputs,
                job.output
            )
