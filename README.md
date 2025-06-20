# Vendor Recommender

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

## How It Works
1. **User Input**: The script prompts for event type, location, and budget.
2. **Vendor Filtering**: Only vendors in the selected location are considered.
3. **Recommendation Logic**: The script selects the best combination of top-rated vendors (one per service) whose total price fits within the budget. If no full set fits, it suggests the best possible subset.
4. **Planning Steps**: Based on the event type, the script suggests a basic order for booking services (e.g., venue, decoration, catering, photography).

## How to Run the Script
1. Make sure you have Python 3 installed.
2. Place `vendor_recommender.py` and `mock_data.json` in the same directory.
3. Open a terminal and navigate to the project directory.
4. Run the script:
   ```bash
   python vendor_recommender.py
   ```
5. Follow the prompts to enter event details.

---

Feel free to modify `mock_data.json` to add more vendors or services! 
