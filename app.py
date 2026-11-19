
import streamlit as st

# ==========================================
# SMART ELEVATOR CONTROLLER
# Main Application - Module Integration
# ==========================================

from modules.validation import validate_command
from modules.scheduler import RequestScheduler
from modules.elevator import Elevator
from modules.diagnostics import diagnose


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Smart Elevator Controller",
    page_icon="🛗",
    layout="wide"
)

st.title("🛗 Smart Elevator Controller")

st.caption(
    "Theory of Computation Project | "
    "Regular Expressions | Mealy & Moore Machines | "
    "PDA | Turing Machine"
)


# ==========================================
# CONSTANTS
# ==========================================

MIN_FLOOR = 1
MAX_FLOOR = 10


# ==========================================
# SESSION INITIALIZATION
# ==========================================

if "elevator" not in st.session_state:
    st.session_state.elevator = Elevator(
        initial_floor=1,
        min_floor=MIN_FLOOR,
        max_floor=MAX_FLOOR
    )

if "scheduler" not in st.session_state:
    st.session_state.scheduler = RequestScheduler(
        max_floor=MAX_FLOOR
    )

if "travel_direction" not in st.session_state:
    st.session_state.travel_direction = "UP"

if "activity_log" not in st.session_state:
    st.session_state.activity_log = [
        "Elevator initialized at Floor 1"
    ]

if "diagnostic_log" not in st.session_state:
    st.session_state.diagnostic_log = ["IDLE"]


elevator = st.session_state.elevator
scheduler = st.session_state.scheduler


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def add_activity(message):
    """Store activity in chronological order."""
    st.session_state.activity_log.append(message)


def add_diagnostic_state(state):
    """Record valid state symbols for the Turing Machine."""
    st.session_state.diagnostic_log.append(state)


def get_scan_next_request():
    """
    Direction-based SCAN scheduling.

    The stack remains in scheduler.py for PDA demonstration.
    The application selects the nearest request in the
    current direction.
    """

    pending = scheduler.get_pending_requests()

    if not pending:
        return None

    current = elevator.current_floor
    direction = st.session_state.travel_direction

    # If current floor is requested, service it first.
    if current in pending:
        return current

    # Moving UP: select the nearest higher floor.
    if direction == "UP":

        upward_requests = [
            floor for floor in pending
            if floor > current
        ]

        if upward_requests:
            return min(upward_requests)

        # No requests above: reverse direction.
        st.session_state.travel_direction = "DOWN"

    # Moving DOWN: select the nearest lower floor.
    if st.session_state.travel_direction == "DOWN":

        downward_requests = [
            floor for floor in pending
            if floor < current
        ]

        if downward_requests:
            return max(downward_requests)

        # No requests below: reverse direction.
        st.session_state.travel_direction = "UP"

    # Retry with the new direction.
    return get_scan_next_request()


def process_next_request():
    """Process the next request using SCAN scheduling."""

    if elevator.state == "DOOR_OPEN":
        add_activity(
            "Cannot move: Close the elevator door first."
        )
        return

    target = get_scan_next_request()

    if target is None:
        add_activity("No pending floor requests.")
        return

    previous_floor = elevator.current_floor

    # Remove selected request from the original stack.
    scheduler.cancel_request(target)

    # Determine actual movement direction.
    if target > previous_floor:

        direction = "UP"
        add_diagnostic_state("MOVING_UP")

    elif target < previous_floor:

        direction = "DOWN"
        add_diagnostic_state("MOVING_DOWN")

    else:
        direction = "NONE"

    # Execute original elevator state-machine logic.
    journey = elevator.move_to_floor(target)

    # Store events in their actual execution order.
    for event in journey:
        add_activity(event)

    # Record arrival as IDLE for compatibility
    # with the original diagnostics module.
    if elevator.current_floor == target:
        add_diagnostic_state("IDLE")

    # Update direction after movement.
    # Keep direction while there are more requests
    # in the same direction.
    remaining = scheduler.get_pending_requests()

    if not remaining:
        st.session_state.travel_direction = "UP"

    elif direction != "NONE":
        if direction == "UP":
            if not any(
                floor > elevator.current_floor
                for floor in remaining
            ):
                st.session_state.travel_direction = "DOWN"

        elif direction == "DOWN":
            if not any(
                floor < elevator.current_floor
                for floor in remaining
            ):
                st.session_state.travel_direction = "UP"


# ==========================================
# ELEVATOR STATUS
# ==========================================

st.divider()
st.header("1. Elevator Status")

status = elevator.get_status()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Current Floor",
        status["current_floor"]
    )

with col2:
    st.metric(
        "Elevator State",
        status["state"]
    )

with col3:
    st.metric(
        "Direction",
        status["direction"]
    )

st.info(
    "Moore Machine Output: " + status["moore_output"]
)


# ==========================================
# COMMAND VALIDATION
# ==========================================

st.divider()
st.header("2. Command Input")

st.write(
    "Enter a floor request or door operation."
)

st.code(
    "FLOOR:5\nDOOR:OPEN\nDOOR:CLOSE"
)

with st.form("command_form", clear_on_submit=True):

    command = st.text_input(
        "Enter Command",
        placeholder="Example: FLOOR:5"
    )

    submit = st.form_submit_button(
        "Submit Command"
    )


if submit:

    try:

        validated = validate_command(
            command,
            max_floor=MAX_FLOOR
        )

        if validated.startswith("FLOOR:"):

            floor = int(validated.split(":")[1])

            if floor < MIN_FLOOR:
                raise ValueError(
                    "Floor must be between 1 and 10."
                )

            added = scheduler.add_request(floor)

            if added:

                add_activity(
                    f"Floor {floor} request added successfully."
                )

            else:

                add_activity(
                    f"Floor {floor} is already pending."
                )

        elif validated == "DOOR:OPEN":

            result = elevator.open_door()

            add_activity(result)

            if elevator.state == "DOOR_OPEN":
                add_diagnostic_state("DOOR_OPEN")

        elif validated == "DOOR:CLOSE":

            result = elevator.close_door()

            add_activity(result)

            if elevator.state == "IDLE":
                add_diagnostic_state("IDLE")

    except ValueError as error:

        add_activity(
            f"Validation Error: {error}"
        )


# ==========================================
# REQUEST SCHEDULER
# ==========================================

st.divider()
st.header("3. Floor Request Scheduler")

st.write(
    "PDA Concept: Requests are stored in a stack. "
    "The application uses direction-based SCAN selection "
    "to choose which pending request to service."
)

pending = scheduler.get_pending_requests()

col1, col2 = st.columns(2)

with col1:

    st.write("**Pending Requests:**")

    if pending:
        st.write(
            sorted(pending)
        )
    else:
        st.write("No pending requests.")

with col2:

    st.write("**Current Travel Direction:**")

    st.write(
    st.session_state.travel_direction
    if scheduler.get_pending_requests()
    else "IDLE"
)


st.write(
    "**Next Floor to be Serviced:**",
    get_scan_next_request()
)


col1, col2 = st.columns(2)

with col1:

    if st.button(
        "Process Next Request",
        use_container_width=True
    ):

        process_next_request()
        st.rerun()


with col2:

    if st.button(
        "Clear All Requests",
        use_container_width=True
    ):

        scheduler.clear_requests()

        st.session_state.travel_direction = "UP"

        add_activity(
            "All pending requests cleared."
        )

        st.rerun()


# ==========================================
# ACTIVITY LOG
# ==========================================

st.divider()
st.header("4. Elevator Activity Log")

st.caption(
    "Events are displayed in chronological order."
)

if st.session_state.activity_log:

    for index, event in enumerate(
        st.session_state.activity_log,
        start=1
    ):

        st.write(f"{index}. {event}")

else:

    st.write("No activity recorded.")


# ==========================================
# TURING MACHINE DIAGNOSTICS
# ==========================================

st.divider()
st.header("5. Fault Diagnosis - Turing Machine")

st.write(
    "The Turing Machine scans the session state tape "
    "and detects invalid state transitions."
)

st.write("**Session State Tape:**")

st.code(
    " → ".join(st.session_state.diagnostic_log)
)

if st.button(
    "Run Fault Diagnosis",
    type="primary"
):

    report = diagnose(
        st.session_state.diagnostic_log
    )

    if report["status"] == "ACCEPT":

        st.success(
            "ACCEPT: No invalid state transitions detected."
        )

    else:

        st.error(
            "REJECT: Anomalies detected."
        )

    st.write(
        "**Machine Status:**",
        report["status"]
    )

    st.write(
        "**Events Scanned:**",
        report["scanned_events"]
    )

    st.write(
        "**Total Events:**",
        report["total_events"]
    )

    if report["anomalies"]:

        st.subheader("Detected Anomalies")

        for anomaly in report["anomalies"]:
            st.warning(anomaly)


# ==========================================
# RAW ELEVATOR EVENT LOG
# ==========================================

with st.expander(
    "View Original Elevator Event Log"
):

    for index, event in enumerate(
        elevator.get_event_log(),
        start=1
    ):

        st.write(f"{index}. {event}")


# ==========================================
# RESET SIMULATION
# ==========================================

st.divider()

if st.button(
    "Reset Elevator Simulation",
    use_container_width=True
):

    st.session_state.elevator = Elevator(
        initial_floor=1,
        min_floor=MIN_FLOOR,
        max_floor=MAX_FLOOR
    )

    st.session_state.scheduler = RequestScheduler(
        max_floor=MAX_FLOOR
    )

    st.session_state.travel_direction = "UP"

    st.session_state.activity_log = [
        "Elevator initialized at Floor 1"
    ]

    st.session_state.diagnostic_log = [
        "IDLE"
    ]

    st.rerun()
