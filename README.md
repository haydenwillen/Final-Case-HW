# College Football Offense Dashboard (Flask + Docker)

## 1) Executive Summary
**Problem:** College Football is one of the fastest-moving sports in today's world. We can only attempt to measure all actions on the field using descriptive statistics. However, there are simply too many metrics nowadays, and finding relevant ones has become increasingly difficult. Is there a way to simplify these statistics so that a casual fan can follow statistics without getting lost?

**Solution:** A lightweight, easy-to-navigate Flask API that serves four correlation plots and a stats summary for a 2023 college football dataset. Everything is containerized for a one-command run. Graphs are easy to read and display vital information, including the correlation between selected statistics and the Points-Per-Game statistic. This helps casual college football fans easily view plots that summarize scoring trends. 

## 2) System Overview
- **Course Concept(s):**
  - A working Flask API serving both matplotlib plots and HTML/JSON responses.  
  - Data wrangling with pandas/numpy, visualization with matplotlib.  
  - Containerization with Docker for reproducible runs.  
  - Configuration via environment variables instead of hard-coded paths/ports.  
- **Data/Models/Services:**  
  - **Dataset:** `cfb23.csv` (2023 college football offensive stats), credited to **Jeff Gallini**, accessed via Kaggle.  
  - **Stat transforms:** Numeric coercion, NaN drops, linear regression (`np.polyfit`) for best-fit lines, Pearson correlation (`np.corrcoef`).  
  - **Views:** Scatter plots with regression line + r value; stats endpoint returns both HTML summary and JSON payload.  
- **Architecture:**  
  1) Client requests a route (plot or stats).  
  2) Flask reads the CSV from `DATA_PATH`, coerces numeric fields per endpoint.  
  3) Matplotlib renders a figure to PNG in-memory; stats endpoint renders a Jinja template or JSON.  
  4) Response is sent with cache-busting headers to avoid stale images.  
  5) Docker image bakes code + dataset; `MPLCONFIGDIR` set to a writable temp dir.  
  
**Flow Chart**
  <img width="1234" height="691" alt="Screenshot 2025-12-01 at 1 27 11 PM" src="https://github.com/user-attachments/assets/b62d547d-778f-4cc0-8a1c-43fe175c0e5c" />


## 3) How to Run (Local via Docker)
```bash
# from Final-Project/
./run.sh
# or manually
docker build -t final-project:latest .
docker run --rm -p 5000:5000 --env-file .env.example final-project:latest
```
Health check: `curl http://localhost:5000/health`

Key endpoints:  
- `/` home with cards to plots and stats  
- `/api/ppg-vs-pass-tds`  
- `/api/ppg-vs-rush-tds`  
- `/api/ppg-vs-total-yds`  
- `/api/ppg-vs-turnovers`  
- `/api/stats?format=html|json`

## 4) Design Decisions
- **Why Flask + PNGs?**
  - Flask provides a lightweight, minimal-complexity framework for building web applications, making it easy to stand up an API or dashboard quickly without unnecessary overhead. Its simplicity lets me focus on core functionality rather than navigating a complex front-end stack. Additionally, using Flask keeps my project’s dependencies streamlined by limiting them primarily to essential data-science libraries like Pandas, NumPy, and Matplotlib, which results in faster setup, easier maintenance, and a cleaner deployment footprint.  
- **Why linear fit & r?**
  - Using linear fit and r provides a simple, explainable signal for correlation that renders quickly. These plots are easy to navigate and understand for the average viewer, even for someone unfamiliar with college football and its inner workings. The plots include all available teams and show the correlation between each statistic and the performance metric (“Points-Per-Game”). Using a linear fit and correlation coefficient also provides a consistent metric across all comparisons, making it straightforward to evaluate which variables have the strongest relationship to scoring performance.
- **Env config:**
  - Using environment variables like DATA_PATH, FLASK_RUN_PORT, and MPLCONFIGDIR helps keep your paths and ports flexible, whether you're running the app locally or inside Docker. This way, you don’t have to hard-code anything or constantly tweak the project when switching environments. It also keeps the setup cleaner and more portable, making it easier for anyone else to run the project without digging through your code to make changes.  
- **Caching:**
  - By adding explicit no-store headers, we make sure the browser doesn’t hang onto old versions of the plots. This prevents you from accidentally viewing outdated graphics while you’re iterating and testing, ensuring every refresh shows the most recent version.  
- **Security/Privacy:**
  - The app only uses a read-only public dataset, with no file uploads or user-generated content, which keeps things simple and safe. There are no sensitive keys or secrets stored in the repo, and a .env.example file clearly lists the variables needed to run the project without exposing any private information.  
- **Ops & DX:**
  - A simple health endpoint makes it easy to confirm the app is up and running, and a run.sh script lets you build and launch everything with a single command. Lightweight pytest smoke tests help ensure the key endpoints work as expected, and Docker provides a consistent, reproducible environment so the project behaves the same wherever it’s deployed.  
- **Tradeoffs:**
  - The app uses static plots and sticks to straightforward linear correlations, which keeps things simple but limits the depth of the analysis. It also reloads the CSV file on every request—perfectly fine for a small dataset, but something that could be optimized later by caching or keeping the data in memory if performance ever becomes an issue.

## 5) Results & Evaluation
The four offensive plots load in well under a second on a typical laptop, each showing a clean scatterplot with a best-fit line and the Pearson r value clearly labeled so you can spot trends right away. The `/api/stats` endpoint provides both a short, readable HTML summary and a JSON payload, which makes it easy to double-check the data yourself or plug it into another tool. Basic smoke tests using pytest validate the health endpoint and one of the plot routes with a small fixture CSV, giving you confidence that the app can start up, read data correctly, and return a proper PNG. Overall, the app stays lightweight: even with the CSV loading on each request and Matplotlib running headless, it uses minimal resources and still delivers consistent, reliable outputs—perfect for quick exploratory work or simple demos.

## 6) What’s Next
Looking ahead, the project could grow in a few meaningful ways. Additional endpoints—such as defensive metrics or overall efficiency stats—would round out the analysis and give users a fuller picture of team performance across both sides of the ball. A major upgrade would be moving from static images to interactive charts using libraries like Plotly or Altair; this would allow viewers to hover for exact values, zoom into dense clusters, toggle variables, and generally explore the data in a more intuitive, hands-on way. On the engineering side, adding continuous integration to automatically run pytest on every push would help catch issues early and keep the codebase stable as new features are introduced. Finally, incorporating basic observability—such as request logging, endpoint timing, or lightweight metrics—would make it easier to monitor performance and understand how the app behaves under different loads. 

## 7) Links
- **GitHub Repo:** (https://github.com/haydenwillen/Final-Case-HW)  
- **License:** MIT (see LICENSE)  
- **Dataset Credit:** Jeff Gallini (https://www.kaggle.com/datasets/jeffgallini/college-football-team-stats-2019?resource=download&select=cfb23.csv)

## 8) Development & Testing
```bash
# install deps
pip install -r requirements.txt
# run app locally (non-Docker)
export DATA_PATH=cfb23.csv
python app.py
# tests
pytest
```

## 9) Repo Layout
```
Final-Project/
├─ assets/
|  └─ architecture.png     # Architecture Flow Chart
│  └─ cfb23.csv            # 2023 CFB dataset (credit: Jeff Gallini, via Kaggle)
├─ src/
│  └─ app.py               # Flask application and routes
├─ tests/
│  └─ test_app.py          # pytest smoke tests
├─ .env.example            # sample environment variables
├─ Dockerfile              # container definition for reproducible runs
├─ LICENSE                 # MIT license for the project
├─ README.md               # Project documentation
├─ requirements.txt        # Python dependencies list 
└─ run.sh                  # one-command build/run script

```
