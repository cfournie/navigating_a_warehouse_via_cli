import navigate_warehouse_via_cli.lib as lib

# pylint: disable=invalid-name

if __name__ == '__main__':
    flows = lib.generate_schedule(seed=2)
    for name, flow in flows.items():
        print(name, flow.owner, flow.frequency, flow.slo)
