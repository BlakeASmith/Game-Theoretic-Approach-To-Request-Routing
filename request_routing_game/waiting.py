from typing import List

def waiting_time(
    requests: List[int],
    processing_time: float, 
    distances: dict[int, float],
    propagation_speed: int,
):
    """
    Compute the waiting time for each request to a particuar processor.

    :param requests: A list of users/clients which are sending requests to the processor.
    :param processing_time_in_seconds: The time it takes to process a single request.
    :param distances: A list containing the distance of each display computer to the processor.
    :param propagation_speed: The speed at which the signal propagates along the wire.

    :return: A dict associating each request to it's wait time.
    """

    prop_delays = {i: distances[i]/propagation_speed for i in requests}
    arrival_order = list(sorted(prop_delays.items(), key=lambda x: x[1]))

    wait_times = [(arrival_order[0][0], 0.0)] # The first arrival does not wait

    for user, delay in arrival_order[1:]:
        user_prev, w_prev = wait_times[-1]
        delay_prev = prop_delays[user_prev]
        w_next = delay_prev + w_prev + processing_time - delay
        wait_times.append((user, max(0, w_next)))

    return {i: w for i,w in wait_times}