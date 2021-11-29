"""Visualization functions"""
import matplotlib.pyplot as plt
import pandas as pd
from collections import defaultdict

def timeline(profile, waiting_times, game):
    tasks = defaultdict(lambda: [])
    finishes = defaultdict(lambda: [])

    for p, (u, w) in zip(profile, waiting_times.items()):
        d = game.distance_matrix[p][u] / game.propagation_speed
        tasks[p].append(f"User {u}")
        finishes[p].append(d + w + game.processing_time + d)

    fig, axis = plt.subplots(1, len(tasks))

    for p, ax in zip(tasks, axis):
        ax.stem(tasks[p], finishes[p])
        ax.set_title(f"Processor {p}")

    return fig