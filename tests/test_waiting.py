from request_routing_game import waiting, game


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


def test_waiting_times_for_profile():
    wait_times = waiting.waiting_times_for_profile(
        profile = {
            1: 1, 
            2: 1, 
            3: 1,
            4: 2,
        },
        processing_time = 1,
        distance_matrix = {1: {1: 1, 2: 2, 3: 3, 4:4}, 2: {1: 2, 2: 6, 3: 7, 4: 9}},
        propagation_speed = 2,
    )

    assert dict(wait_times) == {1: 0.0, 2:0.5, 3:1.0, 4:0.0}


def test_game():
    g = game.Game(
        n_users=3,
        n_processors=2,
        processing_time=6,
        propagation_speed=1,
        distance_matrix={
            0: {0: 3, 1: 4, 2: 5},
            1: {0: 7, 1: 1, 2: 2}
        }
    )

    outcomes = g.simulate()

    for outcome in outcomes.items():
        print(outcome)

    print("NASH EQUILIBRIA FOUND")
    for equilibria in g.nash_equilibria():
        print(equilibria)

    raise ValueError()