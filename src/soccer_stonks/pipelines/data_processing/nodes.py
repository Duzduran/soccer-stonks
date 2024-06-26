import pandas as pd
import pickle

def load_data(data: pd.DataFrame) -> pd.DataFrame:
    print(f"Data loaded: {data.head()}")  # Debugging print
    return data


def drop_duplicates(data: pd.DataFrame) -> pd.DataFrame:
    return data.drop_duplicates()


def drop_unnecessary_columns(data: pd.DataFrame) -> pd.DataFrame:
    columns_to_drop = ["ID", "name", "Unnamed: 64", "Team & Contract"]
    existing_columns_to_drop = [col for col in columns_to_drop if col in data.columns]
    print(f"Columns in DataFrame: {data.columns.tolist()}")
    print(f"Attempting to drop columns: {existing_columns_to_drop}")
    return data.drop(columns=existing_columns_to_drop)



def encode_and_transform(df: pd.DataFrame) -> pd.DataFrame:
    # Foot encoding
    df['foot'] = df['foot'].replace(["Right", "Left"], [0, 1]).astype("float")

    # Value transformation
    ValueToFloat = df['Value'].str.strip('€').str.extract(r'(\d+\.?\d*)(K|M)').replace({'M': 1000000, 'K': 1000})
    ValueToFloat[0] = pd.to_numeric(ValueToFloat[0], errors='coerce')
    df['Value'] = ValueToFloat.prod(axis=1).astype("float64")

    # Wage transformation
    ValueToFloat = df['Wage'].str.strip('€').str.extract(r'(\d+\.?\d*)(K|M)').replace({'M': 1000000, 'K': 1000})
    ValueToFloat[0] = pd.to_numeric(ValueToFloat[0], errors='coerce')
    df['Wage'] = ValueToFloat.prod(axis=1).astype("float64")

    # Release clause transformation
    ValueToFloat = df['Release clause'].str.strip('€').str.extract(r'(\d+\.?\d*)(K|M)').replace(
        {'M': 1000000, 'K': 1000})
    ValueToFloat[0] = pd.to_numeric(ValueToFloat[0], errors='coerce')
    df['Release clause'] = ValueToFloat.prod(axis=1).astype("float64")

    # Height transformation
    ValueToInt = df['Height'].str.split("/", expand=True)
    ValueToInt.drop(1, axis=1, inplace=True)
    ValueToInt[0] = ValueToInt[0].str.replace('cm', "").astype("int")
    df['Height'] = ValueToInt

    # Weight transformation
    ValueToInt = df['Weight'].str.split("/", expand=True)
    ValueToInt.drop(1, axis=1, inplace=True)
    ValueToInt[0] = ValueToInt[0].str.replace('kg', "").astype("int")
    df['Weight'] = ValueToInt

    fixed_positions = ['CAM', 'ST', 'LWB', 'CB', 'CM', 'RM', 'CDM', 'LM', 'RB', 'RWB', 'LB', 'LW', 'GK', 'CF', 'RW']
    inverse_mapping = {pos: i for i, pos in enumerate(fixed_positions)}

    # Convert 'Best position' using the fixed mapping
    df['Best position'] = df['Best position'].map(inverse_mapping).fillna(-1).astype(int)

    # Save the mappings to a file
    with open('data/08_reporting/category_mapping.pkl', 'wb') as f:
        pickle.dump(inverse_mapping, f)

    return df

def dfObjectSplit(df, column):
    split = df[column].str.split('+', expand=True)
    split2 = split[0].str.split('-', expand=True)
    df[column] = split2[0]
    df[column] = df[column].astype("float")
    return df

def preprocess_data(df):
    columns_to_process = [
        "Overall rating", "Potential", "Crossing", "Finishing", "Heading accuracy",
        "Short passing", "Volleys", "Dribbling", "Curve", "FK Accuracy",
        "Long passing", "Ball control", "Acceleration", "Sprint speed",
        "Agility", "Reactions", "Balance", "Shot power", "Jumping",
        "Stamina", "Strength", "Long shots", "Aggression", "Interceptions",
        "Att. Position", "Vision", "Penalties", "Composure", "Defensive awareness",
        "Standing tackle", "Sliding tackle", "GK Diving", "GK Handling",
        "GK Kicking", "GK Positioning", "GK Reflexes"
    ]
    for column in columns_to_process:
        df = dfObjectSplit(df, column)

    return df

def drop_correlated_columns(df: pd.DataFrame) -> pd.DataFrame:



    columns_to_drop = [
        "Total attacking", "Crossing", "Finishing", "Heading accuracy", "Short passing", "Volleys",
        "Total skill", "Dribbling", "Curve", "FK Accuracy", "Long passing", "Ball control",
        "Total movement", "Acceleration", "Sprint speed", "Agility", "Balance",
        "Total power", "Shot power", "Stamina", "Long shots", "Total mentality",
        "Aggression", "Att. Position", "Vision", "Penalties", "Composure",
        "Best overall", "Reactions", "Base stats", "Interceptions", "Defensive awareness",
        "Standing tackle", "Sliding tackle", "Defending / Pace", "GK Diving",
        "GK Handling", "GK Kicking", "GK Positioning", "GK Reflexes",
        "Dribbling / Reflexes"
    ]
    print(f"Dropping correlated columns: {columns_to_drop}")  # Debugging print
    return df.drop(columns=columns_to_drop)
