import datetime
import streamlit as st
from pawpal_system import Owner, Pet, Task, Priority, Frequency, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

# --- session_state initialization ---
# owners: dict keyed by name so we can switch between them without losing data.
# selected_owner / selected_pet: track which owner and pet are active.
# Pets and Tasks are reachable through owner.pets / pet.tasks — no need to
# store them separately in session_state.
if "owners" not in st.session_state:
    st.session_state.owners = {}

if "selected_owner" not in st.session_state:
    st.session_state.selected_owner = None

if "selected_pet" not in st.session_state:
    st.session_state.selected_pet = None


def _add_owner(name):
    if name not in st.session_state.owners:
        st.session_state.owners[name] = Owner(name=name)
    st.session_state.selected_owner = name
    st.session_state.selected_pet = None

def _remove_owner():
    key = st.session_state.selected_owner
    if key and key in st.session_state.owners:
        del st.session_state.owners[key]
    st.session_state.selected_owner = None
    st.session_state.selected_pet = None

def _add_pet(name, spec):
    owner = st.session_state.owners.get(st.session_state.selected_owner)
    if owner and not owner.find_pet(name):
        owner.add_pet(Pet(name=name, species=spec))
    st.session_state.selected_pet = name

def _remove_pet():
    owner = st.session_state.owners.get(st.session_state.selected_owner)
    if owner:
        pet = owner.find_pet(st.session_state.selected_pet)
        if pet:
            owner.remove_pet(pet)
    st.session_state.selected_pet = None


# --- Owner ---
st.subheader("Owner")

owner_keys = list(st.session_state.owners.keys())
if owner_keys:
    if st.session_state.selected_owner not in owner_keys:
        st.session_state.selected_owner = owner_keys[0]
    st.selectbox("Select an owner", owner_keys, key="selected_owner")
else:
    st.selectbox("Select an owner", ["(no owners yet)"], disabled=True)

st.subheader("Manage Owners")

owner_name = st.text_input("Owner name", value="Jordan")
st.button("Add owner", on_click=_add_owner, args=(owner_name,))
if st.session_state.selected_owner:
    st.button("Remove current owner", on_click=_remove_owner)

# Resolve the active owner object from the dict
current_owner = st.session_state.owners.get(st.session_state.selected_owner)

st.divider()

# --- Pet ---
st.subheader("Pet")

pet_names = [p.name for p in current_owner.pets] if current_owner else []
if pet_names:
    if st.session_state.selected_pet not in pet_names:
        st.session_state.selected_pet = pet_names[0]
    st.selectbox("Select a pet", pet_names, key="selected_pet")
else:
    st.selectbox("Select a pet", ["(no pets yet)"], disabled=True)

st.subheader("Manage Pets")

pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", [
    "🐕 Dog", "🐈 Cat", "🐇 Rabbit", "🐹 Hamster", "🐠 Fish",
    "🐦 Bird", "🦜 Parrot", "🦎 Lizard", "🐢 Turtle", "🐍 Snake",
    "🐀 Rat", "🐾 Guinea Pig", "🦔 Hedgehog", "🐓 Chicken", "⚡ Pikachu", "🐾 Other",
])
st.button("Add pet", on_click=_add_pet, args=(pet_name, species), disabled=not current_owner)
if current_owner and st.session_state.selected_pet:
    st.button("Remove current pet", on_click=_remove_pet)

# Resolve the active pet object
current_pet = current_owner.find_pet(st.session_state.selected_pet) if current_owner else None

st.divider()

# --- Tasks ---
st.markdown("### Tasks")
st.caption("Add tasks for the active pet. These will feed into the scheduler.")

PRIORITY_MAP = {
    "Very low": Priority.VERY_LOW,
    "Low": Priority.LOW,
    "Medium": Priority.MEDIUM,
    "High": Priority.HIGH,
    "Very high": Priority.VERY_HIGH,
}

FREQUENCY_MAP = {
    "Daily":    Frequency.DAILY,
    "Weekly":   Frequency.WEEKLY,
    "One-time": Frequency.ONE_TIME,
}

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    start_time = st.time_input("Start time", value=datetime.time(9, 0))
with col3:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col4:
    priority_str = st.selectbox("Priority", list(PRIORITY_MAP.keys()), index=3)
with col5:
    frequency_str = st.selectbox("Frequency", list(FREQUENCY_MAP.keys()))

today = datetime.date.today()
if frequency_str == "Daily":
    task_date = today + datetime.timedelta(days=1)
elif frequency_str == "Weekly":
    DAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_str = st.selectbox("Day of week", DAY_NAMES)
    target_weekday = DAY_NAMES.index(day_str)
    days_ahead = (target_weekday - today.weekday()) % 7 or 7
    task_date = today + datetime.timedelta(days=days_ahead)
else:
    task_date = st.date_input("Date", value=today)

if st.button("Add task"):
    if current_pet:
        current_pet.add_task(
            title=task_title,
            date=task_date,
            time=start_time,
            duration=int(duration),
            priority=PRIORITY_MAP[priority_str],
            frequency=FREQUENCY_MAP[frequency_str],
        )
    else:
        st.warning("Add an owner and a pet before adding tasks.")

if current_pet and current_pet.tasks:
    st.write(f"Tasks for {current_pet.name}:")
    st.table([
        {
            "Title": t.title,
            "Date": str(t.date) if t.date else "—",
            "Start time": str(t.time) if t.time else "—",
            "Duration (min)": t.duration,
            "Priority": t.priority.name,
            "Frequency": t.frequency.value,
        }
        for t in current_pet.tasks
    ])
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    st.warning(
        "Not implemented yet. Next step: create your scheduling logic (classes/functions) and call it here."
    )
    st.markdown(
        """
Suggested approach:
1. Design your UML (draft).
2. Create class stubs (no logic).
3. Implement scheduling behavior.
4. Connect your scheduler here and display results.
"""
    )
