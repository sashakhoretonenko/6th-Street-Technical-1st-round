1. Data Cleaning & Loading (20 mins)
   • Load the CSV into a DataFrame
   • Parse the date columns into datetime
   • Ensure loan_amount, current_balance are floats

2. Key Metrics (30 mins)

Write functions to calculate:
• Total outstanding loan amount (sum of current balances)
• Average interest rate by sector
• Default rate (number of loans with status “Default” / total)

3. Risk Flagging (30 mins)

Create a new column called risk_flag with the following logic:
• “High” if:
• status is “Late” or “Default”
• OR current_balance / loan_amount < 0.4
• “Medium” if:
• balance ratio is between 0.4 and 0.6
• “Low” otherwise

Print out a summary: how many loans fall into each risk category?

4. (Optional) Build a Flask API (30 mins)

If you have time, expose a simple /summary endpoint that:
• Returns the total loan amount
• Default rate
• And sector-wise average interest rates in JSON
