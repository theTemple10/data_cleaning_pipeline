import pandas as pd
import re
from datetime import datetime

raw_file = "raw_data.csv"
clean_file = "cleaned_data.csv"
report_file = "data_quality_report.txt"

def is_valid_email(email):
    if pd.isna(email):
        return False
    pattern = r"^[\w\.-]+@[\w\.-]+\.w+$"
    return re.match(pattern, email) is not None

def clean_dataset():
    df = pd.read_csv(raw_file)

    report = []
    report.append(f"DATA QUALITY REPORT")
    report.append(f"Generated: {datetime.now()}")
    report.append("-" * 40)

    initial_rows = len(df)

    # Remove Duplicates
    df.drop_duplicates(inplace=True)
    report.append(f"Duplicates removed: {initial_rows - len(df)}")

    # Standardize Text
    df["Name"] = df["Name"].str.title()
    df["Country"] = df["Country"].str.title()

    # Standardize Age
    df["Age"] = pd.to_numeric(df["Age"], errors = "coerce")
    missing_age = df["Age"].isna().sum()
    df["Age"].fillna(df["Age"].median(), inplace = True)
    report.append(f"Invalid/Missing ages fixed: {missing_age}")

    # Handle Email
    invalid_emails = df[~df["Email"].apply(is_valid_email)]
    report.append(f"Invalid emails flagged: {len(invalid_emails)}")
    df = df[df["Email"].apply(is_valid_email)]

    # Handle missing critical fields
    before_drop = len(df)
    df.dropna(subset=["Name", "Country"], inplace=True)
    report.append(f"Rows removed due to missing critical fields: {before_drop - len(df)}")

    # Save cleaned data
    df.to_csv(clean_file, index=False)

    #Save report
    with open(report_file, "w") as f:
        for line in report:
            f.write(line + "\n")

    print("\n DATA CLEANING SUMMARY")
    for line in report:
        print(line)

    print("\n Cleaned data saved to cleaned_data.csv")
    print(" Data quality report generated")

if __name__ == "__main__":
    clean_dataset()