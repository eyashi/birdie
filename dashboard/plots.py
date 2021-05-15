import matplotlib.pyplot as plt
import os, datetime

TOY_DATA = "toy-data.txt"


def parse_datetime(line):
    time_str = line.split("@")[-1]
    return datetime.datetime.strptime(time_str, "%Y-%m-%d %H-%M-%S")


def get_data(log_file):
    d_out = []
    with open(log_file, "r") as lf:
        lines = lf.read().split("\n")
        for line in lines:
            if line != "":
                d = parse_datetime(line)
                d_out.append(d)
    return d_out


def plot_freq_by_hour(date_start, date_end, data):
    counter = [0] * 24
    for date in data:
        if date > date_start and date < date_end:
            counter[date.hour] += 1

    plt.bar(list(range(24)), counter)
    plt.show()


if __name__ == "__main__":
    d = get_data(TOY_DATA)
    date_start = datetime.datetime.now() - datetime.timedelta(days=7)
    date_end = datetime.datetime.now() - datetime.timedelta(days=4)
    plot_freq_by_hour(date_start, date_end, d)
