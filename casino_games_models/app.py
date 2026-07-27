import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime

st.set_page_config(page_title="Siya Dlamini - Casino Analytics Hub", layout="wide")

LOG_FILE = "app_data/prediction_logs.csv"
TRAINING_LOG_FILE = "app_data/training_logs.csv"

LOG_COLUMNS = [
    "Timestamp", "Casino_ID", "Game_ID", "Cohort",
    "Predicted_Players", "Actual_Players", "Absolute_Error",
    "APE_%", "Residual", "Tree_Uncertainty_Std"
]


def load_logs():
    if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > 0:
        try:
            return pd.read_csv(LOG_FILE)
        except pd.errors.EmptyDataError:
            pass
    return pd.DataFrame(columns=LOG_COLUMNS)


def save_log(casino, game, cohort, prediction, uncertainty, clean_df):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    df = load_logs()

    # look up ground truth in the historical data, if this combo exists
    sub = clean_df[(clean_df['CASINO_ID'] == casino) & (clean_df['GAME_ID'] == game)]
    actual = int(sub['PLAYER_ID'].nunique()) if not sub.empty else None

    abs_error = abs(actual - prediction) if actual is not None else None
    ape = (abs_error / actual * 100) if (actual is not None and actual > 0) else None
    residual = (actual - prediction) if actual is not None else None

    new_entry = pd.DataFrame([{
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Casino_ID": casino,
        "Game_ID": game,
        "Cohort": cohort,
        "Predicted_Players": round(prediction, 2),
        "Actual_Players": actual if actual is not None else "Unobserved",
        "Absolute_Error": round(abs_error, 2) if abs_error is not None else None,
        "APE_%": round(ape, 2) if ape is not None else None,
        "Residual": round(residual, 2) if residual is not None else None,
        "Tree_Uncertainty_Std": round(uncertainty, 2)
    }])

    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(LOG_FILE, index=False)


def load_training_logs():
    if not os.path.exists(TRAINING_LOG_FILE):
        return None
    df = pd.read_csv(TRAINING_LOG_FILE)
    # strip mlflow's metrics./params./tags. prefixes
    df.columns = [col.replace('metrics.', '').replace('params.', '').replace('tags.', '') for col in df.columns]
    return df


@st.cache_resource
def load_recommendation_data():
    clean_data = pd.read_parquet('app_data/clean_df.parquet')
    sim_data = pd.read_parquet('app_data/similarity_df.parquet')
    return clean_data, sim_data


@st.cache_resource
def load_predictor_data():
    cohorts = pd.read_parquet('app_data/casino_cohorts.parquet')
    profiles = pd.read_parquet('app_data/game_profiles.parquet')
    clean_data = pd.read_parquet('app_data/clean_df.parquet')
    return cohorts, profiles, clean_data


@st.cache_resource
def load_models():
    model = joblib.load('app_data/player_predictor_model.joblib')
    features = joblib.load('app_data/model_features.joblib')
    return model, features


st.sidebar.title("Analytics Hub")
app_mode = st.sidebar.radio("Select a Tool:", [
    "Game Recommendations",
    "Player Predictor",
    "Live Prediction Logs",
    "Model Training Logs"
])

if app_mode == "Game Recommendations":
    st.title("Game Recommendation Engine")
    st.markdown("Finds the best new games for a casino based on historical behavioral profiles.")

    try:
        clean_df, similarity_df = load_recommendation_data()
    except FileNotFoundError:
        st.error("Missing required .parquet files in app_data/. Make sure the notebook export finished.")
        st.stop()

    casino_list = sorted(clean_df['CASINO_ID'].dropna().unique().tolist())
    selected_casino = st.sidebar.selectbox("Select Target Casino:", casino_list)
    top_n_selection = st.sidebar.slider("Number of Recommendations:", min_value=1, max_value=10, value=5)

    if selected_casino:
        st.subheader(f"Results for {selected_casino}")

        casino_data = clean_df[clean_df['CASINO_ID'] == selected_casino]
        live_games = casino_data['GAME_ID'].unique().tolist()

        top_historical_games = (
            casino_data.groupby('GAME_ID')['TOTAL_WAGER_RATED']
            .sum()
            .sort_values(ascending=False)
            .head(3)
            .index.tolist()
        )

        recommendations = {}
        for game in top_historical_games:
            if game not in similarity_df.index:
                continue
            for candidate_game, score in similarity_df.loc[game].items():
                if candidate_game in live_games or candidate_game == game:
                    continue
                recommendations[candidate_game] = recommendations.get(candidate_game, 0) + score

        sorted_recs = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)

        if not sorted_recs:
            st.warning("Not enough historical data to generate recommendations.")
        else:
            rec_df = pd.DataFrame(sorted_recs[:top_n_selection], columns=['Recommended_GAME_ID', 'Relevance_Score'])
            rec_df['Reason'] = f"Similar to top performers: {', '.join(top_historical_games)}"

            col1, col2 = st.columns(2)
            col1.metric("Games Already Live", len(live_games))
            col2.metric("Top Performers Analyzed", len(top_historical_games))

            st.dataframe(
                rec_df,
                hide_index=True,
                use_container_width=True,
                column_config={"Relevance_Score": st.column_config.NumberColumn(format="%.4f")}
            )

elif app_mode == "Player Predictor":
    st.title("Target Player Predictor")
    st.markdown("Forecasts how many unique players a game will attract at a given casino.")

    try:
        casino_cohorts, game_profiles, clean_df = load_predictor_data()
        rf_model, model_features = load_models()
    except FileNotFoundError:
        st.error("Missing required .parquet or .joblib files in app_data/.")
        st.stop()

    col_c, col_g = st.columns(2)
    with col_c:
        pred_casino = st.selectbox("Select Target Casino:", sorted(casino_cohorts['CASINO_ID'].unique()))
    with col_g:
        pred_game = st.selectbox("Select Game to Evaluate:", sorted(game_profiles.index))

    if st.button("Predict Player Count", type="primary"):
        cohort_val = casino_cohorts.loc[casino_cohorts['CASINO_ID'] == pred_casino, 'COHORT'].values[0]
        game_vector = game_profiles.loc[pred_game].to_dict()

        feature_dict = {'COHORT': cohort_val, **game_vector}
        input_df = pd.DataFrame([feature_dict]).reindex(columns=model_features, fill_value=0)

        prediction = rf_model.predict(input_df)[0]

        # spread of the individual tree predictions gives a rough uncertainty estimate
        tree_predictions = [tree.predict(input_df)[0] for tree in rf_model.estimators_]
        uncertainty_std = np.std(tree_predictions)

        save_log(pred_casino, pred_game, cohort_val, prediction, uncertainty_std, clean_df)

        st.success("Prediction generated and logged.")

        col_res1, col_res2 = st.columns(2)
        col_res1.metric(
            label=f"Expected Active Players ({pred_game} @ {pred_casino})",
            value=f"{int(prediction)} Players"
        )
        col_res2.metric(
            label="Uncertainty (Tree Std Dev)",
            value=f"± {uncertainty_std:.2f} Players",
            help="Lower values mean the trees agree more on this prediction."
        )

elif app_mode == "Live Prediction Logs":
    st.title("📊 Model Inference Diagnostics")
    st.markdown("Live error metrics and variance tracking, useful for deciding when to retrain.")

    log_df = load_logs()

    if log_df.empty:
        st.info("No predictions logged yet - head to the Player Predictor to generate some.")
    else:
        # only rows with a known ground truth can be evaluated
        eval_df = log_df[log_df['Actual_Players'] != "Unobserved"].copy()

        if not eval_df.empty:
            for col in ['Absolute_Error', 'APE_%', 'Predicted_Players', 'Actual_Players']:
                eval_df[col] = pd.to_numeric(eval_df[col])

            st.subheader("Live Model Performance")
            kpi1, kpi2, kpi3, kpi4 = st.columns(4)

            live_mae = eval_df['Absolute_Error'].mean()
            live_rmse = np.sqrt((eval_df['Absolute_Error'] ** 2).mean())
            mean_mape = eval_df['APE_%'].mean()
            avg_uncertainty = pd.to_numeric(log_df['Tree_Uncertainty_Std']).mean()

            kpi1.metric("Live MAE", f"{live_mae:.2f} Players")
            kpi2.metric("Live RMSE", f"{live_rmse:.2f} Players")
            kpi3.metric("Mean APE (Error %)", f"{mean_mape:.1f}%")
            kpi4.metric("Avg Tree Uncertainty", f"± {avg_uncertainty:.2f}")

            st.markdown("### Actual vs. Predicted")
            chart_data = eval_df[['Timestamp', 'Predicted_Players', 'Actual_Players']].set_index('Timestamp')
            st.line_chart(chart_data)
        else:
            st.warning("Logs recorded, but none of them have ground-truth observations to evaluate against yet.")

        st.markdown("### Inference Ledger")
        st.dataframe(
            log_df.sort_values(by="Timestamp", ascending=False),
            hide_index=True,
            use_container_width=True,
            column_config={
                "APE_%": st.column_config.NumberColumn(format="%.2f%%"),
                "Tree_Uncertainty_Std": st.column_config.NumberColumn(format="± %.2f")
            }
        )

elif app_mode == "Model Training Logs":
    st.title("Model Training History")
    st.markdown("Metrics and hyperparameters logged by MLflow during training.")

    training_df = load_training_logs()

    if training_df is None or training_df.empty:
        st.warning(f"No training logs found at `{TRAINING_LOG_FILE}` - export the MLflow data from the notebook first.")
    else:
        # newest run is row 0
        latest_run = training_df.iloc[0]

        st.subheader("Latest Production Model Metrics")
        col1, col2, col3 = st.columns(3)

        r2_score = latest_run.get('training_r2_score', 'N/A')
        mae_score = latest_run.get('training_mean_absolute_error', 'N/A')
        n_trees = latest_run.get('n_estimators', 'N/A')

        if isinstance(r2_score, (int, float)):
            r2_score = f"{r2_score:.4f}"
        if isinstance(mae_score, (int, float)):
            mae_score = f"{mae_score:.2f}"

        col1.metric("R-Squared (Accuracy)", r2_score)
        col2.metric("Mean Absolute Error", mae_score)
        col3.metric("Estimators (Trees)", n_trees)

        st.markdown("### Full MLflow Training Ledger")
        cols_to_display = ['start_time', 'run_id', 'training_r2_score', 'training_mean_absolute_error', 'n_estimators', 'max_depth']
        available_cols = [c for c in cols_to_display if c in training_df.columns]

        st.dataframe(training_df[available_cols], hide_index=True, use_container_width=True)