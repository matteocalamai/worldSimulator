# World Simulator

A small Python simulation of a society where individuals make decisions based on their needs and the resources available to them.

The project is being developed as an experiment in software design, behavioral modeling, and emergent behavior. The aim is to understand the systems being built rather than hide them behind a large framework.

## What it does

The simulation contains a world with:

- people with individual traits and internal needs;
- a shared food supply;
- a simple decision-making system;
- working, resting, and eating;
- events generated during the simulation;
- a history of past world states.

Each simulation step updates people, evaluates their decisions, executes those decisions, and records the resulting state.

The model is intentionally small. It is not yet a complete game, economy, or population simulator.

## Project structure

```text
worldSimulator/
├── simulation.py    # World and simulation loop
├── person.py        # Individual state, decisions, and actions
├── event.py         # Simulation events
├── observer.py      # Historical data access
├── renderer.py      # Matplotlib analysis plots
├── dashboard.py     # Streamlit interface
├── requirements.txt # Python dependencies
└── README.md
```

The main architectural boundary is between the simulation and its presentation:

```text
Person / Event
      ↑
    World
      │
      ├── history
      │
      ↓
   Observer
      │
      ├── Renderer
      └── Streamlit dashboard
```

The simulation does not depend on the dashboard or renderer. This keeps the model independent from how its state is displayed.

## The simulation

### World

`World` keeps track of:

- simulation time;
- the population;
- shared food;
- generated events;
- recorded historical states.

A simulation step follows this sequence:

```text
World.step()
    │
    ├── update people
    ├── make decisions
    ├── execute actions
    └── record the new state
```

The default world starts with five people with different characteristics.

### People

Each `Person` currently has:

- age;
- health;
- energy;
- hunger;
- work efficiency;
- hunger threshold;
- hunger resilience.

Needs are kept within a `0..100` range.

Age advances with simulated time. Energy decreases over time, and prolonged hunger damages health.

### Decisions

A person evaluates three actions:

- `eat`
- `work`
- `rest`

The decision scores depend on the person's current state and the food available in the world.

The model is deterministic at this stage. Similar people under the same conditions can therefore make the same decisions. This is useful while studying the effects of the rules.

### Work, rest, and food

Working produces food. Production depends on time worked, work efficiency, hunger, and available energy. Working also consumes energy and increases hunger.

Resting restores energy while increasing hunger slightly.

Eating consumes food from the shared supply and reduces the person's hunger.

## Observing the simulation

After each step, the world records a snapshot of its state. `Observer` provides access to this history without putting analysis logic inside `World`.

It currently supports:

- world food history;
- a person's historical state;
- historical health, energy, and hunger;
- a person's action history;
- population action history.

## Dashboard

The project includes a Streamlit dashboard.

Start it with:

```bash
streamlit run dashboard.py
```

The current interface has four sections.

### Overview

Shows the current simulation day, population, and food supply.

### People

A person can be selected to inspect current health, energy, hunger, age, and work efficiency. Historical health, energy, and hunger can also be viewed.

### Actions

Shows how many people are currently working, resting, or eating, together with recent simulation events.

### Statistics

The section is currently a placeholder for population-level statistics.

The dashboard stores the current `World` in Streamlit session state, so navigating between sections does not recreate the simulation. The simulation can currently be advanced one day at a time from the sidebar.

## Running from Python

The simulation can also be run without the dashboard:

```bash
python simulation.py
```

The module provides:

```python
world = createWorld()
runSimulation(world, 60)
```

The command-line entry point runs a short simulation and prints the resulting people, events, and world status.

## Development setup

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

The `.venv` directory should not be committed to Git.

## Why this project exists

This is a learning project, but it is built as one evolving system rather than a collection of unrelated exercises.

The focus is on:

- object-oriented design;
- separation of responsibilities;
- simulation state;
- time-step based systems;
- resource constraints;
- decision systems;
- historical data;
- visualization;
- emergent behavior.

Development is intentionally incremental. A mechanic is added, its behavior is observed, and only then is the model changed.

Unexpected behavior is part of the project. If people synchronize, food runs out, or the system reaches an unstable state, the first question is which rules produced it rather than how to hide the behavior with arbitrary randomness.

## Current limitations

The model does not yet include:

- births or deaths;
- families or relationships;
- multiple resources;
- jobs or a developed economy;
- inventories or ownership;
- migration;
- persistence of world state;
- a configurable population;
- a completed statistics section.

These are possible future directions, not commitments for the next version.

## Roadmap

Possible future work includes:

1. improving the decision-making system;
2. making individual behavior more expressive;
3. separating update, decision, and action phases more clearly;
4. adding meaningful population-level statistics;
5. introducing additional resources and economic interactions;
6. adding population dynamics;
7. saving and loading simulation state;
8. studying more complex emergent behavior.

The order is deliberately flexible. New features should earn their place by helping answer a useful question about the model.

## Philosophy

The project is built one system at a time.

The goal is not to produce the largest simulation possible. It is to keep the model small enough to understand while making it rich enough for interactions between simple rules to produce behavior worth investigating.
