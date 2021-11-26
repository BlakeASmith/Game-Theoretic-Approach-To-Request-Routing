import streamlit as st
import pandas as pd
import numpy as np
import game 

st.title("Game Theoretic Request Routing")

n_user = int(st.number_input(label="Number of Users:", step=1, value=6))
n_processor = int(st.number_input(label="Number of Processors:", step=1, value=2))

processing_time = st.number_input(label="Processing Time (seconds):", value=0.5, step=0.25)
propagation_speed = st.number_input(label="Propagation Speed (km/s):", value=1, step=1)

st.header("Distance Matrix (Users x Processors)")

min_d = int(st.number_input(label="Min Distance", step=1, value=1))
max_d = int(st.number_input(label="Max Distance", step=2, value=10))

distance_matrix = {k: {i: np.random.uniform(min_d, max_d) for i in range(n_user)} for k in range(n_processor)}

st.table(distance_matrix)


game_ = game.Game(n_user, n_processor, processing_time, propagation_speed, distance_matrix)
game_.simulate()

for NE in game_.nash_equilibria():
    st.write(NE)
