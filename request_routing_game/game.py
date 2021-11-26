import permutations, waiting
from typing import Tuple, Dict
from dataclasses import dataclass

@dataclass
class Game:
    n_users: int
    n_processors: int
    processing_time: float
    propagation_speed: int
    distance_matrix: Dict[int, Dict[int, float]]

    def simulate(self):
        self.outcomes = {}

        for profile in permutations.all_profiles(self.n_users, self.n_processors):
            wait_times = waiting.waiting_times_for_profile(
                profile=profile,
                propagation_speed=self.propagation_speed,
                processing_time=self.processing_time,
                distance_matrix=self.distance_matrix,
            )

            self.outcomes[tuple(profile.values())] = wait_times

        return self.outcomes

    def nash_equilibria(self) -> Tuple[int]:
        for profile, wait_times in self.outcomes.items():
            # For each profile, check if it is a nash equilibrium
            if self.check_nash_equilibrium(profile) is True:
                yield profile, wait_times


    def check_nash_equilibrium(self, profile):
        for user in range(self.n_users):
            # Go through potential payoffs for each user
            for processor in range(self.n_processors):
                # Change the current processor selection to this processor
                alt_profile = profile[:user] + (processor,) + profile[user+1:]
                # Compare the current wait time to the alternate
                if self.outcomes[profile][user] > self.outcomes[alt_profile][user]:
                    # There is a better move for this user
                    # --> not a nash equilibrium
                    return False
        return True

