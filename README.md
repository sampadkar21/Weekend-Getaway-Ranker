# Weekend Getaway Recommender System

## Overview
This project implements a **weekend travel destination recommender** that suggests nearby tourist destinations based on a user’s **source city**.

The system prioritizes:
- Short travel distance (weekend feasibility)
- High Google review ratings (destination quality)
- Interpretable, deterministic ranking logic

The solution is implemented using **Python and Pandas**, supported by an exploratory notebook and a production-ready script.

---

## Tech Stack
- Python
- Pandas
- NumPy

---

## Project Structure

```

.
├── outputs/
│   └── (generated recommendations)
├── README.md
├── final_data_with_coords.csv
├── recommender.py
├── requirements.txt
└── weekend-getaway-ranker.ipynb

````

---

## Dataset Description
The dataset (`final_data_with_coords.csv`) contains curated information about Indian tourist destinations.

### Key Columns
- `City` – Source city name  
- `Name` – Destination name  
- `Type` – Destination category (e.g., hill station, beach, heritage)  
- `Latitude`, `Longitude` – Geographical coordinates  
- `Google review rating` – Average user rating  

---

## Mathematical Formulation

### 1. Distance Calculation (Haversine Formula)

To compute the geographical distance between a **source city** and a **destination**, the Haversine formula is used.  
It calculates the great-circle distance between two points on the Earth using latitude and longitude.

\begin{aligned}
\Delta \phi &= \phi_2 - \phi_1 \\
\Delta \lambda &= \lambda_2 - \lambda_1 \\
a &= \sin^2\left(\frac{\Delta \phi}{2}\right)
    + \cos(\phi_1)\cos(\phi_2)\sin^2\left(\frac{\Delta \lambda}{2}\right) \\
c &= 2 \cdot \tan^{-1}\left(\frac{\sqrt{a}}{\sqrt{1-a}}\right) \\
d &= R \cdot c
\end{aligned}

Where:
- \(\phi_1, \phi_2\) are latitudes (in radians)
- \(\lambda_1, \lambda_2\) are longitudes (in radians)
- \(R = 6371\) km (Earth’s radius)
- \(d\) is the distance in kilometers

Only destinations within **250 km** are considered for recommendations.

---

### 2. Bayesian Popularity Score (Optional Extension)

Raw ratings alone can be misleading when review counts differ significantly.  
A **Bayesian weighted popularity score** stabilizes destination rankings.

\text{Popularity} =
\frac{v}{v + m} \cdot R
+
\frac{m}{v + m} \cdot C

Where:
- \(R\) = destination’s average Google review rating  
- \(v\) = number of reviews  
- \(C\) = mean rating across all destinations  
- \(m\) = median number of reviews (confidence threshold)

This prevents destinations with very few reviews from being over-ranked.

---

### 3. Final Destination Ranking Score

Each destination is assigned a final ranking score balancing **quality** and **travel convenience**.

\[
\text{Final Rank} =
0.7 \times \text{Rating}
+
0.3 \times \frac{1}{\text{Distance}_{km} + 1}
\]

Where:
- `Rating` is the Google review rating
- `Distanceₖₘ` is the Haversine distance from the source city
- The constant \(+1\) avoids division by zero

---

## Algorithm Summary
1. Load destination dataset  
2. Validate source city  
3. Compute distances using Haversine formula  
4. Filter destinations within 250 km  
5. Compute final ranking score  
6. Sort and return top-k recommendations  

---

## How to Run

### Install Dependencies
```bash
pip install -r requirements.txt
````

### Run the Recommender

```bash
python recommender.py
```

### Usage

The script runs in interactive mode:

```
Enter your current city (or 'q' to quit):
```

The top weekend destinations are printed to the console.

---

## Sample Output

![img1](outputs/out_1.png)

![img2](outputs/out_2.png)

![img3](outputs/out_3.png)

---

## Notebook

`weekend-getaway-ranker.ipynb` contains:

* Data exploration
* Distance analysis
* Feature reasoning
* Ranking experiments

The final logic is distilled into `recommender.py`.

---

## Why This Approach Works

* Simple and interpretable scoring
* No black-box models
* Easy to justify mathematically
* Suitable for small to medium datasets
