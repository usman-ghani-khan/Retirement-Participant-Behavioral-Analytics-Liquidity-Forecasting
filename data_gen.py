import pandas as pd
import numpy as np

# Set seed for accuracy and consistency
np.random.seed(42)

# Configuration
n_participants = 1000
months = 36

# --- TABLE 1: Participants (The Dimension Table) ---
ids = [f"P{i:04d}" for i in range(1, n_participants + 1)]
groups = np.random.choice(['Power-Saver', 'Auto-Pilot', 'Fragile'], n_participants, p=[0.3, 0.5, 0.2])

data_p = []
for i in range(n_participants):
    p_id = ids[i]
    group = groups[i]

    if group == 'Power-Saver':
        salary = np.random.normal(135000, 15000)
        savings_rate = np.random.uniform(0.10, 0.15)
        login_freq = np.random.randint(12, 30)
    elif group == 'Fragile':
        salary = np.random.normal(52000, 8000)
        savings_rate = np.random.uniform(0.01, 0.04)
        login_freq = np.random.randint(0, 4)
    else: # Auto-Pilot
        salary = np.random.normal(82000, 12000)
        savings_rate = 0.06
        login_freq = np.random.randint(4, 10)

    data_p.append([p_id, round(salary, 2), round(savings_rate, 3), login_freq, group])

df_p = pd.DataFrame(data_p, columns=['participant_id', 'salary', 'savings_rate', 'login_frequency', 'segment_label'])
df_p.to_csv('participants.csv', index=False)

# --- TABLE 2: Transactions (The Fact Table) ---
data_t = []
for m in range(1, months + 1):
    # Market Crash logic in Month 18
    market_perf = -0.18 if m == 18 else np.random.normal(0.007, 0.02)

    for i in range(n_participants):
        p_id = ids[i]
        group = groups[i]

        # Loan Logic: High spike for 'Fragile' group during market crash
        loan_chance = 0.01
        if m >= 18 and group == 'Fragile':
            loan_chance = 0.18 # 18% chance of loan during volatility

        has_loan = 1 if np.random.random() < loan_chance else 0
        loan_amt = np.random.randint(2000, 6000) if has_loan else 0

        data_t.append([p_id, m, round(market_perf, 4), has_loan, loan_amt])

df_t = pd.DataFrame(data_t, columns=['participant_id', 'month_id', 'market_return', 'loan_event', 'loan_amount'])
df_t.to_csv('transactions.csv', index=False)

print("Files generated: 'participants.csv' and 'transactions.csv'")
