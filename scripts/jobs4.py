import signal
import sys

import navigate_warehouse_via_cli.lib as lib


# pylint: disable=invalid-name
if __name__ == '__main__':
    # Handle the SIGPIPE signal by exiting gracefully when receiving it. This
    # occurs when our output is piped to `head`
    def handle_sigpipe(_, __):
        sys.stderr.close()
        sys.exit(0)
    signal.signal(signal.SIGPIPE, handle_sigpipe)

    # Write table to stdout
    flows = lib.generate_schedule(seed=2)
    for flow_name, flow in flows.items():
        for job_name, job in flow.jobs.items():
            print('\t'.join((
                flow_name,
                str(flow.frequency),
                job_name,
                job.resource_class.value,
                job.executable,
                job.output
            )))
