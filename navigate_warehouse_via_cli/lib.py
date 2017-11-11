import enum
import itertools
import os
import random
import sys
import typing

import codenamize
import networkx as nx


class ResourceClass(enum.Enum):
    SMALL = 'small'
    MEDIUM = 'medium'
    LARGE = 'large'
    XLARGE = 'xlarge'
    XXLARGE = 'xxlarge'


class Job(typing.NamedTuple):
    name: str
    resource_class: ResourceClass
    executable: str
    inputs: typing.Iterable[str]
    output: str


class Flow(typing.NamedTuple):
    name: str
    frequency: int  # Hours
    jobs: typing.Iterable[Job]


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
    inputs = random.sample(
        potential_inputs,
        random.randint(1, min(3, len(potential_inputs)))
    )
    return Job(
        name=name,
        resource_class=random.choice(list(ResourceClass)),
        executable=os.path.join(f'jobs/{name}.py'),
        inputs=inputs,
        output=output
    )


def generate_schedule(
        min_initial_datasets=5,
        max_initial_datasets=10,
        max_initial_jobs_per_flow=3,
        max_end_jobs_per_flow=4,
        min_flows=70,
        max_flows=90,
        seed=None):
    if seed:
        random.seed(seed)

    datasets = random.randint(min_initial_datasets, max_initial_datasets)
    datasets = list(create_path() for _ in range(0, datasets))

    flows = []

    def generate_flow(flows, datasets):
        initial_jobs = []
        initial_datasets = []

        # Generate jobs that accept initial dataset inputs
        for _ in range(random.randint(1, max_initial_jobs_per_flow)):
            job = generate_job(
                name=create_name(initial_jobs),
                potential_inputs=datasets,
                output=create_path(
                    paths=itertools.chain(
                        datasets, initial_datasets))
            )
            initial_jobs.append(job)
            initial_datasets.append(job.output)

        # Generate pairs of jobs that accept flow inputs (one job and an
        # associated loader)
        jobs = []
        for _ in range(0, random.randint(1, max_end_jobs_per_flow)):
            # Job that accepts flow dataset inputs
            name = create_name(itertools.chain(initial_jobs, jobs))
            job = generate_job(
                name=name,
                potential_inputs=initial_datasets,
                output=create_path(
                    paths=itertools.chain(
                        datasets, initial_datasets))
            )
            jobs.append(job)
            datasets.append(job.output)

            # Load this output (don't register it as an eligible input)
            loader = generate_job(
                name=f'load-{name}',
                potential_inputs=(job.output,),
                output=f'scheme.{name}@database'
            )
            jobs.append(loader)

        # Fold in initial jobs and their datasets
        jobs.extend(initial_jobs)
        datasets.extend(initial_datasets)

        # Create flow
        return Flow(
            name=create_name(flows),
            frequency=random.randint(1, 24),
            jobs=jobs
        )

    for _ in range(0, random.randint(min_flows, max_flows)):
        flows.append(generate_flow(flows, datasets))
    return flows


def create_graph(flows):
    graph = nx.DiGraph()
    for flow in flows:
        for job in flow.jobs:
            for _input in job.inputs:
                graph.add_edge(_input, job.output)
    return graph


def create_downstream(graph):
    for dataset in graph.nodes():
        downstream_datasets = set(nx.bfs_tree(
            graph, source=dataset, reverse=False
        ).nodes())
        downstream_datasets.remove(dataset)
        for downstream_dataset in downstream_datasets:
            yield dataset, downstream_dataset


def draw(graph, path):
    agraph = nx.nx_agraph.to_agraph(graph)
    agraph.layout('dot')
    agraph.draw(path)
