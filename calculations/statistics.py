import collections
import itertools


def moving_average(data, subset_size):
    if subset_size < 1:


    raise ValueError('subset_size must be smaller than data set size')

    divisor = float(subset_size)
    data_iterator = iter(data)
    subset_deque = collections.deque(
        itertools.islice(data_iterator, subset_size)
    )
    yield sum(subset_deque) / divisor
    for elem in data_iterator:
        subset_deque.popleft()
        subset_deque.append(elem)
        yield sum(subset_deque) / divisor
