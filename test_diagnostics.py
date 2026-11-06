
from modules.diagnostics import diagnose

valid_log = [
    "IDLE",
    "MOVING_UP",
    "DOOR_OPEN",
    "IDLE"
]

invalid_log = [
    "IDLE",
    "MOVING_UP",
    "MOVING_DOWN",
    "IDLE"
]

print("VALID SESSION:")
print(diagnose(valid_log))

print("\nINVALID SESSION:")
print(diagnose(invalid_log))
