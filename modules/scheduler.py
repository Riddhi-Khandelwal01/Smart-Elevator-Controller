"""
SMART ELEVATOR CONTROLLER
Member 3: Request Scheduler

TOC Concept:
Pushdown Automaton (PDA)
Stack-Based Scheduling

Author: Member 3
"""


class RequestScheduler:

    def __init__(self, max_floor=10):

        self.max_floor = max_floor

        # Stack stores pending floor requests
        self.stack = []

    # -----------------------------------------
    # 1. VALIDATE FLOOR REQUEST
    # -----------------------------------------

    def validate_floor(self, floor):

        if not isinstance(floor, int) or isinstance(floor, bool):
            raise ValueError("Floor must be an integer.")

        if floor < 1 or floor > self.max_floor:
            raise ValueError(
                f"Floor must be between 1 and {self.max_floor}."
            )

        return True

    # -----------------------------------------
    # 2. PUSH OPERATION
    # -----------------------------------------

    def add_request(self, floor):

        self.validate_floor(floor)

        # Prevent duplicate pending requests
        if floor in self.stack:
            return False

        # PUSH request onto stack
        self.stack.append(floor)

        return True

    # -----------------------------------------
    # 3. POP OPERATION
    # -----------------------------------------

    def get_next_request(self):

        if not self.stack:
            return None

        # POP the latest request
        return self.stack.pop()

    # -----------------------------------------
    # 4. PEEK OPERATION
    # -----------------------------------------

    def peek_next_request(self):

        if not self.stack:
            return None

        # View top element without removing it
        return self.stack[-1]

    # -----------------------------------------
    # 5. GET PENDING REQUESTS
    # -----------------------------------------

    def get_pending_requests(self):

        return self.stack.copy()

    # -----------------------------------------
    # 6. CANCEL REQUEST
    # -----------------------------------------

    def cancel_request(self, floor):

        self.validate_floor(floor)

        if floor not in self.stack:
            return False

        self.stack.remove(floor)

        return True

    # -----------------------------------------
    # 7. CHECK PENDING REQUESTS
    # -----------------------------------------

    def has_pending_requests(self):

        return len(self.stack) > 0

    # -----------------------------------------
    # 8. COUNT REQUESTS
    # -----------------------------------------

    def total_requests(self):

        return len(self.stack)

    # -----------------------------------------
    # 9. CLEAR ALL REQUESTS
    # -----------------------------------------

    def clear_requests(self):

        self.stack.clear()

        return True

    # -----------------------------------------
    # 10. GET SCHEDULER STATUS
    # -----------------------------------------

    def get_status(self):

        return {
            "pending_requests": self.get_pending_requests(),
            "total_requests": self.total_requests(),
            "next_request": self.peek_next_request(),
            "is_empty": not self.has_pending_requests()
        }


# =============================================
# INDEPENDENT TESTING
# =============================================

if __name__ == "__main__":

    scheduler = RequestScheduler(max_floor=10)

    print("\n===================================")
    print(" SMART ELEVATOR REQUEST SCHEDULER")
    print("===================================")

    # Add floor requests
    print("\n1. Adding Floor Requests")

    print("Floor 3:", scheduler.add_request(3))
    print("Floor 5:", scheduler.add_request(5))
    print("Floor 8:", scheduler.add_request(8))

    # Display stack
    print("\n2. Pending Requests")

    print(scheduler.get_pending_requests())

    # Check top element
    print("\n3. PEEK Operation")

    print("Next Request:", scheduler.peek_next_request())

    # Process request
    print("\n4. POP Operation")

    print("Processed Request:", scheduler.get_next_request())

    # Remaining requests
    print("\n5. Remaining Requests")

    print(scheduler.get_pending_requests())

    # Duplicate test
    print("\n6. Duplicate Request Test")

    print("Add Floor 5 Again:", scheduler.add_request(5))

    # Cancel request
    print("\n7. Cancel Request")

    print("Cancel Floor 3:", scheduler.cancel_request(3))

    # Check status
    print("\n8. Scheduler Status")

    print(scheduler.get_status())

    # Empty stack test
    print("\n9. Clear All Requests")

    scheduler.clear_requests()

    print("Is Empty:", not scheduler.has_pending_requests())

    print("\n===================================")
    print(" TESTING COMPLETED SUCCESSFULLY")
    print("===================================")
