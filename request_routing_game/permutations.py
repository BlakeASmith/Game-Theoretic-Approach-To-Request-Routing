from itertools import product, chain

def all_profiles(n_users, n_processors):
    users = range(n_users)
    processors = range(n_processors)

    for profile in product(processors, repeat=n_users):
        yield {user: processor for user, processor in zip(users, profile)}



if __name__ == "__main__":
    for profile in all_profiles(4, 3): 
        print(profile)