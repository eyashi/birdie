# generate some toy data

import datetime
import random
from tqdm import tqdm

open("toy-data.txt", "a").close()

initial_time = datetime.datetime.now() - datetime.timedelta(days=7)
minute_range = 7 * 24 * 60

for _ in tqdm(range(5000)):
    num_minutes = random.randint(0, minute_range)
    log_time = initial_time + datetime.timedelta(minutes=num_minutes)

    time_stamp = log_time.strftime("%Y-%m-%d %H-%M-%S")
    with open("toy-data.txt", "a") as l:
        l.write("BIRD! @{}\n".format(time_stamp))

