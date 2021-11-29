import streamlit as st
from io import StringIO
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import networkx as nx
from pyvis.network import Network
import game 
import time
from pathlib import Path
import csv

st.title("Game Theoretic Request Routing")

processing_time = st.number_input(label="Processing Time (seconds):", value=0.5, step=0.25)
propagation_speed = st.number_input(label="Propagation Speed (km/s):", value=1, step=1)

st.header("Distance Matrix (Users x Processors)")

method = st.radio(label="How should we get the distance matrix?", options=["Random", "From CSV"])

if method == "Random":
    n_user = int(st.number_input(label="Number of Users:", step=1, value=6))
    n_processor = int(st.number_input(label="Number of Processors:", step=1, value=2))

    min_d = int(st.number_input(label="Min Distance", step=1, value=1))
    max_d = int(st.number_input(label="Max Distance", step=2, value=10))
    distance_matrix = {k: {i: np.random.uniform(min_d, max_d) for i in range(n_user)} for k in range(n_processor)}
elif method == "From CSV":
    st.info("""
    #### CSV format

    Rows represent **processors** and columns represent **users**.

    The **first row** must be the user numbers, starting from 0.

    ##### For 2 users and 3 processors

    ```csv
    0, 1
    X, X
    X, X
    X, X
    ```

    ##### For 8 users and 3 processors

    ```csv
    0, 1, 2, 3, 4, 5, 6, 7
    X, X, X, X, X, X, X, X
    X, X, X, X, X, X, X, X
    X, X, X, X, X, X, X, X
    ```
    """)
    csv_data = st.file_uploader(label="Upload CSV file!")

    if not csv_data:
        st.error("Please provide distance data (csv or random)")
        distance_matrix = None
    else:
        csv_string = StringIO(csv_data.getvalue().decode("utf-8"))
        d_reader = csv.DictReader(csv_string)
        distance_matrix = {int(j) : {int(i): float(d) for i, d in row.items()} for j, row in enumerate(d_reader)}
        n_processor = len(distance_matrix)
        n_user = len(distance_matrix[0])


if distance_matrix:

    st.table(distance_matrix)

    D = nx.DiGraph()

    n = Network("800px", "800px", notebook=True, heading="")
    for k, distances in distance_matrix.items():
        proc = f"proc {k}"
        n.add_node(proc, color="orange")
        for i, d in distances.items():
            user = f"user {i}"
            n.add_node(user, color="blue")
            n.add_edge(user, proc, length=d*20, label=str(int(d)))

    n.from_nx(D)
    n.show('D.html')

    components.html(Path('D.html').read_text(), height=900, width=900)


    game_ = game.Game(
        n_users=n_user,
        n_processors=n_processor, 
        processing_time=processing_time,
        propagation_speed=propagation_speed, 
        distance_matrix=distance_matrix
    )

    time1 = time.time()
    game_.simulate()
    time2 = time.time()


    equilibria = list(game_.nash_equilibria())

    st.header(f"Found {len(equilibria)} Nash Equilibria from {len(game_.outcomes)} profiles in {time2-time1} seconds")

    vis = st.checkbox(label=f"Visualize NE?")

    for profile, times in equilibria:
        ne_table = {
            "User": [u for u in times.keys()],
            "Processor Choice": profile, 
            "Wait Times": [time for time in times.values()],
        }

        df = pd.DataFrame(ne_table)
        styler = df.style.hide_index()
        st.write(styler.to_html(), unsafe_allow_html=True)

        if vis:
            g = nx.Graph()
            for user, proc in enumerate(profile):
                g.add_node(f"proc {proc}", color="orange")
                g.add_edge(f"user {user}", f"proc {proc}", length=times[user] * 10, label=round(times[user], 1))
                


            ne = Network("800px", "800px", notebook=True, heading="")
            ne.from_nx(g)
            ne.show('ne.html')

            components.html(Path('ne.html').read_text(), height=900, width=900)

