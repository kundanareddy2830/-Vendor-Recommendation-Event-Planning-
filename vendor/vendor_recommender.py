import json
from itertools import combinations
import os

# Step 1: Get user input
def get_user_input():
    print('Welcome to the Vendor Recommender!')
    event_type = input('Enter event type (e.g., Wedding, Birthday, Corporate): ')
    location = input('Enter location (e.g., Hyderabad, Bangalore): ')
    budget = int(input('Enter your budget (e.g., 100000): '))
    return event_type, location, budget

# Step 2: Load mock vendor data
def load_vendor_data(filename=None):
    if filename is None:
        # Always load from the same directory as this script
        filename = os.path.join(os.path.dirname(__file__), 'mock_data.json')
    with open(filename, 'r') as f:
        return json.load(f)

# Step 3: Filter vendors by location
def filter_vendors_by_location(vendors, location):
    location = location.lower()
    return [v for v in vendors if location in v['location'].lower()]

# Step 4: Group vendors by service
def group_vendors_by_service(vendors):
    services = {}
    for v in vendors:
        services.setdefault(v['service'], []).append(v)
    for service in services:
        services[service].sort(key=lambda x: (-x['rating'], x['price']))
    return services

# Step 5: Show all vendors by service
def show_all_vendors(services):
    print('\nAll available vendors by service:')
    for service, vendors in services.items():
        print(f'\nService: {service}')
        for idx, v in enumerate(vendors, 1):
            print(f"  {idx}. {v['name']} (Price: ₹{v['price']}, Rating: {v['rating']}, Location: {v['location']})")

# Step 6: Select top-rated vendors under budget
def recommend_vendors(vendors, budget):
    services = group_vendors_by_service(vendors)
    service_lists = [services[s] for s in services]
    best_combo = None
    best_score = -1
    for combo in zip(*service_lists):
        total_price = sum(v['price'] for v in combo)
        if total_price <= budget:
            score = sum(v['rating'] for v in combo)
            if score > best_score:
                best_score = score
                best_combo = combo
    if not best_combo:
        all_vendors = [v for sublist in service_lists for v in sublist]
        for r in range(len(service_lists), 0, -1):
            for combo in combinations(all_vendors, r):
                service_set = set(v['service'] for v in combo)
                if len(service_set) != len(combo):
                    continue
                total_price = sum(v['price'] for v in combo)
                if total_price <= budget:
                    score = sum(v['rating'] for v in combo)
                    if score > best_score:
                        best_score = score
                        best_combo = combo
            if best_combo:
                break
    return list(best_combo) if best_combo else []

# Step 7: Suggest planning steps
def suggest_planning_steps(event_type):
    steps = {
        'wedding': ['Book venue', 'Book decoration', 'Book catering', 'Book photographer'],
        'birthday': ['Book venue', 'Book decoration', 'Book cake', 'Book photographer'],
        'corporate': ['Book venue', 'Book catering', 'Book AV equipment', 'Book decoration']
    }
    return steps.get(event_type.lower(), ['Book venue', 'Book vendors'])

# --- Core Logic as Functions ---
def closest_possible_set(vendors):
    services = group_vendors_by_service(vendors)
    all_vendors = [v for sublist in services.values() for v in sublist]
    best_combo = None
    best_score = -1
    for r in range(len(services), 0, -1):
        for combo in combinations(all_vendors, r):
            if len(set(v['service'] for v in combo)) != len(combo):
                continue
            score = sum(v['rating'] for v in combo)
            if score > best_score:
                best_score = score
                best_combo = combo
        if best_combo:
            break
    return list(best_combo) if best_combo else []

# --- CLI Entrypoint (optional, for local testing) ---
if __name__ == '__main__':
    event_type, location, budget = get_user_input()
    vendors = load_vendor_data()
    filtered_vendors = filter_vendors_by_location(vendors, location)
    services = group_vendors_by_service(filtered_vendors)
    show_all_vendors(services)
    recommended = recommend_vendors(filtered_vendors, budget)
    print('\nRecommended Vendors (Best Combo Under Budget):')
    if recommended:
        for v in recommended:
            print(f"- {v['service']}: {v['name']} (Price: ₹{v['price']}, Rating: {v['rating']})")
        total = sum(v['price'] for v in recommended)
        print(f"Total Estimated Cost: ₹{total}")
        if total < budget:
            print(f"You have ₹{budget-total} remaining in your budget.")
        elif total > budget:
            print(f"You are over budget by ₹{total-budget}.")
    else:
        print('No suitable vendor combination found within your budget.')
        closest = closest_possible_set(filtered_vendors)
        if closest:
            total = sum(v['price'] for v in closest)
            print(f"Closest possible set costs: ₹{total}")
            for v in closest:
                print(f"- {v['service']}: {v['name']} (Price: ₹{v['price']}, Rating: {v['rating']})")
    print('\nSuggested Planning Steps:')
    for i, step in enumerate(suggest_planning_steps(event_type), 1):
        print(f"{i}. {step}") 