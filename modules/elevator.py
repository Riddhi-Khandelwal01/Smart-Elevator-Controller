"""
Smart Elevator Controller
Member 2: Core Elevator Control

TOC Concepts:
1. Mealy Machine - actions depend on current state + input
2. Moore Machine - output depends only on current state
"""


class Elevator:
    # -------------------- INITIALIZATION --------------------

    def __init__(self, initial_floor=1, min_floor=1, max_floor=10):
        self.current_floor = initial_floor
        self.min_floor = min_floor
        self.max_floor = max_floor

        # Elevator states
        self.state = "IDLE"

        # Elevator direction
        self.direction = "NONE"

        # Stores all events for diagnostics
        self.event_log = []

        self.log_event(
            f"Elevator initialized at Floor {self.current_floor}"
        )

    # -------------------- EVENT LOG --------------------

    def log_event(self, event):
        """Store an event in the elevator session log."""
        self.event_log.append(event)

    def get_event_log(self):
        """Return the complete session log."""
        return self.event_log.copy()

    # -------------------- MOORE MACHINE --------------------

    def get_moore_output(self):
        """
        Moore Machine:
        The output depends ONLY on the current state.
        """

        outputs = {
            "IDLE": "Elevator is waiting",
            "MOVING_UP": "Elevator is moving up",
            "MOVING_DOWN": "Elevator is moving down",
            "ARRIVED": "Elevator has reached the destination",
            "DOOR_OPEN": "Elevator door is open"
        }

        return outputs.get(self.state, "Unknown elevator state")

    # -------------------- MEALY MACHINE --------------------

    def request_floor(self, target_floor):
        """
        Mealy Machine:
        Action depends on the current state and the input
        (requested floor).
        """

        # Check whether the floor is within the elevator range
        if target_floor < self.min_floor or target_floor > self.max_floor:
            action = f"Invalid floor: {target_floor}"
            self.log_event(action)
            return action

        # Elevator should not accept a new movement request
        # while its door is open
        if self.state == "DOOR_OPEN":
            action = "Cannot move: Please close the door first"
            self.log_event(action)
            return action

        # Requested floor is the current floor
        if target_floor == self.current_floor:
            self.state = "ARRIVED"
            self.direction = "NONE"

            action = (
                f"Already at Floor {self.current_floor}. "
                "Destination reached."
            )

        # Requested floor is above the current floor
        elif target_floor > self.current_floor:
            self.state = "MOVING_UP"
            self.direction = "UP"

            action = (
                f"Motor started: Moving UP towards Floor {target_floor}"
            )

        # Requested floor is below the current floor
        else:
            self.state = "MOVING_DOWN"
            self.direction = "DOWN"

            action = (
                f"Motor started: Moving DOWN towards Floor {target_floor}"
            )

        self.log_event(action)
        return action

    # -------------------- ELEVATOR MOVEMENT --------------------

    def move_one_floor(self):
        """Move the elevator by one floor according to its state."""

        if self.state == "MOVING_UP":
            if self.current_floor < self.max_floor:
                self.current_floor += 1

                event = f"Moved UP to Floor {self.current_floor}"
                self.log_event(event)

                return event

        elif self.state == "MOVING_DOWN":
            if self.current_floor > self.min_floor:
                self.current_floor -= 1

                event = f"Moved DOWN to Floor {self.current_floor}"
                self.log_event(event)

                return event

        return "Elevator is not currently moving"

    # -------------------- DESTINATION CHECK --------------------

    def check_destination(self, target_floor):
        """
        Check whether the elevator has reached its destination.
        """

        if self.current_floor == target_floor:
            self.state = "ARRIVED"
            self.direction = "NONE"

            event = f"Arrived at Floor {self.current_floor}"
            self.log_event(event)

            return True

        return False

    # -------------------- DOOR CONTROL --------------------

    def open_door(self):
        """Open the door only when the elevator has arrived."""

        if self.state == "ARRIVED" or self.state == "IDLE":

            self.state = "DOOR_OPEN"

            event = (
                f"Door opened at Floor {self.current_floor}"
            )

            self.log_event(event)

            return event

        event = "Cannot open door while elevator is moving"
        self.log_event(event)

        return event

    def close_door(self):
        """Close the door and return the elevator to IDLE state."""

        if self.state == "DOOR_OPEN":

            self.state = "IDLE"
            self.direction = "NONE"

            event = "Door closed. Elevator is now IDLE."

            self.log_event(event)

            return event

        event = "Door is already closed"
        self.log_event(event)

        return event

    # -------------------- COMPLETE MOVEMENT --------------------

    def move_to_floor(self, target_floor):
        """
        Complete elevator journey to the requested floor.

        This method can be used by app.py for a simple simulation.
        """

        result = []

        # Start movement using Mealy Machine logic
        action = self.request_floor(target_floor)
        result.append(action)

        # Stop if the request was invalid
        if target_floor < self.min_floor or target_floor > self.max_floor:
            return result

        # Stop if the door is open
        if self.state == "DOOR_OPEN":
            return result

        # Move floor by floor
        while self.current_floor != target_floor:
            result.append(self.move_one_floor())

        # Destination reached
        if self.check_destination(target_floor):
            result.append(
                f"Destination Floor {target_floor} reached"
            )

        return result

    # -------------------- STATUS --------------------

    def get_status(self):
        """
        Return the current elevator status.
        This can be displayed in the Streamlit interface.
        """

        return {
            "current_floor": self.current_floor,
            "state": self.state,
            "direction": self.direction,
            "moore_output": self.get_moore_output()
        }


# ============================================================
# TESTING SECTION
# This runs only when elevator.py is executed directly.
# ============================================================

if __name__ == "__main__":

    elevator = Elevator(initial_floor=2)

    print("\n===== SMART ELEVATOR CONTROLLER TEST =====\n")

    print("Initial Status:")
    print(elevator.get_status())

    print("\nRequesting Floor 5...\n")

    journey = elevator.move_to_floor(5)

    for event in journey:
        print(event)

    print("\nCurrent Status:")
    print(elevator.get_status())

    print("\nOpening Door:")
    print(elevator.open_door())

    print("\nClosing Door:")
    print(elevator.close_door())

    print("\nFinal Status:")
    print(elevator.get_status())

    print("\n===== EVENT LOG =====")

    for event in elevator.get_event_log():
        print(event)
