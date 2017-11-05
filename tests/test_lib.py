import random
import re

import navigate_warehouse_via_cli.lib as lib


def assert_path(path):
    assert path.startswith('/data/')
    assert not path.endswith('/')
    assert path.count('/') == 4
    assert all(path.lstrip('/').split('/'))


def test_create_path():
    assert_path(lib.create_path())
    assert_path(lib.create_path('my-name'))
    assert lib.create_path('my-name').endswith('/my_name')


def test_create_name():
    name = lib.create_name()
    assert name
    assert len(name.split('-')) == 2
    assert all(name.split('-'))


def test_generate_job():
    name = 'my-job'
    potential_inputs = ['input-a', 'input-b', 'input-c']
    output = 'my-output'

    # Specify output
    job = lib.generate_job(
        name=name,
        potential_inputs=potential_inputs,
        output=output
    )
    assert job.executable == 'jobs/my-job.py'
    assert job.inputs <= set(potential_inputs)
    assert job.output == output

    # Don't specify output
    job = lib.generate_job(
        name=name,
        potential_inputs=potential_inputs
    )
    assert job.executable == 'jobs/my-job.py'
    assert job.inputs <= set(potential_inputs)
    assert_path(job.output)
    assert job.output not in set(potential_inputs)


def test_generate_schedule():
    flows = lib.generate_schedule()

    # Pick a flow
    flow = random.choice(list(flows.values()))

    # Does this flow have reasonable values?
    assert flow.frequency > 0
    assert flow.jobs

    def assert_job(job):
        assert isinstance(job.resource_class, lib.ResourceClass)
        assert job.executable.endswith('.py')
        assert job.inputs
        assert job.output

    # Find a load job
    load_job = [
        job for job_name,
        job in flow.jobs.items() if job_name.startswith('load-')][0]

    # Does this load job have reasonable values?
    assert_job(load_job)
    assert re.match(r'scheme\.[a-z\-]+@database', load_job.output)

    # Find the 'end' job that created the input for this load job
    end_job = [job for job in flow.jobs.values(
    ) if job.output in load_job.inputs]
    assert len(end_job) == 1
    end_job = end_job[0]

    # Does this 'end' job have reasonable values?
    assert_job(end_job)

    # Find the 'initial' job that created the input for this 'end' job
    initial_job = [job for job in flow.jobs.values(
    ) if job.output in end_job.inputs]
    assert initial_job
    initial_job = initial_job[0]  # Pick an arbitrary end job

    # Does this 'intitial' job have reasonable values?
    assert_job(initial_job)

    # Does this initial job use any other job in this flow's output? (if so
    # it's not an 'initial' job)
    assert not initial_job.inputs & set(
        job.output for job in flow.jobs.values())
