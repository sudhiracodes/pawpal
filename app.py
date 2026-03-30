import streamlit as st
from datetime import datetime, date
from pawpal_system import Owner, Pet, Task, Scheduler

# --- 1. Session State Initialization ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner("PawPal User")

owner = st.session_state.owner
scheduler = Scheduler(owner)

# --- 2. App Header ---
st.title("🐾 PawPal+ Smart Scheduler")
st.write("Plan your pet care tasks with priority and time constraints.")

# --- 3. Sidebar: Add Pets ---
with st.sidebar:
    st.header("1. Add a Pet")
    with st.form("add_pet_form"):
        pet_name = st.text_input("Pet Name")
        pet_species = st.text_input("Species (Dog, Cat, etc.)")
        submit_pet = st.form_submit_button("Add Pet")
        
        if submit_pet and pet_name:
            new_pet = Pet(pet_name, pet_species)
            owner.add_pet(new_pet)
            st.success(f"{pet_name} added!")

# --- 4. Main Body: Add Tasks ---
st.header("2. Schedule a Task")
if not owner.pets():
    st.info("👈 Please add a pet in the sidebar first!")
else:
    pet_names = [pet.name() for pet in owner.pets()]
    with st.form("add_task_form"):
        selected_pet_name = st.selectbox("Select Pet", pet_names)
        task_desc = st.text_input("Task Description")
        
        col1, col2 = st.columns(2)
        with col1:
            task_time = st.time_input("Start Time")
            task_freq = st.selectbox("Frequency", ["Once", "Daily", "Weekly"])
        with col2:
            task_duration = st.number_input("Duration (minutes)", min_value=1, value=15)
            task_priority = st.slider("Priority (1-5, 5 is highest)", 1, 5, 3)
            
        submit_task = st.form_submit_button("Add Task")
        
        if submit_task and task_desc:
            # Convert Streamlit time to a full datetime object for today
            full_datetime = datetime.combine(date.today(), task_time)
            
            # Find the correct pet and add the task
            selected_pet = next(p for p in owner.pets() if p.name() == selected_pet_name)
            new_task = Task(task_desc, full_datetime, task_freq, task_duration, task_priority)
            selected_pet.add_task(new_task)
            st.success("Task scheduled!")

# --- 5. Display Schedule with Time Budget ---
st.header("3. Today's Plan")

budget_toggle = st.checkbox("Enable Time Budget?")
budget_mins = None
if budget_toggle:
    budget_mins = st.number_input("How many minutes do you have today?", min_value=10, value=60)

# Optional filter by pet
pet_filter_options = ["All Pets"] + [pet.name() for pet in owner.pets()]
selected_filter = st.selectbox("Filter by pet", pet_filter_options)

# Run Algorithms
today = date.today()

if selected_filter == "All Pets":
    base_tasks = owner.get_all_tasks()
else:
    selected_pet = next(p for p in owner.pets() if p.name() == selected_filter)
    base_tasks = selected_pet.get_tasks()

scheduled_tasks = scheduler.get_today_schedule(today, budget_mins, tasks=base_tasks)
conflicts = scheduler.check_conflicts(scheduled_tasks)

for warning_task in conflicts:
    st.warning(f"Time conflict detected at {warning_task.time().strftime('%H:%M')}!", icon="⚠️")

if not scheduled_tasks:
    st.write("No tasks scheduled for today.")
else:
    for task in scheduled_tasks:
        # Find which pet owns the task for UI display
        pet_name_display = "Unknown"
        for pet in owner.pets():
            if task in pet.get_tasks():
                pet_name_display = pet.name()
                break

        col1, col2, col3 = st.columns([1, 3, 1])
        with col1:
            st.write(f"**{task.time().strftime('%H:%M')}**")
        with col2:
            st.write(f"🐶 **{pet_name_display}**: {task.description()} ({task.duration_minutes()}m) | Priority: {'⭐'*task.priority()}")
        with col3:
            status = "✅ Done" if task.is_complete() else "⏳ Pending"
            st.write(status)