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

## Responding to Assessment Questions
