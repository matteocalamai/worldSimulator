import streamlit as st

from simulation import createWorld, runSimulation
from observer import Observer

if "world" not in st.session_state:
    st.session_state.world = createWorld()

world = st.session_state.world
observer = Observer(world)

st.set_page_config(
    page_title="World Simulator",
    page_icon="🌍",
    layout="wide"
)


st.title("🌍 World Simulator")
st.caption("Simulation dashboard")


st.sidebar.title("Navigation")

st.sidebar.subheader("Simulation")

if st.sidebar.button("▶ Run 1 day"):
    world.step(1)

page = st.sidebar.radio(
    "Go to",
    [
        "Overview",
        "People",
        "Actions",
        "Statistics"
    ]
)


if page == "Overview":
    st.header("Overview")
    st.metric(
    "Day",
    int(world.time)
)

    st.metric(
        "Population",
        len(world.people)
    )

    st.metric(
        "Food",
        f"{world.food:.1f}"
    )

elif page == "People":
    st.header("People")

    person_ids = [person.id for person in world.people]

    selected_id = st.selectbox(
        "Select a person",
        person_ids
    )

    selected_person = next(
        person
        for person in world.people
        if person.id == selected_id
    )

    st.subheader(f"Person #{selected_person.id}")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Health", f"{selected_person.health:.1f}")

    with col2:
        st.metric("Energy", f"{selected_person.energy:.1f}")

    with col3:
        st.metric("Hunger", f"{selected_person.hunger:.1f}")

    st.write(f"Age: {selected_person.age:.1f}")
    st.write(
        f"Work efficiency: "
        f"{selected_person.workEfficiency:.2f}"
    )

    st.divider()

    metric = st.selectbox(
        "History",
        [
            "energy",
            "hunger",
            "health"
        ]
    )

    history = observer.getPersonMetricHistory(
        selected_id,
        metric
    )

    st.line_chart(history)

elif page == "Actions":
    st.header("Actions")

    if not world.history:
        st.info("No simulation data yet.")
    else:
        current_state = world.history[-1]

        action_counts = {
            "work": 0,
            "rest": 0,
            "eat": 0
        }

        for person in current_state["people"]:
            action = person.get("action")

            if action in action_counts:
                action_counts[action] += 1

        st.subheader(f"Day {int(world.time)}")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Working",
                action_counts["work"]
            )

        with col2:
            st.metric(
                "Resting",
                action_counts["rest"]
            )

        with col3:
            st.metric(
                "Eating",
                action_counts["eat"]
            )

        st.divider()

        st.subheader("Recent events")

        recent_events = world.events[-10:]

        if recent_events:
            for event in reversed(recent_events):
                st.write(
                    f"**Day {event.time:.0f}** — "
                    f"{event.message}"
                )
        else:
            st.write("No events yet.")

elif page == "Statistics":
    st.header("Statistics")
    st.write("Simulation statistics")

