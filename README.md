#  Smart Elevator Controller

A Smart Elevator Controller developed as a **Theory of Computation (TOC) Project** using Python and Streamlit.

The project simulates elevator operations and demonstrates the practical applications of four major concepts of Theory of Computation.

##  Project Overview

The Smart Elevator Controller allows users to:
- Enter and validate elevator commands.
- Submit multiple floor requests.
- Process requests using stack-based scheduling.
- Simulate elevator movement and state transitions.
- Detect invalid state transitions using a fault-diagnosis system.

##  Theory of Computation Concepts

| TOC Concept | Implementation | Description |
|---|---|---|
| Regular Expressions | `validation.py` | Validates elevator commands and floor requests. |
| Mealy & Moore Machines | `elevator.py` | Controls elevator states and generates outputs. |
| Pushdown Automaton (PDA) | `scheduler.py` | Uses a stack to manage pending floor requests. |
| Turing Machine | `diagnostics.py` | Scans elevator session logs and detects invalid state transitions. |

##  Project Structure

```text
Smart-Elevator-Controller/
│
├── app.py
├── requirements.txt
├── README.md
│
├── modules/
│   ├── validation.py
│   ├── elevator.py
│   ├── scheduler.py
│   ├── diagnostics.py
│   └── __init__.py
│
└── test_diagnostics.py
```

##  Technologies Used

- Python
- Streamlit
- Regular Expressions
- State Machine Simulation
- Stack-based Scheduling
- Turing Machine Simulation

##  Installation and Execution

### 1. Clone the repository

```bash
git clone https://github.com/Riddhi-Khandelwal01/Smart-Elevator-Controller.git
```

### 2. Navigate to the project directory

```bash
cd Smart-Elevator-Controller
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python -m streamlit run app.py
```

The application will open in your browser.

##  Testing

The diagnostic module is tested using valid and invalid elevator state sequences.

Run the diagnostic tests:

```bash
python test_diagnostics.py
```

### Test Case 1: Valid Session

```text
IDLE → MOVING_UP → DOOR_OPEN → IDLE
```

Expected Result: **ACCEPT**

No invalid transitions are detected.

### Test Case 2: Invalid Session

```text
IDLE → MOVING_UP → MOVING_DOWN → IDLE
```

Expected Result: **REJECT**

The system detects the invalid transition:

`MOVING_UP → MOVING_DOWN`

##  Team Contributions

| Module | Responsibility | TOC Concept |
|---|---|---|
| `validation.py` | Input validation | Regular Expressions |
| `elevator.py` | Elevator control and state transitions | Mealy & Moore Machines |
| `scheduler.py` | Floor request management | Pushdown Automaton |
| `diagnostics.py` | Fault detection and session analysis | Turing Machine |
| `app.py` | Main application and module integration | Integration |

##  Project Objective

The primary objective is to demonstrate how theoretical concepts of computation can be applied to a practical simulation system.

The project combines formal language processing, finite-state machines, stack-based computation and Turing Machine-based log analysis into one interactive elevator simulation.

---

Team Members-
Tanya Agarwal,
Anshul Kumar,
Riddhi Khandelwal,
Romit Chaudhary
