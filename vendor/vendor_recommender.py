import json
from itertools import combinations

# Step 1: Get user input
def get_user_input():
    event_type = input('Enter event type (e.g., Wedding, Birthday, Corporate): ')
    location = input('Enter location (e.g., Hyderabad, Bangalore): ')
    budget = int(input('Enter your budget (e.g., 100000): '))
    return event_type, location, budget

# Step 2: Load mock vendor data
def load_vendor_data(filename='mock_data.json'):
    with open(filename, 'r') as f:
        return json.load(f)

# Step 3: Filter vendors by location
def filter_vendors_by_location(vendors, location):
    return [v for v in vendors if v['location'].lower() == location.lower()]

# Step 4: Select top-rated vendors under budget
def recommend_vendors(vendors, budget):
    # Group vendors by service
    services = {}
    for v in vendors:
        services.setdefault(v['service'], []).append(v)
    # For each service, sort vendors by rating (desc), then price (asc)
    for service in services:
        services[service].sort(key=lambda x: (-x['rating'], x['price']))
    # Try all combinations: pick top vendor from each service, check if total price <= budget
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
    # If no combo fits, try picking fewer services
    if not best_combo:
        all_vendors = [v for sublist in service_lists for v in sublist]
        for r in range(len(service_lists), 0, -1):
            for combo in combinations(all_vendors, r):
                # Only one vendor per service
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

# Step 5: Suggest planning steps
def suggest_planning_steps(event_type):
    steps = {
        'wedding': ['Book venue', 'Book decoration', 'Book catering', 'Book photographer'],
        'birthday': ['Book venue', 'Book decoration', 'Book cake', 'Book photographer'],
        'corporate': ['Book venue', 'Book catering', 'Book AV equipment', 'Book decoration']
    }
    return steps.get(event_type.lower(), ['Book venue', 'Book vendors'])

if __name__ == '__main__':
    event_type, location, budget = get_user_input()
    vendors = load_vendor_data()
    filtered_vendors = filter_vendors_by_location(vendors, location)
    recommended = recommend_vendors(filtered_vendors, budget)
    print('\nRecommended Vendors:')
    if recommended:
        for v in recommended:
            print(f"- {v['service']}: {v['name']} (Price: ₹{v['price']}, Rating: {v['rating']})")
        total = sum(v['price'] for v in recommended)
        print(f"Total Estimated Cost: ₹{total}")
    else:
        print('No suitable vendor combination found within your budget.')
    print('\nSuggested Planning Steps:')
    for i, step in enumerate(suggest_planning_steps(event_type), 1):
        print(f"{i}. {step}") 