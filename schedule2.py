import random

import faker
import lib

if __name__ == '__main__':
    random.seed(2)
    fake = faker.Faker('en_CA')
    fake.seed(2)

    flows = lib.generate_schedule()

    for flow in flows.keys():
        print(flow)
