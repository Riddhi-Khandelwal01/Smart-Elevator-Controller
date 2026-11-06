
# SMART ELEVATOR CONTROLLER
# Member 4 - Turing Machine Based Fault Diagnosis

# Valid elevator states
VALID_STATES = {
    "IDLE",
    "MOVING_UP",
    "MOVING_DOWN",
    "DOOR_OPEN"
}

# Allowed state transitions
VALID_TRANSITIONS = {
    "IDLE": ["IDLE", "MOVING_UP", "MOVING_DOWN", "DOOR_OPEN"],
    "MOVING_UP": ["MOVING_UP", "DOOR_OPEN", "IDLE"],
    "MOVING_DOWN": ["MOVING_DOWN", "DOOR_OPEN", "IDLE"],
    "DOOR_OPEN": ["DOOR_OPEN", "IDLE"]
}


def get_state(entry):
    """Extract elevator state from log entry."""

    if isinstance(entry, str):
        return entry

    if isinstance(entry, dict):
        if "to" in entry:
            return entry["to"]

        if "state" in entry:
            return entry["state"]

    return None


def run_turing_machine(session_log):
    """Simulate Turing Machine for fault detection."""

    tape = session_log.copy()
    head = 0

    machine_state = "SCANNING"
    anomalies = []
    states = []

    # Scan session log one entry at a time
    while head < len(tape):

        current = get_state(tape[head])

        # Check invalid states
        if current not in VALID_STATES:
            anomalies.append(
                f"Invalid state at position {head}: {current}"
            )
            machine_state = "REJECT"
            head += 1
            continue

        states.append(current)

        # Check state transitions
        if len(states) > 1:

            previous = states[-2]

            if current not in VALID_TRANSITIONS[previous]:

                anomalies.append(
                    f"Invalid transition: {previous} -> {current}"
                )

                machine_state = "REJECT"

        # Move read head forward
        head += 1

    # Final decision
    if len(tape) == 0:
        machine_state = "REJECT"
        anomalies.append("Session log is empty")

    elif len(anomalies) == 0:
        machine_state = "ACCEPT"

    return {
        "status": machine_state,
        "anomalies": anomalies,
        "scanned_events": head,
        "total_events": len(tape)
    }


def diagnose(session_log):
    """Generate final diagnostic report."""

    return run_turing_machine(session_log)
