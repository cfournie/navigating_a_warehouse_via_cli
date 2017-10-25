import enum
import yaml
import faker
import random

class Monitoring(enum.Enum):
    OFF = 'off'
    PASSIVE = 'passive'
    ACTIVE = 'active'


class Job(object):

    def __init__(self, resource_class, executable, command_options, dependencies=None):
        self.resource_class = resource_class
        self.executable = executable
        self.command_options = command_options
        self.dependencies = dependencies


class Subflow(object):

    def __init__(self, name):
        self.name = name

        
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
    
    def generate_job(potential_dependencies):
        return Job(
            resource_class=random.choice(['small', 'medium', 'large']),
            executable=fake.file_name(extension='py'),
            command_options={fake.word(): fake.word() for _ in range(0, random.randint(1, 4))},
            dependencies=random.choices(potential_dependencies) if potential_dependencies else None
        )
    
    def generate_flow(potential_subflows):
        jobs = dict()
        for _ in range(0, random.randint(1, 5)):
            jobs[fake.word()] = Subflow(random.choice(potential_subflows)) if potential_subflows and random.choice([True, False]) else \
                                generate_job(list(jobs.keys()))
                                
        slo = random.randint(0, 24)
        frequency = random.randint(slo, 24) if slo else None
        return Flow(
            owner=fake.safe_email(),
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
