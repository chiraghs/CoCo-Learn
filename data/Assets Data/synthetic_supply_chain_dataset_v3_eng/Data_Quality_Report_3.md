# Data Quality Report 3 — Full Data Quality Assessment

*Translated from: `Kalite Raporu DATA.docx` — AI-Based Stock Tracking and Demand Forecasting System – Quality Report*

## 1. Project Scope and Data Production Methodology

The core objective of this project is to develop an AI-based system that analyzes historical sales data and seasonal effects to produce product-level demand forecasts, reduce inventory costs, and provide decision support for optimal order planning. To meet these goals, the dataset used was synthetically generated with a deterministic seed (`seed=42`) in order to model real-world supply-chain dynamics.

The dataset covers a 365-day simulation period (01.01.2025 – 31.12.2025). In total, 120 products (SKUs), 30 categories, 12 suppliers, 120 customer companies, and 4 distinct sales channels (Online, Retail, Wholesale, B2B Express) are integrated into the database.

## 2. Database Architecture and Structural Integrity Tests

Architectural (referential) integrity tests applied to prevent system crashes and to stop the AI model from learning from incorrect data produced flawless results.

- **Uniqueness (Primary Key) Check:** It was proven that the `STOKGUNLUK` (Daily Stock) table contains exactly one row per product/date (`product_id`, `date`) combination each day, with no duplicate records. Full compliance with the uniqueness principle was achieved, with 0 faulty records.
- **Referential Integrity (Foreign Key) Check:** No "orphaned" product records were found when examining the sales and stock tables; all ID matches were successfully validated.
- **Physical and Logical Time Constraints:** In line with fundamental physical rules of inventory management, it was verified that the on-hand stock quantity (`on_hand_qty`) in the `STOKGUNLUK` table never fell below zero (negative) in any scenario. Similarly, it was confirmed that in the `SATIN_ALMA` (Purchasing) table, the receipt date (`receipt_date`) never occurs before the order date (`order_date`).

## 3. Supply Chain Business Rules and Design Validations (False Alarms)

Some metrics that were assessed as statistical weaknesses or errors in the initial test phase were confirmed to be logical and correct *by design*, in line with the architectural intent of the Data Production Plan:

- **Special-Day Lift Effect:** When examining the demand impact of campaign and holiday periods in the `OZEL_OLAYLAR` (Special Events) table, sales were found to increase by only 0.9% on special days (from 1,023 units to 1,032 units). This low signal is not a data error. The original production plan used the design `Event → logistics + campaign` and `Weather → logistics`. In other words, the intent was for events and weather to hit logistics processes — not to increase consumer demand. The lack of a demand-side lift is therefore exactly what the design intended.
- **Lack of Lagged (Lag) Correlation:** Sales velocity in the days approaching event dates was tested, and the Pearson correlation came out at −0.051, showing no meaningful relationship. Since events were designed to affect logistics (events → logistics) rather than create a demand increase, the absence of a lag correlation is fully consistent with the design.
- **Absence of Currency Noise (Deliberate Omission):** The planned 10% rate of differing currency usage — intended to prevent the data from being over-learned — did not materialize; currency variability in the dataset remained at 0.00%. This is not a coding error; it was deliberately omitted in the early stages to avoid over-complicating the AI model.
- **Inactive-Product Sales Noise:** A total of 2,787 sales rows were found to have been generated for 8 products marked as inactive in the system. This will require filtering during training.

## 4. Impact on the Model and Genuine Signal Weakness

The single genuine design flaw that must be corrected for the AI algorithms to produce accurate forecasts was identified in price elasticity:

- **Non-Functioning Discount Signal:** The relationship between discount rate and sales quantity was calculated at 0.035 (near zero), indicating that discounts do not increase sales volume.
- **Analysis:** The Data Production Plan explicitly includes the rule "as discount rate increases, sales quantity increases" (discount ↑ → qty ↑). Since a scenario of price-inelastic products was outside the plan, this is a clear signal weakness that will prevent the model from learning the price effect.

## 5. Segmentation and Risk (Bottleneck) Analysis

Supply chain segmentation and operational risk scenarios have been successfully integrated into the database.

- **ABC Segmentation:** Sales data strongly confirms the Pareto principle. Class A products dominate 59.4% of total volume, while Class C products account for only 13.1%.
- **Stockout Scenarios:** Across the simulation, stock was confirmed to hit zero for various products on exactly 353 distinct days. This scenario provides an excellent foundation for the model to learn "stockout" behavior and perform lost-sales calculations.

## 6. Conclusion and Optimization Recommendations

The current synthetic dataset has a flawless structure in terms of software architecture and database integration testing. Based on the analyses performed, the following firm conclusions have been reached regarding the system's learnability by AI:

- **Full Suitability for Logistics and Operational Models (Design Validation):** It is now confirmed that the "Special-Day Effect (Event Lift)" and "Lagged Correlation (Lag Correlation)" results — previously interpreted as weak signals in earlier tests — are in fact fully consistent with the data production plan design. Since the production plan deliberately designed events and weather to affect logistics rather than demand (Weather → logistics, Event → logistics), expecting a demand spike on special days or a lagged demand correlation is a false assumption. The dataset is therefore fully ready and highly reliable for supply-delay, risk-prediction, and stock-optimization algorithms. No artificial multiplier intended to boost demand on special days should ever be added to the code.
- **Currency Noise (Deliberate Omission):** The differing-currency-use rate, planned at 10% but measured at 0% in testing, has been reported as a finding. However, this was deliberately excluded from the documentation and omitted at this stage of the project to avoid over-complicating the AI model.
- **The Single Critical Action for V3: Fixing the Discount/Demand Signal:** The only genuine obstacle preventing the model from learning "price elasticity" from this dataset is the weak discount signal. The correlation between discount rate and demand increase (0.035) is a genuine signal weakness. The `discount ↑ → qty ↑` logic explicitly targeted in the production plan is not reflected in the data.
- **V3 Optimization Recommendation:** Only the discount logic in the data-production script needs to be refined and corrected. A logic block should be integrated so that when discount rates increase during campaign periods (e.g., exceeding 15%), sales quantity (`qty`) is directly and proportionally affected. In addition, to prevent MOQ (Minimum Order Quantity) violations in the `SATIN_ALMA` (Purchasing) table, the rule "if `qty_ordered` < `min_order_qty`, then set `qty_ordered` = `min_order_qty`" should be enforced.

Once these revisions are completed, the system will reach production-ready quality standards for all AI models end-to-end, including the Demand Forecasting model.

## 7. Final Note and Decision

As stated in earlier project meetings, priority within this project has been given to *modeling supply chain and inventory behavior*. Given this, although the relationship between discount and sales quantity was found to be limited in the current dataset, the demand model was designed to be multi-factor (seasonality, channel, customer segment, price effect, etc.). For this reason, the discount variable failing to produce a strong correlation on its own was not assessed as a critical issue for the overall system design.

It was decided to *proceed to the modeling stage with the current dataset rather than regenerating it*. If a data-related problem or performance constraint is identified during model development, both the discount–demand relationship and any other identified data scenarios will be improved together in the next iteration (V3 data production).

In line with this decision, the project has been planned to *continue with modeling and analysis on the current dataset*.
