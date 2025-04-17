import pandas as pd
import os
import json
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.metrics import accuracy_score
import joblib
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree


def add_average_columns(df):
    """
    For every column that contains a list in each row,
    compute the average of the list and add a new column with suffix '_avg'.
    """
    for col in df.columns:
        if df[col].apply(lambda x: isinstance(x, list)).all():
            # Compute the average for each row; if the list is empty, use 0.
            df[col + '_avg'] = df[col].apply(lambda x: np.mean(x) if len(x) > 0 else 0)
    return df

def expand_list_columns(df):
    """
    Expand DataFrame columns where each entry is a list.
    Each element in a list is moved into its own column (e.g., roll0 -> roll0_0, roll0_1, etc.).
    """
    # Identify columns where every value is a list.
    columns_to_expand = [col for col in df.columns if df[col].apply(lambda x: isinstance(x, list)).all()]
    for col in columns_to_expand:
        max_length = df[col].apply(len).max()  # In case lists are uneven
        new_columns = [f"{col}_{i}" for i in range(max_length)]
        # When lists are of unequal length, missing elements will be filled with NaN.
        expanded_df = pd.DataFrame(df[col].tolist(), columns=new_columns, index=df.index)
        df = df.drop(columns=[col]).join(expanded_df)
    return df

def load_and_process_json(json_path, form_label, flatten_lists=True):
    """
    Load a JSON file from json_path, drop the "rep_id" field if present,
    optionally flatten any list-valued columns, and assign a label (e.g., "bad" or "good").
    """
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    df = pd.DataFrame(data)
    # Drop the "rep_id" column if it exists.
    if 'rep_id' in df.columns:
        df = df.drop(columns=['rep_id'])


    # Drop any columns that start with "env"
    df = df.drop(columns=[col for col in df.columns if col.startswith("env")])
    # Drop any columns that start with "z"
    df = df.drop(columns=[col for col in df.columns if col.startswith("z")])
    # Drop any columns that contain "1" in their name
    df = df.drop(columns=[col for col in df.columns if "1" in col])
        
    if flatten_lists:
        df = expand_list_columns(df)
    
    # Add a column with the provided label.
    df['Form'] = form_label
    return df

def noise_augment_df(df, num_augmented=3, noise_level=0.001):
    """
    Generate augmented data for each row in the DataFrame by adding Gaussian noise
    to every numeric column. Non-numeric columns (such as 'Form') remain unchanged.
    
    Parameters:
      - df: Input DataFrame to augment.
      - num_augmented: The number of augmented versions to generate for each original row.
      - noise_level: Standard deviation of the Gaussian noise added.
    
    Returns:
      A new DataFrame containing the original rows plus the augmented rows.
    """
    augmented_rows = []
    for idx, row in df.iterrows():
        for i in range(num_augmented):
            new_row = row.copy()
            for col in df.columns:
                if pd.api.types.is_numeric_dtype(df[col]):
                    # Add Gaussian noise to numeric columns
                    new_row[col] = row[col] + np.random.normal(0, noise_level)
            # Optionally, add a suffix to an ID if you have one (not required here)
            # if 'rep_id' in df.columns:
            #     new_row['rep_id'] = f"{row['rep_id']}_aug{i+1}"
            augmented_rows.append(new_row)
    df_augmented = pd.DataFrame(augmented_rows)
    return pd.concat([df, df_augmented], ignore_index=True)

def create_training_csv(csv_file='training_data.csv', augment=True, num_augmented=3, noise_level=0.001):
    """
    Create a training CSV file by loading and processing JSON files.
    Drops the rep_id field from the JSON data before combining.
    Replaces missing values (NaN and empty strings) with 0 before saving.
    
    Parameters:
      - csv_file: Name of the output CSV file.
      - augment: If True, apply noise-based augmentation to the training data.
      - num_augmented: Number of augmented samples to create per original sample.
      - noise_level: Standard deviation of the noise to add.
    """
    # Process each JSON file with the appropriate label.
    df_bad = load_and_process_json('bad_form.json', form_label='bad', flatten_lists=True)
    df_good = load_and_process_json('good_form.json', form_label='good', flatten_lists=True)
    
    # Concatenate the processed DataFrames.
    df_training = pd.concat([df_bad, df_good], ignore_index=True)
    
    # Replace missing values (NaN) with 0.
    df_training.fillna(0, inplace=True)
    # Also replace empty strings (or cells containing only whitespace) with 0.
    df_training.replace(r'^\s*$', 0, regex=True, inplace=True)
    
    # Apply noise-based augmentation if requested.
    if augment:
        df_training = noise_augment_df(df_training, num_augmented=num_augmented, noise_level=noise_level)
    
    df_training = add_average_columns(df_training)

    # Save the training data to CSV.
    df_training.to_csv(csv_file, index=False)
    print(f"Created {csv_file} from JSON data.")
    

# Create the training CSV file (this will drop 'rep_id' and fill in missing values/empty strings with 0).
create_training_csv('train.csv')

# Load the training data.
data = pd.read_csv('train.csv')

# Separate the target variable and features.
y = data['Form']
X = data.drop('Form', axis=1)

# Split the data into training and testing sets.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Decision Tree classifier.
model = DecisionTreeClassifier(random_state=42)
model.fit(X_train.values, y_train)

# Evaluate the model.
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f'Model Accuracy: {accuracy:.2f}')

# Save the model.
os.makedirs('ml_model', exist_ok=True)
joblib.dump(model, 'ml_model/posture_classifier.pkl')

# Export and print the decision tree rules.
tree_rules = export_text(model, feature_names=list(X.columns))
print(tree_rules)

plt.figure(figsize=(20, 10))

# Plot the tree. Optionally, include feature names and class names.
plot_tree(model, feature_names=list(X.columns), class_names=model.classes_, filled=True, rounded=True)
plt.show()