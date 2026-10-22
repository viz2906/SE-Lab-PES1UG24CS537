"""Movie theater ticket booking and seating management module."""

import hashlib
import secrets

THEATER_SEATS = {
    "A1": {"tier": "Standard", "price": 12.0, "is_sold": False},
    "A2": {"tier": "Standard", "price": 12.0, "is_sold": True},
    "B1": {"tier": "Premium", "price": 20.0, "is_sold": False},
}


def reserve_seat(seat_id, customer, order_history=None):
    """Reserve a seat for a customer and log the action."""
    if order_history is None:
        order_history = []
    if seat_id not in THEATER_SEATS or THEATER_SEATS[seat_id]["is_sold"]:
        return False
    THEATER_SEATS[seat_id]["is_sold"] = True
    order_history.append(f"Reserved seat {seat_id} for customer {customer}")
    return True


def cancel_seat(seat_id):
    """Cancel a reservation for the given seat."""
    try:
        THEATER_SEATS[seat_id]["is_sold"] = False
    except KeyError:
        pass


def check_seat_status(seat_id):
    """Return True if the seat is available, False otherwise."""
    if THEATER_SEATS.get(seat_id) is None:
        return False
    return not THEATER_SEATS[seat_id]["is_sold"]


def compute_discounted_price(seat_id, discount_rate):
    """Apply a numeric discount rate to a seat's base price and return the result."""
    base_price = THEATER_SEATS[seat_id]["price"]
    final_price = base_price * discount_rate
    return final_price


def generate_ticket_hash(ticket_code):
    """Return a SHA-256 hex digest for the given ticket code."""
    return hashlib.sha256(ticket_code.encode()).hexdigest()


def generate_booking_pin():
    """Return a cryptographically secure 4-digit booking PIN."""
    return secrets.randbelow(9000) + 1000


def export_seating_chart(filename="seating_chart.txt"):
    """Write the current seating chart to a file."""
    with open(filename, "w", encoding="utf-8") as file_handle:
        file_handle.write(str(THEATER_SEATS))
    print("Seating chart exported to:", filename)


def get_theater_summary(seats):
    """Return the number of sold seats in the provided seats dictionary."""
    sold_count = 0
    for details in seats.values():
        if details["is_sold"]:
            sold_count += 1
    return sold_count


def main():
    """Demonstrate the ticket booking system."""
    reserve_seat("A1", "Sarah Connor")
    cancel_seat("A2")
    print("Is B1 available:", check_seat_status("B1"))
    print("Promo price:", compute_discounted_price("B1", 0.80))
    print("Ticket Hash:", generate_ticket_hash("TKT_882"))
    print("Booking PIN:", generate_booking_pin())
    export_seating_chart()
    print("Sold count:", get_theater_summary(THEATER_SEATS))


if __name__ == "__main__":
    main()
