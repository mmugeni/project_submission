#Description

**Welcome Uganda** is a comprehensive Python-based command-line application designed to help travelers explore, plan, and organize trips across Uganda’s diverse regions and attractions.  
It features detailed information on attractions, route planning, reviews, favorites, and integrates with Google Maps for navigation.

---

## Features

- Browse and search attractions by region, category, or keyword
- View detailed attraction information including images, opening hours, fees, and popularity
- Add and view user reviews for attractions
- Manage a list of favorite attractions
- Plan routes and get estimated travel times and distances between locations
- Open images and Google Maps directions directly from the app
- Data persistence using JSON files for attractions, reviews, favorites, and routes

---

## Data Structure

- `data/attractions.json` — Stores information on tourist attractions
- `data/reviews.json` — Stores user reviews keyed by attraction IDs
- `data/favorites.json` — Stores user favorites
- `data/routes.json` — Stores travel route info and distances

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/uganda-trip-planner.git
   cd uganda-trip-planner
(Optional) Create a virtual environment and activate it:

bash
Copy code
python3 -m venv env
source env/bin/activate   # On Windows use `env\Scripts\activate`
Install required dependencies (if any).
Note: The project uses standard Python libraries and does not require external packages.

Usage
Run the main script:

bash
Copy code
python main.py
Follow the interactive menu prompts to:

View attractions by region or category

Search for attractions

Plan routes and get directions

Manage and view reviews and favorites

Project Structure
pgsql
Copy code
uganda-trip-planner/
│
├── data/
│   ├── attractions.json
│   ├── reviews.json
│   ├── favorites.json
│   └── routes.json
│
├── images/
│   └── [attraction images]
│
├── main.py
├── README.md
└── LICENSE

