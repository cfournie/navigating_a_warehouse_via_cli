import signal
import sys

import navigate_warehouse_via_cli.lib as lib


# pylint: disable=invalid-name
if __name__ == '__main__':
    # Handle the SIGPIPE signal by exiting gracefully when receiving it. This
    # occurs when our output is piped to `head`
    def handle_sigpipe(_, __):
        sys.exit(0)
    signal.signal(signal.SIGPIPE, handle_sigpipe)

    # Output jobs
    flows = lib.generate_schedule(seed=2)
    for flow in flows.values():
        for name, job in flow.jobs.items():
            print('\t'.join((
                name,
                job.resource_class.value,
                job.executable,
                job.output
            )))
