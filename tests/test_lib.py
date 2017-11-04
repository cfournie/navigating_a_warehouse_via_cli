import random

import faker
import navigate_warehouse_via_cli.lib as lib
import pytest


@pytest.fixture
def random_seed():
    random.seed(2)

pytestmark = pytest.mark.usefixtures("random_seed")


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
    assert job.inputs == {'input-a',}
    assert job.output == 'my-output'

    # Don't specify output
    job = lib.generate_job(
        name='my-job',
        potential_inputs=['input-a', 'input-b', 'input-c'],
    )
    assert job.executable == 'jobs/my-job.py'
    assert job.inputs == {'input-a', 'input-c',}
    assert job.output == '/data/alleged/hotel/my_job'


def test_generate_schedule():
    schedule = lib.generate_schedule(
        min_initial_datasets=2,
        max_initial_datasets=2,
        max_initial_jobs_per_flow=2,
        max_end_jobs_per_flow=2,
        min_flows=1,
        max_flows=1
    )
    assert {
        flow_name: {
            **flow.__dict__, **{'jobs': {job_name: job.__dict__ for job_name, job in flow.jobs.items()}}
        } for flow_name, flow in schedule.items()} == {
            'wretched-object': {
                'frequency': '23h',
                'monitoring': lib.Monitoring.OFF,
                'owner': 'few-size@example.com',
                'slo': '23h',
                'jobs': {
                    'goofy-forever': {
                        'executable': 'jobs/goofy-forever.py',
                        'inputs': {'/data/aspiring/brawny/cloud'},
                        'output': '/data/ethereal/item/goofy_forever',
                        'resource_class': 'xxlarge'
                    },
                    'annoyed-morning': {
                        'executable': 'jobs/annoyed-morning.py',
                        'inputs': {'/data/ethereal/item/goofy_forever'},
                        'output': '/data/pricey/appearance/annoyed_morning',
                        'resource_class': 'large'
                    },
                    'eager-confidence': {
                        'executable': 'jobs/eager-confidence.py',
                        'inputs': {'/data/ethereal/item/goofy_forever'},
                        'output': '/data/tense/protection/eager_confidence',
                        'resource_class': 'medium'
                    },
                    'load-annoyed-morning': {
                        'executable': 'jobs/load-annoyed-morning.py',
                        'inputs': {'/data/pricey/appearance/annoyed_morning'},
                        'output': 'scheme.annoyed-morning@database',
                        'resource_class': 'medium'
                    },
                    'load-eager-confidence': {
                        'executable': 'jobs/load-eager-confidence.py',
                        'inputs': {'/data/tense/protection/eager_confidence'},
                        'output': 'scheme.eager-confidence@database',
                        'resource_class': 'xxlarge'
                    }
                }
            }
        }


def test_generate_schedule_large():
    flows = lib.generate_schedule()

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
