# Vendor Recommender & event planning

## Project Description
A simple AI-like system that recommends event vendors and provides planning steps based on user input such as event type, location, and budget. This tool helps users efficiently plan events by suggesting the best vendor combinations within their budget.

## Problem Statement
Event planning can be overwhelming, especially when choosing the right vendors within a budget. This project aims to simplify the process by recommending top-rated vendors for each service and outlining a basic event planning workflow.

## Inputs
- **event_type**: Type of event (e.g., Wedding, Birthday, Corporate)
- **location**: Event location (e.g., Hyderabad, Bangalore)
- **budget**: Total budget in INR (e.g., 100000)

## Outputs
- List of recommended vendors (one per service) within the budget
- Total estimated cost
- Suggested planning steps for the event type

## Mock Data
Vendor data is stored in `mock_data.json` and includes:
- Vendor Name
- Service Type (e.g., Decoration, Photography, Catering, Venue)
- Price (in INR)
- Rating (out of 5)
- Location

## Features
- **Streamlit Web App**: Clean, modern UI with cards, images, and hover effects.
- **City & Budget Selection**: Choose from real cities and price ranges.
- **All Vendors by Service**: See all available vendors for each service in your city.
- **Smart Recommendations**: Get the best vendor combination under your budget, or the closest possible set if over budget.
- **Interactive Planning Steps**: Book only the steps you want (venue, decoration, catering, etc.), with icons and booking history.
- **Vendor Selection**: For each bookable step, pick your preferred vendor from a dropdown.
- **Confetti Animation**: Celebrate every booking with confetti!
- **Booking History**: See all your booked steps and vendors in one place.
- **Robust State Handling**: All selections and bookings persist during your session.

---

## Setup & Usage

1. **Clone the repository**
   ```bash
   git clone https://github.com/kundanareddy2830/-Vendor-Recommendation-Event-Planning-.git
   cd -Vendor-Recommendation-Event-Planning-
   ```

2. **Install dependencies**
   ```bash
   pip install streamlit pandas
   ```

3. **Run the Streamlit app**
   ```bash
   python -m streamlit run vendor/streamlit_app.py
   ```

4. **Open the app**
   - Visit the local URL shown in your terminal (usually http://localhost:8501)

---

## How It Works
1. **Select Event Details**: Use the sidebar to pick event type, city, and budget.
2. **Show Recommendations**: Click the "Show Recommendations" button.
3. **Browse Vendors**: See all available vendors by service, with images.
4. **Book Planning Steps**:
   - Choose which steps you want to book (e.g., venue, catering).
   - For each, click "Book", select a vendor (if applicable), and confirm.
   - Enjoy confetti and see your booking history update live!

---

## Data
- Vendor data is in `vendor/mock_data.json`.
- You can add more vendors, cities, or services by editing this file.

---

## License
This project is for educational and demonstration purposes. 
