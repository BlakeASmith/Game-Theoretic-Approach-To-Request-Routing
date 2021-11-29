from typing import List
from itertools import groupby
from typing import Dict
from collections import ChainMap, defaultdict

def waiting_time(
    requests: List[int],
    processing_time: float, 
    distances: Dict[int, float],
    propagation_speed: int,
):
    """
    Compute the waiting time for each request to a particuar processor.

    :param requests: A list of users/clients which are sending requests to the processor.
    :param processing_time_in_seconds: The time it takes to process a single request.
    :param distances: A list containing the distance of each display computer to the processor.
    :param propagation_speed: The speed at which the signal propagates along the wire.

    :return: A Dict associating each request to it's wait time.
    """

    prop_delays = {i: distances[i]/propagation_speed for i in requests}
    arrival_order = list(sorted(prop_delays.items(), key=lambda x: x[1]))

    wait_times = [(arrival_order[0][0], 0.0)] # The first arrival does not wait

    for user, delay in arrival_order[1:]:
        user_prev, w_prev = wait_times[-1]
        delay_prev = prop_delays[user_prev]
        w_next = delay_prev + w_prev + processing_time - delay
        wait_times.append((user, max(0.0, w_next)))

    return {i: w for i,w in wait_times}


def waiting_times_for_profile(
    profile: Dict[int, int],
    processing_time: float, 
    distance_matrix: Dict[int, Dict[int, float]],
    propagation_speed: int,
) -> Dict[int, float]:
    """
    Compute waiting times for all users given a profile of the game.

    :param processing_time_in_seconds: The time it takes to process a single request.
    :param distance_matrix: The distance matrix, giving distances between each user and processor.
    :param propagation_speed: The speed at which the signal propagates along the wire.

    :return: A Mapping[int, float] associating users to the waiting time during this game.
    """
    groups = defaultdict(lambda: [])

    for u, p in profile.items():
        groups[p].append(u)

    mappings = []


    for processor, requests in groups. items():

        waiting_times = waiting_time(
            requests,
            processing_time,
            distance_matrix[processor],
            propagation_speed
        )

        mappings.append(waiting_times)

    return dict(ChainMap(*mappings))



        
