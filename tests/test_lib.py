import random
import re

import navigate_warehouse_via_cli.lib as lib
import pytest


@pytest.fixture
def random_seed():
    random.seed(2)


pytestmark = (  # pylint: disable=global-variable,invalid-name
    pytest.mark.usefixtures("random_seed")
)


def test_create_path():
    assert lib.create_path() == '/data/witty/abnormal/meeting'
    assert lib.create_path('my-name') == '/data/fine/cake/my_name'


def test_create_name():
    assert lib.create_name() == 'abnormal-meeting'


def test_generate_job():
    # Specify output
    job = lib.generate_job(
        name='my-job',
        potential_inputs=['input-a', 'input-b', 'input-c'],
        output='my-output'
    )
    assert job.executable == 'jobs/my-job.py'
    assert job.inputs == {'input-a', }
    assert job.output == 'my-output'

    # Don't specify output
    job = lib.generate_job(
        name='my-job',
        potential_inputs=['input-a', 'input-b', 'input-c'],
    )
    assert job.executable == 'jobs/my-job.py'
    assert job.inputs == {'input-a', 'input-c', }
    assert job.output == '/data/alleged/hotel/my_job'


def test_generate_schedule():
    flows = lib.generate_schedule()

    # Pick a flow
    flow = random.choice(list(flows.values()))

    # Does this flow have reasonable values?
    assert isinstance(flow.monitoring, lib.Monitoring)
    assert re.match(r'[a-z\-]+@example.com', flow.owner)
    assert re.match(r'[0-9]+h', flow.frequency)
    assert re.match(r'[0-9]+h', flow.slo)
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
    assert len(initial_job) == 1
    initial_job = initial_job[0]

    # Does this 'intitial' job have reasonable values?
    assert_job(initial_job)

    # Does this initial job use any other job in this flow's output? (if so
    # it's not an 'initial' job)
    assert not initial_job.inputs & set(
        job.output for job in flow.jobs.values())
