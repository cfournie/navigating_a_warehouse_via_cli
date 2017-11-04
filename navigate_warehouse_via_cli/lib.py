import enum
import itertools
import os
import random
import sys

import yaml
import codenamize


class Monitoring(enum.Enum):
    OFF = 'off'
    PASSIVE = 'passive'
    ACTIVE = 'active'


class Job(object):

    def __init__(self, resource_class, executable, inputs, output):
        self.resource_class = resource_class
        self.executable = executable
        self.inputs = inputs
        self.output = output


class Flow(object):

    def __init__(self, owner, monitoring=None, frequency=None, slo=None, jobs=None):
        self.monitoring = monitoring if monitoring else Monitoring.OFF
        self.owner = owner
        self.frequency = frequency
        self.slo = slo
        self.jobs = jobs


def randint(a=0, b=sys.maxsize):
    return random.randint(a, b)


def create_path(end=None):
    adjectives = 1 if end else 2
    parts = ('/data', codenamize.codenamize(randint(), adjectives, join='/'))
    if end:
        parts += (end.replace('-', '_'), )
    return os.path.join(*parts)


def create_name():
    return codenamize.codenamize(randint(), adjectives=1, join='-')


def generate_job(name, potential_inputs, output=None):
    output = output if output else create_path(name)
    inputs = set(random.sample(
        potential_inputs,
        randint(1, min(3, len(potential_inputs)))
    ))

    return Job(
        resource_class=random.choice(['small', 'medium', 'large', 'xlarge', 'xxlarge']),
        executable=os.path.join('jobs', name + '.py'),
        inputs=inputs,
        output=output
    )


def generate_schedule(
        random_seed=2,
        min_initial_datasets=10,
        max_initial_datasets=30,
        max_initial_jobs_per_flow=3,
        max_end_jobs_per_flow=4,
        min_flows=50,
        max_flows=100):
    datasets = set(create_path() for _ in range(0, randint(min_initial_datasets, max_initial_datasets)))
    owners = ['%s@example.com' % create_name() for _ in range(randint(5, 10))]
             
    def generate_flow(potential_subflows):
        initial_jobs = dict()
        initial_datasets = set()
        jobs = dict()

        # Generate jobs that accept initial dataset inputs
        for _ in range(randint(1, max_initial_jobs_per_flow)):
            name = create_name()
            job = generate_job(name, potential_inputs=datasets)
            initial_jobs[name] = job
            initial_datasets.add(job.output)

        # Generate pairs of jobs that accept flow inputs (one job and an associated loader)
        datasets_used = set()
        for last in map(lambda i: i == 0, reversed(range(randint(0, max_end_jobs_per_flow)))):
            # Job that accepts flow dataset inputs
            name = create_name()
            job = generate_job(name, potential_inputs=initial_datasets)
            jobs[name] = job
            datasets.add(job.output)

            # Make sure that all flow dataset inputs are used
            datasets_used |= set(job.inputs)
            unused_datasets = initial_datasets - datasets_used
            if last and unused_datasets:
                job.inputs |= unused_datasets

            # Load this output (don't register it as an eligible input)
            loader = generate_job(
                name='load-' + name,
                potential_inputs=(job.output,),
                output='scheme.%s@database' % name
            )
            jobs['load-' + name] = loader

        jobs.update(initial_jobs)
            
        slo = randint(0, 24)
        frequency = randint(slo, 24) if slo else None
        return Flow(
            owner=random.choice(owners),
            monitoring=random.choice(list(Monitoring)),
            frequency='{}h'.format(frequency) if frequency else None,
            slo='{}h'.format(frequency) if slo else None,
            jobs=jobs
        )

    flows = dict()
    for _ in range(0, randint(min_flows, max_flows)):
        flows[create_name()] = generate_flow(list(flows.keys()))
    return flows
