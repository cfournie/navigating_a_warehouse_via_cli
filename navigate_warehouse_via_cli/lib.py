import enum
import os
import random
import sys

import codenamize


class ResourceClass(enum.Enum):
    SMALL = 'small'
    MEDIUM = 'medium'
    LARGE = 'large'
    XLARGE = 'xlarge'
    XXLARGE = 'xxlarge'


class Job(object):
    # pylint: disable=too-few-public-methods

    def __init__(self, resource_class, executable, inputs, output):
        self.resource_class = resource_class
        self.executable = executable
        self.inputs = inputs
        self.output = output


class Flow(object):
    # pylint: disable=too-few-public-methods

    def __init__(self, frequency, jobs):
        self.frequency = frequency  # Hours
        self.jobs = jobs


def create_path(end=None):
    adjectives = 1 if end else 2
    parts = ('/data', codenamize.codenamize(random.randint(0, sys.maxsize), adjectives, join='/'))
    if end:
        parts += (end.replace('-', '_'), )
    return os.path.join(*parts)


def create_name():
    return codenamize.codenamize(random.randint(0, sys.maxsize), adjectives=1, join='-')


def generate_job(name, potential_inputs, output=None):
    output = output if output else create_path(name)
    inputs = set(random.sample(
        potential_inputs,
        random.randint(1, min(3, len(potential_inputs)))
    ))

    return Job(
        resource_class=random.choice(list(ResourceClass)),
        executable=os.path.join(f'jobs/{name}.py'),
        inputs=inputs,
        output=output
    )


def generate_schedule(
        min_initial_datasets=10,
        max_initial_datasets=30,
        max_initial_jobs_per_flow=3,
        max_end_jobs_per_flow=4,
        min_flows=50,
        max_flows=100,
        seed=None):
    if seed:
        random.seed(seed)

    datasets = set(
        create_path() for _ in range(
            0,
            random.randint(
                min_initial_datasets,
                max_initial_datasets)))

    def generate_flow():
        initial_jobs = dict()
        initial_datasets = set()
        jobs = dict()

        # Generate jobs that accept initial dataset inputs
        for _ in range(random.randint(1, max_initial_jobs_per_flow)):
            name = create_name()
            job = generate_job(name, potential_inputs=datasets)
            initial_jobs[name] = job
            initial_datasets.add(job.output)

        # Generate pairs of jobs that accept flow inputs (one job and an
        # associated loader)
        datasets_used = set()
        end_jobs = random.randint(1, max_end_jobs_per_flow)
        for last in map(lambda i: i == 0, reversed(range(0, end_jobs))):
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
                name=f'load-{name}',
                potential_inputs=(job.output,),
                output=f'scheme.{name}@database'
            )
            jobs[f'load-{name}'] = loader

        jobs.update(initial_jobs)
        return Flow(
            frequency=random.randint(1, 24),
            jobs=jobs
        )

    flows = dict()
    for _ in range(0, random.randint(min_flows, max_flows)):
        flows[create_name()] = generate_flow()
    return flows
