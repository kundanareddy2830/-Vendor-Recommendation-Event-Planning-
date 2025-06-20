import streamlit as st
import pandas as pd
import json
from vendor_recommender import (
    load_vendor_data, filter_vendors_by_location, group_vendors_by_service,
    recommend_vendors, closest_possible_set, suggest_planning_steps
)

st.set_page_config(page_title="Vendor Recommender & Event Planner", layout="wide")
st.markdown("""
    <style>
    .vendor-card {
        background: #f8f9fa;
        border-radius: 16px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.10);
        padding: 1.2em 1em 1em 1em;
        margin-bottom: 1.5em;
        transition: box-shadow 0.2s;
        border: 1.5px solid #e0e0e0;
        min-height: 320px;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .vendor-card:hover {
        box-shadow: 0 8px 32px rgba(79,140,255,0.18);
        border: 2px solid #4f8cff;
        background: #f0f6ff;
    }
    .vendor-img {
        width: 120px;
        height: 120px;
        object-fit: cover;
        border-radius: 12px;
        margin-bottom: 0.7em;
        border: 1.5px solid #e0e0e0;
        background: #fff;
    }
    .service-title {
        font-size: 1.15em;
        font-weight: 700;
        color: #2d3a4a;
        margin-bottom: 0.7em;
        text-align: center;
    }
    .vendor-name {
        font-size: 1.08em;
        font-weight: 600;
        color: #1a237e;
        margin-bottom: 0.2em;
        text-align: center;
    }
    .vendor-details {
        font-size: 0.98em;
        color: #333;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎉 Vendor Recommender & Event Planning AI")
st.write("Plan your event with the best vendors, tailored to your city and budget!")

# --- Load Data ---
vendors = load_vendor_data()

# --- Get all unique locations and price ranges for dropdowns ---
all_locations = sorted({v['location'] for v in vendors})
price_options = [
    20000, 40000, 60000, 80000, 100000, 150000, 200000, 250000, 300000, 400000, 500000
]
def nearest_price(val, options):
    return min(options, key=lambda x: abs(x-val))
def_price = nearest_price(100000, price_options)

# --- Sidebar Inputs ---
def get_sidebar_state():
    if 'event_type' not in st.session_state:
        st.session_state['event_type'] = "Wedding"
    if 'location' not in st.session_state:
        st.session_state['location'] = all_locations[0]
    if 'budget' not in st.session_state:
        st.session_state['budget'] = def_price
    st.session_state['event_type'] = st.sidebar.selectbox("Event Type", ["Wedding", "Birthday", "Corporate"], index=["Wedding", "Birthday", "Corporate"].index(st.session_state['event_type']))
    st.session_state['location'] = st.sidebar.selectbox("Location", all_locations, index=all_locations.index(st.session_state['location']))
    st.session_state['budget'] = st.sidebar.selectbox("Budget (INR)", price_options, index=price_options.index(st.session_state['budget']))
get_sidebar_state()

event_type = st.session_state['event_type']
location = st.session_state['location']
budget = st.session_state['budget']

# --- Sample images for vendors (by service type) ---
SAMPLE_IMAGES = {
    "Venue": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=400&q=80",
    "Decoration": "https://images.unsplash.com/photo-1509228468518-180dd4864904?auto=format&fit=crop&w=400&q=80",
    "Catering": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=400&q=80",
    "Photography": "https://images.unsplash.com/photo-1465101046530-73398c7f28ca?auto=format&fit=crop&w=400&q=80",
    "Cake": "https://images.unsplash.com/photo-1505250469679-203ad9ced0cb?auto=format&fit=crop&w=400&q=80",
    "AV Equipment": "https://images.unsplash.com/photo-1515378791036-0648a3ef77b2?auto=format&fit=crop&w=400&q=80",
    "Other": "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=400&q=80"
}

def get_vendor_image(service):
    url = SAMPLE_IMAGES.get(service, SAMPLE_IMAGES["Other"])
    # fallback to a high-quality default if the url is empty or None
    if not url:
        url = "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=400&q=80"
    return url

# --- Main Button ---
if 'show_recommendations' not in st.session_state:
    st.session_state['show_recommendations'] = False
if st.button("Show Recommendations"):
    st.session_state['show_recommendations'] = True

if st.session_state['show_recommendations']:
    filtered_vendors = filter_vendors_by_location(vendors, location)
    services = group_vendors_by_service(filtered_vendors)

    # --- Show All Vendors by Service ---
    st.header("All Available Vendors by Service")
    if not services:
        st.warning("No vendors found for this location. Try another city or check your spelling.")
    else:
        cols = st.columns(min(4, len(services)))
        for idx, (service, vlist) in enumerate(services.items()):
            with cols[idx % len(cols)]:
                st.markdown(f'<div class="service-title">{service}</div>', unsafe_allow_html=True)
                for v in vlist:
                    img_url = get_vendor_image(service)
                    st.markdown(f'''
                        <div class="vendor-card">
                            <img class="vendor-img" src="{img_url}" alt="{service} image" />
                            <div class="vendor-name">{v['name']}</div>
                            <div class="vendor-details">
                                Price: ₹{v['price']}<br/>
                                Rating: {v['rating']}<br/>
                                Location: {v['location']}<br/>
                            </div>
                        </div>
                    ''', unsafe_allow_html=True)

    # --- Recommendation ---
    st.header("Recommended Vendors (Best Combo Under Budget)")
    recommended = recommend_vendors(filtered_vendors, budget)
    if recommended:
        total = sum(v['price'] for v in recommended)
        st.success(f"Total Estimated Cost: ₹{total}")
        if total < budget:
            st.info(f"You have ₹{budget-total} remaining in your budget.")
        elif total > budget:
            st.warning(f"You are over budget by ₹{total-budget}.")
        rec_df = pd.DataFrame(recommended)
        st.dataframe(rec_df)
    else:
        st.error("No suitable vendor combination found within your budget.")
        closest = closest_possible_set(filtered_vendors)
        if closest:
            total = sum(v['price'] for v in closest)
            st.info(f"Closest possible set costs: ₹{total}")
            close_df = pd.DataFrame(closest)
            st.dataframe(close_df)

    # --- Planning Steps ---
    st.header("Suggested Planning Steps")
    steps = suggest_planning_steps(event_type)
    # Add icons for each step
    step_icons = {
        'Book venue': '🏛️',
        'Book decoration': '🎀',
        'Book catering': '🍽️',
        'Book photographer': '📸',
        'Book cake': '🎂',
        'Book AV equipment': '🎤',
    }
    if 'booked_steps' not in st.session_state:
        st.session_state['booked_steps'] = set()
    if 'booked_vendors' not in st.session_state:
        st.session_state['booked_vendors'] = {}
    if 'booking_open' not in st.session_state:
        st.session_state['booking_open'] = None
    if 'last_booked' not in st.session_state:
        st.session_state['last_booked'] = None
    if 'show_confetti' not in st.session_state:
        st.session_state['show_confetti'] = False
    if 'selected_steps' not in st.session_state:
        st.session_state['selected_steps'] = steps
    st.session_state['selected_steps'] = st.multiselect(
        "Which steps do you want to book?",
        steps,
        default=st.session_state['selected_steps']
    )
    selected_steps = st.session_state['selected_steps']
    # Map step names to vendor services
    step_to_service = {
        'Book venue': 'Venue',
        'Book decoration': 'Decoration',
        'Book catering': 'Catering',
        'Book photographer': 'Photography',
        'Book cake': 'Cake',
        'Book AV equipment': 'AV Equipment'
    }
    for i, step in enumerate(steps, 1):
        icon = step_icons.get(step, '📝')
        booked = step in st.session_state['booked_steps']
        service = step_to_service.get(step)
        col1, col2 = st.columns([0.7, 0.3])
        with col1:
            if booked:
                st.markdown(f'<div style="background:#e6ffe6;padding:0.5em 1em;border-radius:8px;font-weight:600;">{icon} {i}. {step}</div>', unsafe_allow_html=True)
            else:
                st.write(f"{icon} {i}. {step}")
        with col2:
            if not booked:
                if st.button(f"Book", key=f"book_btn_{i}"):
                    st.session_state['booking_open'] = step
            if booked:
                vendor = st.session_state['booked_vendors'].get(step)
                if vendor:
                    st.success(f"Booked: {vendor}")
                else:
                    st.success(f"Booked!")
        # Booking UI (expander or section)
        if st.session_state['booking_open'] == step and not booked:
            with st.expander(f"Book {step}", expanded=True):
                if service and service in services:
                    vendor_names = [v['name'] for v in services[service]]
                    if f'vendor_select_{i}_{step}' not in st.session_state:
                        st.session_state[f'vendor_select_{i}_{step}'] = vendor_names[0]
                    selected_vendor = st.selectbox(
                        f"Select {service}",
                        vendor_names,
                        key=f'vendor_select_{i}_{step}'
                    )
                    if st.button(f"Confirm Booking", key=f"confirm_{i}"):
                        st.session_state['booked_steps'].add(step)
                        st.session_state['booked_vendors'][step] = selected_vendor
                        st.session_state['booking_open'] = None
                        st.session_state['last_booked'] = (step, selected_vendor)
                        st.session_state['show_confetti'] = True
                else:
                    if st.button(f"Confirm Booking", key=f"confirm_{i}"):
                        st.session_state['booked_steps'].add(step)
                        st.session_state['booking_open'] = None
                        st.session_state['last_booked'] = (step, None)
                        st.session_state['show_confetti'] = True
    # Show booking confirmation message after rerun
    if st.session_state.get('last_booked'):
        step, vendor = st.session_state['last_booked']
        if vendor:
            st.success(f"{step} - {vendor} booked!")
        else:
            st.success(f"{step} booked!")
        if st.session_state.get('show_confetti'):
            st.balloons()
            st.session_state['show_confetti'] = False
        st.session_state['last_booked'] = None
    # Booking history
    if st.session_state['booked_steps']:
        st.markdown("---")
        st.subheader("Booking History")
        for step in st.session_state['booked_steps']:
            vendor = st.session_state['booked_vendors'].get(step)
            icon = step_icons.get(step, '📝')
            if vendor:
                st.write(f"{icon} {step}: {vendor}")
            else:
                st.write(f"{icon} {step}: Booked")
else:
    st.info("Select your event type, location, and budget, then click 'Show Recommendations' to see results.")