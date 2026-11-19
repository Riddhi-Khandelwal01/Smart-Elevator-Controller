
import streamlit as st

# Importing all four team members' modules
from modules.validation import validate_command
from modules.scheduler import RequestScheduler
from modules.elevator import Elevator
from modules.diagnostics import diagnose


# -----------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------

st.set_page_config(
    page_title="Smart Elevator Controller",
    page_icon="🛗",
    layout="wide"
)

st.title("🛗 Smart Elevator Controller")
st.subheader("Theory of Computation Project")

st.write(
    "An elevator simulation demonstrating Regular Expressions, "
    "Mealy and Moore Machines, Pushdown Automata and Turing Machines."
)


# -----------------------------------------
# INITIALIZE SESSION STATE
# -----------------------------------------

if "elevator" not in st.session_state:
    st.session_state.elevator = Elevator(
        initial_floor=1,
        min_floor=1,
        max_floor=10
    )

if "scheduler" not in st.session_state:
    st.session_state.scheduler = RequestScheduler(max_floor=10)

if "diagnostic_log" not in st.session_state:
    st.session_state.diagnostic_log = ["IDLE"]

if "messages" not in st.session_state:
    st.session_state.messages = []


elevator = st.session_state.elevator
scheduler = st.session_state.scheduler


# -----------------------------------------
# HELPER FUNCTION
# -----------------------------------------

def add_message(message, message_type="info"):
    st.session_state.messages.append(
        (message, message_type)
    )


# -----------------------------------------
# ELEVATOR STATUS
# -----------------------------------------

st.divider()
st.header("1. Elevator Status")

col1, col2, col3 = st.columns(3)

status = elevator.get_status()

with col1:
    st.metric(
        "Current Floor",
        status["current_floor"]
    )

with col2:
    st.metric(
        "Current State",
        status["state"]
    )

with col3:
    st.metric(
        "Direction",
        status["direction"]
    )

st.info("Moore Machine Output: " + status["moore_output"])


# -----------------------------------------
# USER INPUT AND VALIDATION
# -----------------------------------------

st.divider()
st.header("2. Enter Elevator Command")

st.write("Available commands:")
st.code("FLOOR:5\nDOOR:OPEN\nDOOR:CLOSE")

with st.form("command_form"):
    command = st.text_input(
        "Enter your command",
        placeholder="Example: FLOOR:5"
    )

    submit = st.form_submit_button(
        "Submit Command"
    )


if submit:

    try:
        # Member 1: Regular Expression Validation
        validated_command = validate_command(
            command,
            max_floor=10
        )

        # Floor request
        if validated_command.startswith("FLOOR:"):

            floor = int(validated_command.split(":")[1])

            # Member 3: Stack-based Scheduler
            # Scheduler independently validates floors 1-10.
            added = scheduler.add_request(floor)

            if added:
                add_message(
                    f"Floor {floor} request added successfully.",
                    "success"
                )
            else:
                add_message(
                    f"Floor {floor} is already in the pending stack.",
                    "warning"
                )

        # Door opening
        elif validated_command == "DOOR:OPEN":

            result = elevator.open_door()
            add_message(result)

            if elevator.state == "DOOR_OPEN":
                st.session_state.diagnostic_log.append(
                    "DOOR_OPEN"
                )

        # Door closing
        elif validated_command == "DOOR:CLOSE":

            result = elevator.close_door()
            add_message(result)

            if elevator.state == "IDLE":
                st.session_state.diagnostic_log.append(
                    "IDLE"
                )

    except ValueError as error:

        add_message(
            str(error),
            "error"
        )


# -----------------------------------------
# REQUEST SCHEDULER
# -----------------------------------------

st.divider()
st.header("3. Request Scheduler (PDA)")

st.write(
    "The scheduler uses a stack. "
    "The latest request is processed first (LIFO)."
)

st.write(
    "**Pending Floor Requests:**",
    scheduler.get_pending_requests()
)

st.write(
    "**Next Request:**",
    scheduler.peek_next_request()
)

col1, col2 = st.columns(2)

with col1:

    if st.button("Process Next Request"):

        if elevator.state == "DOOR_OPEN":

            add_message(
                "Close the elevator door before moving.",
                "error"
            )

        else:

            # Member 3: POP operation
            target_floor = scheduler.get_next_request()

            if target_floor is None:

                add_message(
                    "No pending floor requests.",
                    "warning"
                )

            else:

                previous_floor = elevator.current_floor

                # Member 2: Mealy and Moore Machine
                result = elevator.move_to_floor(
                    target_floor
                )

                for event in result:
                    add_message(event)

                # Record the movement in the diagnostic tape.
                # ARRIVED is represented as IDLE here because
                # the original diagnostics module does not
                # include ARRIVED in its VALID_STATES.

                if elevator.current_floor != previous_floor:

                    if target_floor > previous_floor:
                        st.session_state.diagnostic_log.append(
                            "MOVING_UP"
                        )

                    else:
                        st.session_state.diagnostic_log.append(
                            "MOVING_DOWN"
                        )

                    st.session_state.diagnostic_log.append(
                        "IDLE"
                    )


with col2:

    if st.button("Clear All Requests"):

        scheduler.clear_requests()

        add_message(
            "All pending requests cleared.",
            "success"
        )


# -----------------------------------------
# ACTIVITY LOG
# -----------------------------------------

st.divider()
st.header("4. Elevator Activity Log")

if st.session_state.messages:

    for message, message_type in reversed(
        st.session_state.messages[-10:]
    ):

        if message_type == "success":
            st.success(message)

        elif message_type == "warning":
            st.warning(message)

        elif message_type == "error":
            st.error(message)

        else:
            st.info(message)

else:

    st.write("No activity recorded yet.")


# -----------------------------------------
# TURING MACHINE DIAGNOSTICS
# -----------------------------------------

st.divider()
st.header("5. Fault Diagnosis (Turing Machine)")

st.write(
    "The diagnostic module scans the session state sequence "
    "and checks whether the transitions are valid."
)

st.write(
    "**Session State Tape:**",
    " → ".join(st.session_state.diagnostic_log)
)

if st.button("Run Fault Diagnosis"):

    # Member 4: Original Turing Machine implementation
    report = diagnose(
        st.session_state.diagnostic_log
    )

    if report["status"] == "ACCEPT":

        st.success(
            "ACCEPT: No invalid state transitions detected."
        )

    else:

        st.error(
            "REJECT: Anomalies detected in the session."
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


# -----------------------------------------
# RAW ELEVATOR EVENT LOG
# -----------------------------------------

with st.expander("View Complete Elevator Event Log"):

    for event in elevator.get_event_log():
        st.write("•", event)


# -----------------------------------------
# RESET SIMULATION
# -----------------------------------------

st.divider()

if st.button("Reset Elevator Simulation"):

    st.session_state.elevator = Elevator(
        initial_floor=1,
        min_floor=1,
        max_floor=10
    )

    st.session_state.scheduler = RequestScheduler(
        max_floor=10
    )

    st.session_state.diagnostic_log = ["IDLE"]
    st.session_state.messages = []

    st.rerun()

