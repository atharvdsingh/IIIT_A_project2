# TreeFARMS CSV to TimberTrek Visualizer

This project allows you to upload a CSV file, train a TreeFARMS model, get decision paths in JSON format, and visualize them.

## Tech Stack

- Python + Flask (Backend)
- React (Frontend)
- Svelte + TimberTrek (via iframe)
- TreeFARMS (Machine Learning)
- TimberTrek (Visualization)

---
### Requirements

- Python 3.7 +
- Node.js 18+ (for React frontend)

## 🛠 Setup Instructions

### Step 1: Clone this Repository

```bash
git clone https://github.com/atharvdsingh/IIIT_All_project.git
cd IIIT_All_project

(1) now go to backend 
cd backend

(2) create and activate  new virtual environment
python3 -m venv tf-env
source tf-env/bin/activate 

(3) install required dependencies
pip install -r requirements.txt
(4) start the flask server 
python app.py
> The backend server will run at: http://localhost:5000


```
### step 2: Setup and run the Frontend

```bash 
cd frontend
npm install
npm run dev
> The frontend will be available at: [http://localhost:5173](http://localhost:5173)
>   If port 5173 is already in use, check your terminal — Vite will assign a new port automatically.
>   Open the URL shown in the console (e.g., http://localhost:5174, etc.).


> Upload the CSV file from frontend. The model will train and return a downloadable JSON.
> Scroll down to the embedded TimberTrek iframe.
> Upload the downloaded JSON file in TimberTrek using the upload button.
> Explore the decision paths visually!
