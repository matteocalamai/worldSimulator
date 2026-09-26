# Mini World Simulation

A small Python simulation of a society made up of individuals who make decisions based on their needs and the resources available to them.

The project is primarily a programming and modeling exercise. The goal is not to build a complete game immediately, but to gradually build a small simulated world and observe how simple rules can produce behavior over time.

## Project Goal

The simulation is initially being developed without graphics.

The **simulation engine** should remain independent from visualization, so that a renderer can be added later without having to rewrite the core world logic.

The project is being developed incrementally as a way to better understand:

- object-oriented programming in Python;
- state and behavior;
- time-step based simulation;
- resource management;
- decision-making systems;
- interactions between individuals and their environment;
- emergent behavior.

## Current State

The simulation currently contains three main concepts:

- `World` — represents the world and manages time, people, food, and events.
- `Person` — represents an individual with age, health, energy, hunger, and personal traits.
- `Event` — records what happens during the simulation.

## Current Mechanics

### Time

The world advances through `World.step(deltaTime)`.

Each time step updates the individuals and allows them to make a decision.

Age is represented in years and increases proportionally to simulated time:

```text
1 day = 1 / 365 of a year
```

### Needs

Each person currently has three main needs:

- `health` — health, initially 100;
- `energy` — energy, initially 100;
- `hunger` — hunger, initially 0.

As time passes:

- energy decreases;
- hunger increases;
- when hunger exceeds 80, health starts to decrease.

Values are kept within the `0..100` range.

### Food

The world has a global food supply.

A person can consume food when they decide to eat. Consumed food is removed from the world's supply and reduces the person's hunger.

If less food is available than requested, the person can consume only the amount that remains.

### Decisions

Each person can choose between three actions:

- `eat`
- `work`
- `rest`

The decision mainly depends on:

1. hunger level;
2. food availability;
3. energy level.

In particular, a hungry person tries to eat when food is available. If they cannot eat and have low energy, they rest; otherwise, they work.

### Work

Working produces food for the world.

The amount produced depends on:

- time worked;
- the person's `workEfficiency`;
- the person's hunger level.

Each person therefore has a different productivity.

When hunger reaches at least 80, production is reduced by half. This allows the simulation to keep producing food during periods of scarcity instead of reaching a complete deadlock.

Working consumes energy.

### Rest

Rest recovers energy.

A person can recover energy up to a maximum of 100.

### Individual Differences

Individuals are not identical.

Each person currently has:

- `workEfficiency` — efficiency when producing food;
- `hungerThreshold` — hunger level at which the person tends to choose eating.

These characteristics provide a first step toward creating behavioral differences between individuals.

### Unique IDs

Each person automatically receives a sequential ID.

Example:

```text
Person #1
Person #2
Person #3
```

IDs are also used in simulation events.

### Events

The world keeps a list of events.

Events currently record things such as:

- decisions;
- food consumed;
- food produced;
- resting.

Example:

```text
[Day 404.0] Person #1 chose to work
[Day 404.0] Person #1 worked and produced 0.8 food
[Day 404.0] Person #2 chose to eat
[Day 404.0] Person #2 ate 0.8 food
```

The event system will also be useful later for connecting the simulation engine to a possible visualization layer.

## Conceptual Structure

```text
World
 ├── time
 ├── food
 ├── people
 │    ├── Person
 │    ├── Person
 │    └── ...
 └── events
      ├── Event
      ├── Event
      └── ...
```

The current flow of one simulation day is roughly:

```text
World.step()
    ↓
update person
    ↓
person makes a decision
    ↓
execute action
    ↓
world updates resources
    ↓
create Event
```

## Running the Simulation

Python is required.

Run:

```bash
python simulation.py
```

The program runs the simulation and then displays:

- the final state of the people;
- recorded events;
- remaining food;
- the overall world status.

To change the simulation length, modify:

```python
for day in range(500):
    world.step(1)
```

For example, `range(1000)` simulates 1000 time steps.

## Initial Population

The simulation currently starts with five people with different characteristics:

| Person | Age | Efficiency | Hunger Threshold |
|---|---:|---:|---:|
| #1 | 20 | 0.8 | 40 |
| #2 | 25 | 1.0 | 50 |
| #3 | 31 | 1.2 | 65 |
| #4 | 40 | 1.0 | 50 |
| #5 | 55 | 0.7 | 70 |

These values are intentionally simple. They are used to create slightly different individuals and observe how those differences affect the simulation.

## Roadmap

The project is still in its early stages. Possible future developments include:

### Next Steps

- improve the decision-making system;
- introduce more behavioral variation;
- better separate updating, decision, and action phases;
- make the needs system more meaningful.

### Economy

- multiple resource types;
- resource gathering and consumption;
- different jobs;
- production and distribution;
- trading between people;
- ownership and inventories.

### Population

- birth;
- death;
- migration;
- families and relationships;
- generations.

### Emergent Behavior

The goal is to eventually reach situations where the overall behavior of the society is not directly scripted, but emerges from interactions between:

```text
individuals
    +
needs
    +
resources
    +
environment
    +
decisions
```

### Saving and Loading

Future versions may include:

- saving the state of the world;
- loading a previous simulation;
- replaying past events.

### Renderer

Only after the simulation engine becomes more solid, a graphical representation can be added.

The idea is to keep the following layers separate:

```text
Simulation Core
      ↓
   World State
      ↓
    Renderer
```

This way, the renderer does not need to know the internal rules of the simulation.

## Project Philosophy

The project is being built **one system at a time**.

The goal is not to immediately write hundreds of lines of code, but to add one mechanic, observe its behavior, find problems, and understand why the system reacts in a particular way.

The simulation is therefore both a programming exercise and a laboratory for learning how to design software and model complex systems.
