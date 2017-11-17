import random
import re
import sys
import unittest.mock as mock

import navigate_warehouse_via_cli.lib as lib
import pytest


def assert_path(path):
    assert path.startswith('/data/')
    assert not path.endswith('/')
    assert path.count('/') == 3
    assert all(path.lstrip('/').split('/'))


def test_create_path():
    assert_path(lib.create_path())
    assert_path(lib.create_path('my-name'))
    assert lib.create_path('my-name').endswith('/my_name')

    # Are the paths unique?
    with mock.patch('random.randint') as mock_randint:
        mock_randint.side_effect = [1, 1, 2]
        path1 = lib.create_path()
        path2 = lib.create_path(paths=(path1,))
        assert path1 != path2
        mock_randint.assert_has_calls(
            [mock.call(0, sys.maxsize)] * 3
        )


def test_create_name():
    name = lib.create_name()
    assert name
    assert len(name.split('-')) == 1
    assert all(name.split('-'))

    # Are the names unique?
    class Named(object):
        # pylint: disable=too-few-public-methods
        def __init__(self, name):
            self.name = name
    with mock.patch('random.randint') as mock_randint:
        mock_randint.side_effect = [1, 1, 2]
        name1 = lib.create_name()
        name2 = lib.create_name(named_objects=(Named(name1),))
        assert name1 != name2
        mock_randint.assert_has_calls(
            [mock.call(0, sys.maxsize)] * 3
        )


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
    assert set(job.inputs) <= set(potential_inputs)
    assert job.output == output


def test_generate_schedule():
    flows = lib.generate_schedule()

    # Pick a flow
    flow = random.choice(list(flows))

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
        job for job in flow.jobs if job.name.startswith('load-')][0]

    # Does this load job have reasonable values?
    assert_job(load_job)
    assert re.match(r'[a-z]+\.[a-z]+@db', load_job.output)

    # Find the 'end' job that created the input for this load job
    end_job = [job for job in flow.jobs if job.output in load_job.inputs]
    assert len(end_job) == 1
    end_job = end_job[0]

    # Does this 'end' job have reasonable values?
    assert_job(end_job)

    # Find the 'initial' job that created the input for this 'end' job
    initial_job = [job for job in flow.jobs if job.output in end_job.inputs]
    assert initial_job
    initial_job = initial_job[0]  # Pick an arbitrary end job

    # Does this 'intitial' job have reasonable values?
    assert_job(initial_job)

    # Does this initial job use any other job in this flow's output? (if so
    # it's not an 'initial' job)
    assert not set(initial_job.inputs) & set(job.output for job in flow.jobs)

    # Are there any duplicate output paths?
    outputs = set()
    for flow in flows:
        for job in flow.jobs:
            assert job.output not in outputs
            outputs.add(job.output)

    # Are there any duplicate flow.job names?
    flow_jobs = set()
    for flow in flows:
        for job in flow.jobs:
            flow_job = f'{flow.name}.{job.name}'
            assert flow_job not in flow_jobs
            flow_jobs.add(flow_job)


def test_generate_schedule_multiple_times():
    flows = lib.generate_schedule(seed=2)
    assert flows == lib.generate_schedule(seed=2)
    assert flows != lib.generate_schedule(seed=3)


@pytest.fixture
def graph():
    return lib.create_graph((
        lib.Flow(name=None, frequency=None, jobs=(
            lib.Job(
                name=None, resource_class=None, executable=None,
                inputs=('raw-a', 'raw-b'),
                output='joined-ab'
            ),
            lib.Job(
                name=None, resource_class=None, executable=None,
                inputs=('raw-b', 'raw-c'),
                output='joined-bc'
            )
        )),
        lib.Flow(name=None, frequency=None, jobs=(
            lib.Job(
                name=None, resource_class=None, executable=None,
                inputs=('joined-ab', 'joined-bc'),
                output='joined-abc'
            ),
        ))
    ))


def test_create_graph(graph):
    assert set(graph.nodes()) == set([
        'raw-a',
        'raw-b',
        'raw-c',
        'joined-ab',
        'joined-bc',
        'joined-abc'
    ])
    assert set(graph.edges()) == set([
        ('raw-a', 'joined-ab'),
        ('raw-b', 'joined-ab'),
        ('raw-b', 'joined-bc'),
        ('raw-c', 'joined-bc'),
        ('joined-ab', 'joined-abc'),
        ('joined-bc', 'joined-abc')
    ])


def test_create_downstream(graph):
    assert set(lib.create_downstream(graph)) == set([
        ('raw-a', 'joined-ab'),
        ('raw-a', 'joined-abc'),
        ('raw-b', 'joined-ab'),
        ('raw-b', 'joined-abc'),
        ('raw-b', 'joined-bc'),
        ('raw-c', 'joined-abc'),
        ('raw-c', 'joined-bc'),
        ('joined-ab', 'joined-abc'),
        ('joined-bc', 'joined-abc')
    ])


def test_draw(graph, tmpdir):
    path = tmpdir.join('graph.dot')
    lib.draw(graph, str(path))
    assert path.exists()
    assert path.read()
