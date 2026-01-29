# NYSE Matching Engine 📈

**NYSE Matching Engine** is a robust simulation of a stock exchange marketplace built with Python. It models the core functionality of the New York Stock Exchange, handling order processing, trade execution, and volume analysis based on strict financial matching principles.

The system processes a stream of Buy/Sell orders and executes trades based on **Price-Time Priority**, handling complex edge cases like partial fills and timestamp collisions.

## 🚀 Key Features

* **Algorithmic Order Matching:** Automatically pairs buyers and sellers when `Buy Price ≥ Sell Price`.
* **Price-Time Priority:** Prioritizes orders based on timestamp, optimizing for the earliest available trades.
* **Partial Fills:** Supports partial execution of large orders, keeping the remainder open for future liquidity.
* **Advanced Tie-Breaking:** Implements a multi-layered sorting logic for orders with identical timestamps (Alphabetical Stock Name → Price Advantage → User ID).
* **Financial Analytics:** Includes built-in functions to calculate executed volumes and remaining liquidity per user or timeframe.

## ⚙️ How It Works

The simulation reads a stream of order data and applies the following logic:

### 1. Matching Logic
Trades are executed if the buy price meets the sell price.The transaction occurs at the **Sell Order's Price**.
* **Self-Trade Prevention:** Users cannot trade with themselves.
* **Stock Isolation:** Apple (AAPL) orders never match with Microsoft (MSFT) orders.

### 2. Tie-Breaking Rules
When multiple orders arrive at the exact same timestamp, priority is resolved as follows:
1.  **Stock Name:** Alphabetical order.
2.  **Price:** Lower prices for Sellers, Higher prices for Buyers.
3.  **User ID:** Users with lower IDs get priority.

## 📊 Analytics Functions

The system provides detailed reporting through four core functions:

* `total_executed_volume(time)`: Calculates total value of all trades up to a specific timestamp.
* `executed_user_volume(user_id, time)`: Tracks the trading volume of a specific investor.
* `total_remaining_volume(time)`: Analyzing market depth by calculating unexecuted open orders.
* `remaining_user_volume(user_id, time)`: Shows the pending exposure for a specific user.

## 📂 Input Format

The engine expects order data in the following format:
`YYYY-MM-DD-hh-mm-ss <User_ID> <Name> <Stock> <Type> <Quantity> <Price>`

**Example:**
```text
2024-11-18-10-56-35 32 Ali AAPL Buy 15 45.0
```

---
*Developed by Melih Efe Sonmez.*
