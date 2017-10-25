import random

import faker
import lib
import pytest


@pytest.fixture
def yaml_schedule():
    return '''
flow-a:
  monitoring: active
  owner: team@example.com
  frequency: 2h
  slo: 4h
  sub-flow:
    flow: flow-b
  build:
    resource_class: medium
    executable: jobs/builder-a.py
    command_options:
      input-a: /data/raw/input_a
      output: /var/data/facts/output_a
    dependencies:
      - sub-flow
  load:
    resource_class: large
    executable: jobs/loader.py
    command_options:
      path: /var/data/facts/output_a
      table: business.output_a
      destination: presto
    dependencies:
      - build

flow-b:
  monitoring: passive
  owner: team@example.com
  build:
    resource_class: medium
    executable: jobs/builder-b.py
    command_options:
      input-b: /data/raw/input_a
      output: /var/data/facts/output_a
  load:
    resource_class: large
    executable: jobs/loader.py
    command_options:
      path: /var/data/facts/output_a
      table: business.output_a
      destination: presto
    dependencies:
      - build
'''.lstrip()



def test_read_schedule(yaml_schedule, tmpdir):
    schedule_file = tmpdir.join('schedule.yml')
    schedule_file.write(yaml_schedule)
    
    flows = lib.read_schedule(str(schedule_file))

    assert flows.keys() == {'flow-a', 'flow-b'}

    assert flows['flow-a'].monitoring == lib.Monitoring.ACTIVE
    assert flows['flow-a'].frequency == '2h'
    assert flows['flow-a'].slo == '4h'
    assert flows['flow-a'].jobs.keys() == {'sub-flow', 'build', 'load'}

    assert flows['flow-a'].jobs['sub-flow'].name == 'flow-b'
    
    assert flows['flow-a'].jobs['build'].resource_class == 'medium'
    assert flows['flow-a'].jobs['build'].executable == 'jobs/builder-a.py'
    assert flows['flow-a'].jobs['build'].dependencies == ['sub-flow']
    assert flows['flow-a'].jobs['build'].command_options == {'input-a': '/data/raw/input_a',
                                                             'output': '/var/data/facts/output_a'}


def test_generate_schedule():
    random.seed(2)
    fake = faker.Faker('en_CA')
    fake.seed(2)
    
    flows = lib.generate_schedule(fake)

    # Does this flow exist?
    assert 'non' in flows

    # Does this job exist?
    assert 'facilis' in flows['non'].jobs

    # Does this job have sensible dependencies and other values?
    assert set(flows['non'].jobs['facilis'].dependencies) < set(flows['non'].jobs.keys())
    assert flows['non'].jobs['facilis'].command_options
    assert flows['non'].jobs['facilis'].executable
    assert flows['non'].jobs['facilis'].resource_class
    
    # Does this subflow exist and doesit refer to a real flow?
    assert 'ad' in flows['non'].jobs
    assert flows['non'].jobs['ad'].name in flows
