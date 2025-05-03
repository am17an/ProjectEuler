def simulate_hilbert_hotel(num_guests):
    """
    Simulate the Hilbert hotel room assignment for a given number of guests.
    Returns a 2D matrix where matrix[floor][room] = person number (or 0 if vacant)
    """
    # Initialize hotel as a dictionary of dictionaries
    # hotel[floor][room] = person number
    hotel = {}
    
    # Track the latest person on each floor
    latest_person_on_floor = {}
    
    # Process each guest
    for person in range(1, num_guests + 1):
        assigned = False
        floor = 1
        
        while not assigned:
            # Initialize floor if needed
            if floor not in hotel:
                hotel[floor] = {}
                latest_person_on_floor[floor] = 0
            
            # Check if floor is empty
            if latest_person_on_floor[floor] == 0:
                # Assign to first room on empty floor
                room = 1
                hotel[floor][room] = person
                latest_person_on_floor[floor] = person
                assigned = True
            else:
                # Check the perfect square rule
                m = latest_person_on_floor[floor]
                if is_perfect_square(m + person):
                    # Find the first vacant room on this floor
                    room = 1
                    while room in hotel[floor]:
                        room += 1
                    
                    # Assign the room
                    hotel[floor][room] = person
                    latest_person_on_floor[floor] = person
                    assigned = True
                else:
                    # Try the next floor
                    floor += 1
    
    return hotel

def is_perfect_square(n):
    """Check if a number is a perfect square."""
    root = int(n ** 0.5)
    return root * root == n

def P(hotel, f, r):
    """Return the person number in room r on floor f, or 0 if vacant."""
    if f in hotel and r in hotel[f]:
        return hotel[f][r]
    return 0

# Run the simulation for 100 guests
hotel = simulate_hilbert_hotel(10000)

# Print some examples to verify
examples = [
    (1, 1),
    (1, 2),
    (2, 1),
    (10, 20),
    (25, 75),
    (99, 100)
]

print("Verification examples:")
for f, r in examples:
    print(f"P({f}, {r}) = {P(hotel, f, r)}")

# Print the assignment matrix for the first few floors and rooms
print("\nRoom assignment matrix (first 10 floors, first 10 rooms per floor):")
for f in range(1, 100):
    row = [P(hotel, f, r) for r in range(1, 1000) if P(hotel, f, r) != 0]
    print(f"Floor {f}: {row}")

print("\nValues of P(f,r) where f×r is of the form 2^j * 3^k:")
powers = []
for j in range(8):  # 2^0 to 2^7
    for k in range(5):  # 3^0 to 3^4
        product = (2 ** j) * (3 ** k)
        
        # Find all factor pairs for this product
        factors = []
        for f in range(1, int(product**0.5) + 1):
            if product % f == 0:
                r = product // f
                factors.append((f, r))
        
        powers.extend(factors)

# Remove duplicates and sort by floor, then room
powers = list(set(powers))
powers.sort()

# Print in a formatted table
print(f"{'Floor':^8} | {'Room':^8} | {'f×r':^8} | {'Person':^8}")
print("-" * 40)
for f, r in powers:
    person = P(hotel, f, r)
    product = f * r
    print(f"{f:^8} | {r:^8} | {product:^8} | {person:^8}")