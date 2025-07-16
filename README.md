Aave V2 Wallet Credit Scoring
This project assigns credit scores to wallets that interact with the Aave V2 protocol, using their historical transaction behavior. The score ranges from 0 to 1000, where higher scores reflect more responsible usage patterns.

Project Overview
Given a large dataset of raw transaction-level data (~100,000 records), we build a machine learning pipeline that processes these records and generates a single score per wallet. The model is fully unsupervised and uses clustering to group wallets by behavior before assigning scores.

How the Scoring Works
Load and clean the data
The raw JSON file is flattened, and all missing values are handled appropriately.

Feature encoding
Categorical columns like network, protocol, and action types are label encoded.

Wallet-level aggregation
We group data by wallet addresses and calculate behavioral features such as:

Number of transactions

Total and average value involved

Unique actions performed (e.g., deposit, borrow, repay)

Total collateral and debt

Borrow rate statistics

Clustering
We use KMeans clustering to group wallets into 5 behavioral categories.

Scoring
Each cluster is assigned a fixed score:

Cluster 0 → 200

Cluster 1 → 400

Cluster 2 → 600

Cluster 3 → 800

Cluster 4 → 1000

Getting Started
Requirements
Python 3.8+

Pandas

NumPy

scikit-learn

Streamlit

Installation->pip install pandas numpy scikit-learn streamlit

Running the App
Make sure you have both app.py and client.py in the same folder.

Run the Streamlit app using:->streamlit run client.py
Upload your user-wallet-transactions.json file when prompted.

Output
The app will generate a downloadable CSV that includes:

userWallet

Aggregated transaction features

Cluster label

Final credit_score

Use Cases
Risk profiling of DeFi wallets

Identifying reliable or risky users for rewards or monitoring

Behavioral analysis in lending or borrowing protocols

Author
Asang Triratna Ingle
Machine Learning Engineer | Deep Learning and DeFi Enthusiast