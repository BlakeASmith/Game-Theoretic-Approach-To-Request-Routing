from request_routing_game import waiting


def test_waiting_time():
    wait_times = waiting.waiting_time(
        requests = [1, 2, 3, 4],
        processing_time = 1,
        distances = {1: 1, 2: 2, 3: 3, 4:4},
        propagation_speed = 2,
    )

    assert wait_times == {
        1: 0.0, 2: 0.5, 3: 1.0, 4: 1.5  
    }
