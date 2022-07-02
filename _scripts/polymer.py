import random
import os
import random
import json
import time
from datetime import datetime as dt

import streamlit as st


st.title("🧬 Polymer")

if "REVIEWING" not in st.session_state:
    st.session_state.REVIEWING = False

if "atom_idx" not in st.session_state:
    st.session_state.atom_idx = 0


def get_raw_atoms():
    res = []

    # list files in directory
    for f in os.listdir("."):
        if f.endswith(".md") and "__" not in f:
            if not "#todo" in open(f, "r").read():
                res.append(f)

    for f in os.listdir("./Molecules"):
        if f.endswith(".md") and "__" not in f:
            if not "#todo" in open(f"./Molecules/{f}", "r").read():
                res.append(f)
    return res


def create_db():
    filename = "_scripts/db.json"
    atoms = get_raw_atoms()
    random.shuffle(atoms)
    # if db doesn't exist, create it
    if not os.path.exists(filename):
        db = {}
        for i, atom in enumerate(atoms):
            db[atom] = {
                "recall": 0,
                "queue": i,
                "last_tag": "",
                "last_recall": dt.now().timestamp(),
            }
    # else, update it
    else:
        with open(filename, "r") as f:
            db = json.load(f)
        for atom in atoms:
            if atom not in db:
                db[atom] = {"recall": 0}
    return db


def compute_queue(db):
    sorted_items = sorted(db.items(), key=lambda x: x[1]["queue"])
    db = {k: v for k, v in sorted_items}

    for i, (k, _) in enumerate(db.items()):
        db[k]["queue"] = i
    return db


def write_db(db):
    filename = "_scripts/db.json"
    db = compute_queue(db)
    with open(filename, "w") as f:
        json.dump(db, f, indent=4)


def list_atoms(db):
    atoms = list(db.keys())
    return atoms


db = create_db()


def read_atom(atom_name):
    try:
        with open(atom_name, "r") as f:
            contents = f.read()
        path = ""
    except FileNotFoundError:
        with open(f"Molecules/{atom_name}", "r") as f:
            contents = f.read()
        path = "Molecules%2F"
    # contents = contents.split("---")[0]
    contents = contents.replace("[[", "***").replace("]]", "***")
    # link = f'obsidian://open?vault=ObsidianVault&file={path}{atom_name.replace(" ", "%20")}'
    # contents += f"\n{link}"
    return contents


def update_atom(tag, q_increment):
    db[st.session_state["current_atom"]]["last_tag"] = tag
    db[st.session_state["current_atom"]]["recall"] += 1
    db[st.session_state["current_atom"]]["last_recall"] = dt.now().timestamp()
    db[st.session_state["current_atom"]]["queue"] += q_increment
    st.session_state["current_atom"] = atoms[
        atoms.index(st.session_state["current_atom"]) + 1
    ]


atoms = list_atoms(db)

cols = st.columns(10)


with cols[0]:
    show = st.button("show")
with cols[1]:
    fail = st.button("fail")
with cols[2]:
    hard = st.button("hard")
with cols[3]:
    easy = st.button("easy")
with cols[4]:
    instant = st.button("instant")

# Handle button selection
if fail:
    update_atom("fail", 10)
elif hard:
    update_atom("hard", 15)
elif easy:
    update_atom("easy", 20)
elif instant:
    update_atom("instant", 30)


option = st.selectbox(
    "Note:", atoms, key="current_atom", format_func=lambda x: x.split(".md")[0]
)
st.markdown("---")

if show:
    st.markdown(read_atom(option))

write_db(db)
