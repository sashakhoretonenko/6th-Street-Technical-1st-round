from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

# Load and prep data

import pandas as pd

loan_data = pd.read_csv("loan_data.csv")
loan_data['loan_amount'] = loan_data['loan_amount'].astype(float)
loan_data['current_balance'] = loan_data['current_balance'].astype(float)

def total_outstanding_balance(df):
    return df['current_balance'].sum()

def avg_ir_by_sector(df):
    avg_by_sec = df.groupby('sector')['interest_rate'].mean()
    return avg_by_sec

def default_rate(df):
    return (df['status'] == 'Default').sum() / len(df['status'])

def compute_summary(df):
    TOB = total_outstanding_balance(df)
    AVG_IR_BY_SEC = avg_ir_by_sector(df).round(3).to_dict()
    DR = default_rate(df)

    return {
        "Total Outstanding Balance: ": round(TOB, 2),
        "Average Interest Rate by Sector: ": AVG_IR_BY_SEC,
        "Default Rate: ": round(DR * 100, 2)
    }

# Routing endpoints
@app.route("/summary", methods=['GET'])
def summary():
    return jsonify(compute_summary(loan_data))

if __name__ == '__main__':
    app.run(debug=True)
