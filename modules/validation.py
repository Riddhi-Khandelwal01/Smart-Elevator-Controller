"""Regular-expression validation for Smart Elevator Controller inputs.

Accepted commands (spaces around a command are ignored):
    FLOOR:<number>   Request a floor from 0 through max_floor (default 10).
    DOOR:OPEN        Request that the doors open.
    DOOR:CLOSE       Request that the doors close.

Example:
    from modules.validation import validate_command

    command = validate_command(" floor:4 ")  # returns "FLOOR:4"
"""

import re


FLOOR_PATTERN = re.compile(r"^FLOOR:(\d+)$")
DOOR_PATTERN = re.compile(r"^DOOR:(OPEN|CLOSE)$")


def validate_command(command, max_floor=10):
    """Validate one command and return it in a standard format.

    Args:
        command: Text entered by the user, such as ``FLOOR:4`` or
            ``DOOR:OPEN``.
        max_floor: Highest allowed floor number. Floor zero is allowed.

    Returns:
        The validated command in uppercase, with surrounding spaces removed.

    Raises:
        ValueError: If the command has an invalid format or floor number.
    """
    if not isinstance(command, str):
        raise ValueError("Command must be text.")

    if not isinstance(max_floor, int) or max_floor < 0:
        raise ValueError("max_floor must be a non-negative integer.")

    cleaned_command = command.strip().upper()

    floor_match = FLOOR_PATTERN.fullmatch(cleaned_command)
    if floor_match:
        floor_number = int(floor_match.group(1))
        if floor_number > max_floor:
            raise ValueError(
                f"Floor must be between 0 and {max_floor}."
            )
        return f"FLOOR:{floor_number}"

    if DOOR_PATTERN.fullmatch(cleaned_command):
        return cleaned_command

    raise ValueError(
        "Invalid command. Use FLOOR:<number>, DOOR:OPEN, or DOOR:CLOSE."
    )


def validate_event_sequence(commands, max_floor=10):
    """Validate a list of commands, including basic door-state order.

    The sequence starts with the doors closed. Repeated OPEN or CLOSE
    commands are rejected because they do not change the door state.
    Commands are returned in their normalized format.

    Raises:
        ValueError: If a command is malformed, out of range, or repeats the
            current door state. The message identifies the command position.
    """
    if not isinstance(commands, (list, tuple)):
        raise ValueError("Commands must be provided as a list or tuple.")

    validated_commands = []
    doors_are_open = False

    for position, command in enumerate(commands, start=1):
        try:
            validated = validate_command(command, max_floor)
        except ValueError as error:
            raise ValueError(f"Command {position}: {error}") from None

        if validated == "DOOR:OPEN":
            if doors_are_open:
                raise ValueError(
                    f"Command {position}: doors are already open."
                )
            doors_are_open = True
        elif validated == "DOOR:CLOSE":
            if not doors_are_open:
                raise ValueError(
                    f"Command {position}: doors are already closed."
                )
            doors_are_open = False

        validated_commands.append(validated)

    return validated_commands
