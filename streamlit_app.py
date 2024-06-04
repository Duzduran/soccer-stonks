import streamlit as st
import pandas as pd
import pickle
from kedro.framework.session import KedroSession
from kedro.framework.startup import bootstrap_project
from pathlib import Path

project_path = Path(__file__).resolve().parent
bootstrap_project(project_path)

with KedroSession.create("", project_path, env="local", extra_params=None) as session:
    context = session.load_context()

    inverse_mapping = context.catalog.load('category_mapping')

    model = context.catalog.load('model')

    st.title("Soccer Player Value Prediction")

    st.markdown("""
    This app predicts the market value of a soccer player based on their attributes.
    Please provide the following details to get the prediction.
    """)

    age = st.number_input('Age', min_value=15, max_value=50, value=25, help="Enter the age of the player")
    overall_rating = st.number_input('Overall Rating', min_value=1, max_value=100, value=50, help="Enter the overall rating of the player")
    potential = st.number_input('Potential', min_value=1, max_value=100, value=50, help="Enter the potential rating of the player")
    height = st.number_input('Height (cm)', min_value=100, max_value=250, value=180, help="Enter the height of the player in cm")
    weight = st.number_input('Weight (kg)', min_value=30, max_value=150, value=70, help="Enter the weight of the player in kg")
    foot = st.selectbox('Preferred Foot', options=["Right", "Left"], help="Select the preferred foot of the player")
    best_position = st.selectbox('Best Position', options=list(inverse_mapping.keys()), help="Enter the best position of the player")
    growth = st.number_input('Growth', min_value=0, max_value=100, value=50, help="Enter the growth of the player")
    wage = st.number_input('Wage (€)', min_value=0, value=10000, help="Enter the wage of the player in €")
    release_clause = st.number_input('Release Clause (€)', min_value=0, value=5000000, help="Enter the release clause of the player in €")
    jumping = st.number_input('Jumping', min_value=0, max_value=100, value=50, help="Enter the jumping ability of the player")
    strength = st.number_input('Strength', min_value=0, max_value=100, value=50, help="Enter the strength of the player")
    total_defending = st.number_input('Total Defending', min_value=0, max_value=100, value=50, help="Enter the total defending ability of the player")
    total_goalkeeping = st.number_input('Total Goalkeeping', min_value=0, max_value=100, value=50, help="Enter the total goalkeeping ability of the player")
    total_stats = st.number_input('Total Stats', min_value=0, max_value=100, value=50, help="Enter the total stats of the player")
    international_reputation = st.number_input('International Reputation', min_value=0, max_value=5, value=1, help="Enter the international reputation of the player")
    pace_diving = st.number_input('Pace / Diving', min_value=0, max_value=100, value=50, help="Enter the pace or diving ability of the player")
    shooting_handling = st.number_input('Shooting / Handling', min_value=0, max_value=100, value=50, help="Enter the shooting or handling ability of the player")
    passing_kicking = st.number_input('Passing / Kicking', min_value=0, max_value=100, value=50, help="Enter the passing or kicking ability of the player")

    # Create a dataframe from the input
    input_data = pd.DataFrame({
        'Age': [age],
        'Overall rating': [overall_rating],
        'Potential': [potential],
        'Height': [height],
        'Weight': [weight],
        'foot': [1 if foot == 'Left' else 0],
        'Best position': [best_position],
        'Growth': [growth],
        'Wage': [wage],
        'Release clause': [release_clause],
        'Jumping': [jumping],
        'Strength': [strength],
        'Total defending': [total_defending],
        'Total goalkeeping': [total_goalkeeping],
        'Total stats': [total_stats],
        'International reputation': [international_reputation],
        'Pace / Diving': [pace_diving],
        'Shooting / Handling': [shooting_handling],
        'Passing / Kicking': [passing_kicking],
    })

    input_data['Best position'] = input_data['Best position'].map(inverse_mapping).fillna(-1).astype(int)

    if st.button('Predict Value'):
        try:
            st.write("Input Data:", input_data)
            context.catalog.save('raw_data', input_data)

            session.run(pipeline_name='data_processing')

            preprocessed_data = context.catalog.load('preprocessed_players_data')

            st.write("Preprocessed Data Columns:", preprocessed_data.columns.tolist())
            st.write(preprocessed_data.head())

            expected_features = model.feature_names_in_  #
            missing_features = set(expected_features) - set(preprocessed_data.columns)
            if missing_features:
                st.error(f"Missing features: {missing_features}")
            else:
                # Predict the value
                prediction = model.predict(preprocessed_data[expected_features])

                # Display the prediction
                st.success(f"Predicted Value: €{prediction[0]:,.2f}")
        except Exception as e:
            st.error(f"An error occurred: {e}")

    st.markdown("""
    **Note:** This prediction is based on the trained model and provided data. Ensure the input values are accurate for a better prediction.
    """)
