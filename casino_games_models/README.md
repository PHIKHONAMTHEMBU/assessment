Here's the complete README content, formatted with proper Markdown syntax. Just copy everything below this line and paste it directly into your `README.md` file.


# Casino Game Recommendation & Predictive Modelling

**Author:** Siyabonga Dlamini

This repository contains my submission for a data scientist technical assessment. I worked with a casino gaming dataset and used the following tools across different parts of the project:

1. **dbt** - for data transformation and modelling
2. **Streamlit** - for building the interactive dashboard
3. **Snowflake** - as the data warehouse, with data quality and governance implemented through the Medallion Architecture
4. **Google Colab** - for exploratory analysis and model development


## Setting Everything Up

### 1. Environment Setup

Clone the repository and install dependencies:

```bash
git clone https://github.com/PHIKHONAMTHEMBU/assessment.git
cd casino-analytics-assessment
python -m venv dbt-env
dbt-env\Scripts\activate
pip install -r requirements.txt
```

### 2. Snowflake Connection

You'll need to configure the dbt Snowflake connection:

1. Locate your `.dbt` profiles folder (on my Windows machine, it's at `C:\Users\phikh\.dbt\profiles.yml`)
2. Add the following configuration:

```yaml
casino_games_models:
  outputs:
    dev:
      type: snowflake
      account: [ACCOUNT]
      role: ACCOUNTADMIN
      user: [USER]
      password: [PASSWORD]
      database: CASINO_GAMES_DB
      warehouse: COMPUTE_WH
      schema: public
      threads: 1
      client_session_keep_alive: False

  target: dev
```

3. I'll share the credentials separately via email
4. Save the file and run `dbt debug` from the `casino_games_models` folder to test the connection
5. Once that's working, run `dbt run` to build the models

### 3. Running the Streamlit App

The Streamlit app consolidates all the assessment outputs so you can see the results without digging through code:

1. Activate your Python virtual environment
2. Navigate to the `casino_games_models` folder:
   ```bash
   cd casino_games_models
   ```
3. Launch the app:
   ```bash
   streamlit run app.py
   ```

> **Note:** The app runs locally and isn't deployed anywhere. I've used some caching to speed things up, so the first load might take a bit longer.

### 4. Data Modelling with Medallion Architecture

For the data modelling section, I structured the Snowflake warehouse using the Medallion Architecture. The database (`CASINO_GAMES_DB`) has separate schemas for each layer, and each dbt model materializes to its appropriate layer:

**RAW** - This is where the source data lands exactly as received. I only add job metadata here. Having this layer makes it much easier to trace data quality issues back to the source and reconcile what we received against what we processed.

**BRONZE** - This is the staging layer where I make minimal changes - documenting pipeline metadata, renaming columns for clarity, casting types properly, and removing duplicate records. Each bronze model maps one-to-one with a raw model.

**SILVER** - This is where the real cleaning happens. I convert monetary values to a base currency, flatten theme and mechanic data, apply all data quality checks, and run unit tests. This ensures the data is golden before it moves to the warehouse.

**GOLD** - Business-ready data at its lowest granularity. This is what downstream systems read from - EDA, similarity analysis, cohort analysis, the recommender engine, and the price prediction model all pull from here. This is the data that would typically get business sign-off.



## Assessment Breakdown

### Part 2 — Exploratory Data Analysis

The EDA is fully documented in the notebook with code and commentary.

- **Data Quality:** The dataset turned out to be surprisingly complete - no null values or duplicates to worry about.
- **Outliers and Skewness:** I found plenty of outliers and significant skewness. After investigating, I realized these likely come from high rollers who wager substantially more than average players. Rather than removing these outliers, I used logarithmic transformation to normalize the distributions for modelling. These high spenders are actually valuable customers, and cutting them out would lose important signal.
- **Feature Engineering:** I created per-capita metrics like wager per player and spins per player. This prevents the clustering engine from being biased toward casinos just because they have higher volumes.

### Part 3 — Game Similarity

This is accessible through the Streamlit app. To view it:

- Complete the environment setup
- Run `streamlit run app.py`
- Make sure port 8501 is open (or check which port it's using on your machine)
- The app opens at http://localhost:8501/ (might be 5000 depending on your setup)
- The landing page defaults to "Game Recommendations"
- Select a target casino, and the engine returns the top games with similarity scores

For instance, casino_103 returns 85 active games, with GAME_6012 having the highest accumulated similarity score (17189). Its top 3 similar games are GAME_5601, GAME_6013, and GAME_6275.

### Part 4 — Casino Cohorts

You'll find the full cohort analysis in the notebook.

### Part 5 — Recommendation System

The recommendation engine is also in the Streamlit app, bundled with the similarity functionality:

- I've included a table showing both game similarity and performance-based recommendations
- There's a slider that lets you control how many games you want recommended

### Part 6: Evaluating the Recommendation System

**Offline Evaluation:**

To test the recommender's quality, I'd use a 80/20 split approach. For each casino, I'd hide 20% of the games they play, generate recommendations from the remaining 80%, and check if the hidden games appear in the top recommendations. This tells me if the model is generalizing well or just memorizing patterns.

I have also actually configured the app to write logs and you are able to display and monitor the performance of the engine "live" on eh dashboard and you can from that point detect if the results are as expected or below threshold, of which you can use below measures to track and evaluate.

- **Metrics:** I'd look at **Precision** and **Recall** to measure relevance, plus **NDCG (Normalized Discounted Cumulative Gain)** **1** to evaluate ranking quality.

**Production Evaluation:**

Once the system is live, offline metrics aren't enough. I'd run A/B tests comparing the recommender against a baseline popularity model.

- **Metrics:** I'd track **Click-Through Rate (CTR)** , **Wager Conversion Rate**, and **NGR (Net Gaming Revenue)** lift from the recommended cohort.
- I referenced https://www.softswiss.com/knowledge-base/kpi-online-gaming/  **2** for these metrics.

**Risks**

- **Cold Starts:** New casinos with no history break the collaborative filtering approach. My mitigation strategy is to fall back to a "Global Top Performers" baseline or ask casinos to pick 3 "Seed Games" during onboarding.

### Part 9: Production & Operations

**Deployment & Serving:**

- **Real-time Serving:** I'd containerize the RandomForestRegressor and recommendation logic using Docker, deploy it on AWS EC2, and expose it via REST endpoints for sub-second predictions.
- **Batch Delivery:** Assuming game preferences don't change constantly, I'd use Airflow (or dbt) to run nightly batch jobs that pre-calculate recommendations and cache them in DynamoDB or a similar fast NoSQL database.

**Monitoring & Retraining:**

- **Monitoring:** The Streamlit app includes a "Live Prediction Logs" dashboard that calculates real-time Mean Absolute Error (MAE). I'd also implement data drift detection on feature vectors using something like Evidently AI.
- **Retraining:** I'd trigger retraining automatically when Live MAE degrades past a 15% error threshold, or on a monthly schedule to account for new game releases.

**Operational Risk:**

- **Data Pipeline Failures:** If dbt transformations fail upstream, the model would use stale data. I have implemented strict dbt unit tests and I would also add source freshness checks to prevent this. most importanly also, I would implement active pipeline alert on both success and failures, this will give me the confidence that all my processes are running as expected and all unit testing is being performed as they should,

### Part 10: Business Judgment & Data

**Identifying Emerging Casinos:**

From the available data, I'd look for casinos with high SPINS_PER_PLAYER (engagement) and rapid PLAYER_ID growth, even if their TOTAL_WAGER is modest.

- **Caveats:** High spins with low wagers could just mean bonus abuse or bot activity rather than genuine VIP growth. **3**

**Increasing Reach:**

Using the Casino Cohort analysis from Part 4, I'd identify which cluster an emerging casino belongs to. Then I'd look at the most successful mature casino in that same cluster and use the Recommendation Engine to suggest their top-performing games to the emerging casino.

**Additional Data Needed:**

The current dataset lacks some important behavioral context. Adding these would improve the models significantly:

1. **Player Demographics & Session Data:** Session length and playing times
2. **Financial Flow:** Deposit and withdrawal patterns to distinguish genuine VIPs from casual players


## References:
1. Normalized Discounted Cumulative Gain (NDCG) explained. (n.d.). [online] www.evidentlyai.com. Available at: https://www.evidentlyai.com/ranking-metrics/ndcg-metric [Accessed 28 July 2026].
2. Main Online Casino KPIs to Analyze and Improve GGR vs NGR ⋆ SOFTSWISS. (n.d.). [online] SOFTSWISS. Available at: https://www.softswiss.com/knowledge-base/kpi-online-gaming/ [Accessed 28 July 2026].
3. Jacek Białas (2026). Bonus hunter vs. VIP – How to distinguish them using AI. [online] iGaming Agency. Available at: https://igaming.createit.com/news/bonus-hunter-vs-vip-how-to-distinguish-them-using-ai/#device-and-connection-fingerprinting [Accessed 27 July 2026].
4. MLflow AI Platform. (2026). Why Log ML Training Metrics: A 2026 Practitioner Guide. [online] Available at: https://mlflow.org/articles/why-log-ml-training-metrics-a-2026-practitioner-guide/ [Accessed 27 July 2026].