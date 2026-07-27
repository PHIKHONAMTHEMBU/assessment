# Casino Game Recommendation & Predictive Modelling

**Author:** Siyabonga Dlamini

This repo is in response to a technical assessment for a data scientist role, using a casino dataset. The tech stack used across the assessment questions:

1. **dbt**
2. **Streamlit**
3. **Snowflake** 
    - data quality and data governance implementation using the Medallion Architecture
4. **Google Colab**
    - EDA
    - Model training and evaluation

## How to Set Up and Run

### 1. Environment Setup

Clone this repository and install the required dependencies:

```bash
git clone https://github.com/PHIKHONAMTHEMBU/assessment.git
cd casino-analytics-assessment
python -m venv dbt-env
dbt-env\Scripts\activate
pip install -r requirements.txt
```

### 2. Snowflake Connection

The dbt Snowflake connection needs to be configured:

1. Navigate to the hidden `.dbt` profiles folder on your local machine.
   - On my machine the path is: `C:\Users\phikh\.dbt\profiles.yml`
2. Edit the file by copying and pasting the below:

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

3. Secrets will be shared via email.
4. Save your profile changes.
5. Run `dbt debug` (make sure you are inside the `casino_games_models` folder).
6. Run `dbt run` (same folder).

### 3. Launching the Streamlit App

Streamlit is used to demonstrate all the required outputs of the assessment, making it easy for the assessor to see actual results without having to go through or rerun the code.

1. Activate the Python environment (`dbt-env`, or whatever you named yours).
2. Make sure you are in the `casino_games_models` folder:
   ```bash
   cd casino_games_models
   ```
3. Launch the app:
   ```bash
   streamlit run app.py
   ```

> **Note:** The app is not yet deployed. Resource caching is used to improve performance, so the first run may be slow while everything loads.

### 4 Data Modelling Approach: Medallion Architecture
For Part 1 (data modelling with dbt), the warehouse is structured in Snowflake using the Medallion Architecture. The database (`CASINO_GAMES_DB`) is split into layered schemas, and each dbt model is materialised into the layer that matches its level of refinement:

**RAW** - this is where the three raw source extracts land, in this section, no data is changed, we only add the job metadata. Also very useful for tracking and tracing data quality issues and balancing data tht was received vs data that we processed to the data warehouse.

**BRONZE** - this is basically staging the raw data, again here only very little changes are allowed at this level, we document pipeline metadata, and also we change column names, casting types and removing duplicate records. there is a one to one mapping that needs to be maintained between bronze models and raw models.

**SILVER** - the cleaning layer. this is where we perform heavy duty transformations, such as monetary values that we convertered to base currency, themes and mechanics can also be flatted at this level and also applying all the data quality checks and unit testing. this will ensure that data for pushing into the data warehouse and also required for model testing is golden.

**GOLD** - this is business-ready data, that can be trusted and is at it lowested grain required for reporting (casino by game aggregates by net win and by total number of players). basically everything downstream (EDA, similairty, cohorts, recommender engine and price prediction model) reads only on gold. this is data that is generally sign-off by business.

## Responding to Assessment Questions
