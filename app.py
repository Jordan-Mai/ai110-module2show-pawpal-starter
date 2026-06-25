import streamlit as st
from pawpal_system import Owner, Pet, Scheduler, Task

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

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "schedule" not in st.session_state:
    st.session_state.schedule = None

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    # Ensure Owner exists
    name = owner_name.strip() or "Owner"
    existing_owner = st.session_state.get("owner")
    if (not isinstance(existing_owner, Owner)) or (existing_owner.name != name):
        st.session_state.owner = Owner(name=name)
    owner = st.session_state.owner

    # Ensure Pet exists and is attached to the owner
    pet_name_val = pet_name.strip() or "Pet"
    existing_pet = st.session_state.get("pet")
    if (
        (not isinstance(existing_pet, Pet))
        or (existing_pet.name != pet_name_val)
        or (existing_pet.species != species)
        or (existing_pet.owner is not owner)
    ):
        st.session_state.pet = Pet(name=pet_name_val, species=species, owner=owner)
    pet = st.session_state.pet

    # Create a Task instance and attach it to the Pet using the Phase 2 API
    try:
        task_obj = Task(title=task_title, duration_minutes=int(duration), priority=priority)
        pet.add_task(task_obj)
    except ValueError as validation_error:
        st.error(str(validation_error))

current_pet = st.session_state.get("pet")
if current_pet and current_pet.tasks:
    scheduler = Scheduler()
    sorted_tasks = scheduler.sort_by_time(current_pet.tasks)
    
    st.subheader("Current Tasks")
    task_data = []
    for index, task in enumerate(sorted_tasks):
        original_idx = current_pet.tasks.index(task)
        task_data.append({
            "Title": task.title,
            "Duration (min)": task.duration_minutes,
            "Priority": task.priority.upper(),
            "Time": task.time or "—",
            "Recurrence": task.recurrence or "—",
        })
    
    st.dataframe(
        task_data,
        use_container_width=True,
        hide_index=True,
    )
    
    col_a, col_b = st.columns([4, 1])
    with col_b:
        if st.button("Clear all tasks"):
            current_pet.tasks.clear()
            st.experimental_rerun()
elif st.session_state.tasks:
    # Fallback to legacy storage (list of dicts)
    st.info("📋 **Legacy tasks (dict format)**")
    task_data = []
    for index, task in enumerate(st.session_state.tasks):
        task_data.append({
            "Title": task["title"],
            "Duration (min)": task["duration_minutes"],
            "Priority": task["priority"].upper(),
        })
    st.dataframe(task_data, use_container_width=True, hide_index=True)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button runs the scheduler and builds a daily plan.")

if st.button("Generate schedule"):
    try:
        name = owner_name.strip() or "Owner"
        existing_owner = st.session_state.get("owner")
        if (not isinstance(existing_owner, Owner)) or (existing_owner.name != name):
            st.session_state.owner = Owner(name=name)
        owner = st.session_state.owner

        # Reuse pet from session_state (and its Task objects) when available
        pet = st.session_state.get("pet")
        if not isinstance(pet, Pet):
            pet = Pet(name=pet_name.strip() or "Pet", species=species, owner=owner)

        # Use Task objects attached to the pet if present, else fall back to legacy dicts
        if getattr(pet, "tasks", None):
            tasks = pet.tasks
        else:
            tasks = [
                Task(
                    title=task_data["title"],
                    duration_minutes=int(task_data["duration_minutes"]),
                    priority=task_data["priority"],
                )
                for task_data in st.session_state.get("tasks", [])
            ]

        scheduler = Scheduler()
        
        # Check for conflicts and display warnings
        conflicts = scheduler.detect_conflicts(tasks)
        if conflicts:
            with st.warning("⚠️ Time conflicts detected:"):
                for warning in conflicts:
                    st.write(f"- {warning}")
        
        schedule = scheduler.build_schedule(owner=owner, pet=pet, tasks=tasks)
        st.session_state.schedule = schedule
    except ValueError as validation_error:
        st.error(str(validation_error))

if st.session_state.schedule:
    schedule = st.session_state.schedule
    st.success(f"Daily schedule for {schedule.pet.name} created!")
    st.markdown(f"**Owner:** {schedule.owner.name}  ")
    st.markdown(f"**Pet:** {schedule.pet.name} ({schedule.pet.species})")
    st.markdown("---")

    if schedule.entries:
        st.success(f"✅ Scheduled {len(schedule.entries)} task(s) for {schedule.pet.name}")
        st.markdown("### Planned Tasks")
        
        plan_data = []
        for entry in schedule.entries:
            plan_data.append({
                "Time": entry.start_time,
                "Task": entry.task.title,
                "Duration (min)": entry.task.duration_minutes,
                "Priority": entry.task.priority.upper(),
                "Pet": entry.task.pet_name or "—",
            })
        
        st.dataframe(
            plan_data,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Time": st.column_config.TextColumn(width="small"),
                "Priority": st.column_config.TextColumn(width="small"),
            },
        )
    else:
        st.info("ℹ️ No tasks could be scheduled within the available time.")

    if schedule.skipped_tasks:
        st.warning(f"⚠️ {len(schedule.skipped_tasks)} task(s) could not be scheduled")
        st.markdown("### Skipped Tasks")
        # Sort skipped tasks by priority for better visibility
        sorted_skipped = scheduler.sort_by_time(schedule.skipped_tasks)
        
        skipped_data = []
        for task in sorted_skipped:
            skipped_data.append({
                "Task": task.title,
                "Duration (min)": task.duration_minutes,
                "Priority": task.priority.upper(),
                "Pet": task.pet_name or "—",
            })
        
        st.dataframe(
            skipped_data,
            use_container_width=True,
            hide_index=True,
            column_config={"Priority": st.column_config.TextColumn(width="small")},
        )

    st.markdown("### Schedule Explanation")
    st.info(schedule.explanation)
