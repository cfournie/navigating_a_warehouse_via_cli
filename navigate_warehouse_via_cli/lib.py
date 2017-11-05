import enum
import itertools
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

    def __init__(self, name, resource_class, executable, inputs, output):
        self.name = name
        self.resource_class = resource_class
        self.executable = executable
        self.inputs = inputs
        self.output = output


class Flow(object):
    # pylint: disable=too-few-public-methods

    def __init__(self, name, frequency, jobs):
        self.name = name
        self.frequency = frequency  # Hours
        self.jobs = jobs


def create_path(end=None, paths=None):
    def _create_path():
        adjectives = 1 if end else 2
        parts = (
            '/data',
            codenamize.codenamize(
                random.randint(0, sys.maxsize), adjectives, join='/'
            )
        )
        if end:
            parts += (end.replace('-', '_'), )
        return os.path.join(*parts)
    # Enforce uniqueness
    path = _create_path()
    while path in (path for path in paths or []):
        path = _create_path()
    return path


def create_name(named_objects=None):
    def _create_name():
        return codenamize.codenamize(
            random.randint(0, sys.maxsize), adjectives=1, join='-'
        )
    # Enforce uniqueness
    name = _create_name()
    while name in (obj.name for obj in named_objects or []):
        name = _create_name()
    return name


def generate_job(name, potential_inputs, output):
    inputs = set(random.sample(
        potential_inputs,
        random.randint(1, min(3, len(potential_inputs)))
    ))
    return Job(
        name=name,
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

    datasets = random.randint(min_initial_datasets, max_initial_datasets)
    datasets = set(create_path() for _ in range(0, datasets))

    flows = set()

    def generate_flow(flows, datasets):
        initial_jobs = set()
        initial_datasets = set()

        # Generate jobs that accept initial dataset inputs
        for _ in range(random.randint(1, max_initial_jobs_per_flow)):
            job = generate_job(
                name=create_name(initial_jobs),
                potential_inputs=datasets,
                output=create_path(
                    paths=itertools.chain(
                        datasets, initial_datasets))
            )
            initial_jobs.add(job)
            initial_datasets.add(job.output)

        # Generate pairs of jobs that accept flow inputs (one job and an
        # associated loader)
        jobs = set()
        datasets_used = set()
        end_jobs = random.randint(1, max_end_jobs_per_flow)
        for last in map(lambda i: i == 0, reversed(range(0, end_jobs))):
            # Job that accepts flow dataset inputs
            name = create_name(itertools.chain(initial_jobs, jobs))
            job = generate_job(
                name=name,
                potential_inputs=initial_datasets,
                output=create_path(
                    paths=itertools.chain(
                        datasets, initial_datasets))
            )
            jobs.add(job)
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
            jobs.add(loader)

        # Fold in initial jobs and their datasets
        jobs |= initial_jobs
        datasets |= initial_datasets

        # Create flow

        return Flow(
            name=create_name(flows),
            frequency=random.randint(1, 24),
            jobs=jobs
        )

    for _ in range(0, random.randint(min_flows, max_flows)):
        flows.add(generate_flow(flows, datasets))
    return flows
