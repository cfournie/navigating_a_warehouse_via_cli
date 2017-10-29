import enum
import itertools
import os
import random


import yaml
import faker


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


def generate_schedule(fake=None):
    if not fake:
        fake = faker.Faker('en_CA')

    def create_path(end=None):
        if not end:
            end = fake.word()
        return os.path.join('/data', os.path.split(fake.file_path(depth=2))[0], end)
        
    def create_datasets(a, b):
        return set(create_path() for _ in range(0, random.randint(a, b)))

    datasets = create_datasets(10, 30)
    owners = [fake.safe_email() for _ in range(0, random.randint(5, 10))]
     
    def generate_job(name, potential_inputs, output=None):
        output = output if output else create_path(name)
        inputs = set(random.sample(
            potential_inputs,
            random.randint(1, min(3, len(potential_inputs)))
        ))
        
        return Job(
            resource_class=random.choice(['small', 'medium', 'large', 'xlarge', 'xxlarge']),
            executable=os.path.join('jobs', name + '.py'),
            inputs=inputs,
            output=output
        ), output
        
    def generate_flow(potential_subflows):
        initial_jobs = dict()
        initial_datasets = set()
        jobs = dict()

        # Generate 1-3 jobs that accept global dataset inputs
        for _ in range(0, random.randint(1, 3)):
            name = fake.word()
            job, output = generate_job(name, potential_inputs=datasets)
            initial_jobs[name] = job
            initial_datasets.add(output)

        # Generate 1-3 pairs of jobs that accept flow inputs (on job and an associated loader)
        datasets_used = set()
        for last in map(lambda i: i == 0, reversed(range(0, random.randint(1, 4)))):
            # Job that accepts flow dataset inputs
            name = fake.word()
            job, output = generate_job(name, potential_inputs=initial_datasets)
            jobs[name] = job
            datasets.add(output)

            # Make sure that all flow dataset inputs are used
            datasets_used |= set(job.inputs)
            unused_datasets = initial_datasets - datasets_used
            if last and unused_datasets:
                job.inputs |= unused_datasets

            # Load this output (don't register it as an eligible input)
            loader, _ = generate_job(
                name='load-' + name,
                potential_inputs=(output,),
                output='scheme.%s@database' % name
            )
            jobs['load-' + name] = loader

        jobs.update(initial_jobs)
            
        slo = random.randint(0, 24)
        frequency = random.randint(slo, 24) if slo else None
        return Flow(
            owner=random.choice(owners),
            monitoring=random.choice(list(Monitoring)),
            frequency='{}h'.format(frequency) if frequency else None,
            slo='{}h'.format(frequency) if slo else None,
            jobs=jobs
        )

    flows = dict()
    for _ in range(0, random.randint(50, 100)):
        flows[fake.word()] = generate_flow(list(flows.keys()))
    return flows


def read_schedule(filepath=None):
    with open(filepath, 'r') as f:
        data = yaml.load(f)

    flows = {}
    for flow_name, flow_data in data.items():
        monitoring = flow_data.pop('monitoring', None)
        monitoring = Monitoring(monitoring) if monitoring else None
        
        flows[flow_name] = Flow(
            owner=flow_data.pop('owner'),
            monitoring=monitoring,
            frequency=flow_data.pop('frequency', None),
            slo=flow_data.pop('slo', None),
            jobs={
                name: Subflow(data['flow']) if 'flow' in data else Job(**data)
                for name, data in flow_data.items()
            } if flow_data else {}
        )
    return flows
