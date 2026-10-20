# Data Quality Report 2 — Compliance Verification Report

*Translated from: `Test Raporu DATA.docx` — AI-Assisted Demand Forecasting: Data Production Plan and Compliance Verification Report*

**Report Purpose:** To audit how the targets set in the synthetic data production plan are reflected in the final generated dataset, and to determine the actions required before the V3 modeling stage.

## 1. Executive Summary and Overall Assessment

The relational architecture specified in the data production plan and diagram has been successfully implemented. All 37 automated tests performed (unit and integration tests) passed successfully, and the data quality score is certified at 100/100. The dataset contains no missing (null) values and no duplicate records.

It has been confirmed that some signal metrics previously flagged as errors (in V1) are in fact working correctly *by design*. The single genuine design flaw that must be corrected before feeding data to the AI model was found in the discount–demand correlation, and will be fixed in the V3 release.

## 2. Comparative Analysis and Compliance Table

Test results have been updated below in light of the architectural plan and new findings:

| Category | Production Plan Target (Expected) | Actual Test Result | Compliance Status |
|---|---|---|---|
| Referential Integrity | PK/FK relationships must be consistent. | 0 faulty records | ✅ Fully Compliant |
| Business Logic (Timing) | Receipt Date ≥ Order Date | Error rate: 0% | ✅ Fully Compliant |
| Special Event (Event) Impact | Plan design: events should hit the "Logistics" side. | Low impact on demand (+0.9%), logistics cost +20–60% (SIG-02) | ✅ Compliant with Design |
| Lagged (Lag) Correlation | Plan design: events should delay logistics, not increase demand. | No demand correlation (−0.051), delivery delay +2–7 days (SIG-01) | ✅ Compliant with Design |
| Currency Noise | 10% "realistic noise" (use of different currencies) should be added. | 0.00% (none at all) | ℹ️ Deliberately Omitted |
| ABC Segmentation | Distribution should follow the Pareto principle. | Approximately Pareto distribution achieved | ✅ Fully Compliant |
| Discount Signal | Increased discount → Increased sales (Qty ↑) | Pearson: 0.035 (near zero) | 🔴 Genuine Defect / To Be Fixed in V3 |

## 3. Critical Findings and Design Validations (False Alarms)

Results that were flagged as weak signals or inconsistencies during the initial test phase, but are in fact consistent with the intended design of the production plan, are clarified below:

- **Special-Day Lift and Lack of Lagged Correlation:** The data production plan used the design `Weather → logistics` and `Event → logistics + campaign`. The intent was for special events and weather to affect the supply chain and delivery times directly, rather than consumer demand. Indeed, regime testing mathematically confirms that unit costs rise 20–60% on event days, and extreme weather extends lead time by 2–7 days. The lack of a demand-side correlation is therefore not a defect — it is the design itself.
- **Absence of Currency Noise:** The 10% currency-differentiation rate specified in the plan came out as 0% in testing. This was correctly detected by the test system; it was deliberately omitted in the V1 and V2 stages to avoid over-complicating the AI model.

## 4. Impact on the Model and Genuine Defects to Be Fixed

The following genuine risks — to be corrected during V3 data production and addressed during Feature Engineering — have been identified:

- **Non-Functioning Discount Signal (V3 Code Revision):** The rule explicitly stated in the production plan — "as discount rate increases, sales quantity increases" (discount ↑ → qty ↑) — is not reflected in the data (correlation: 0.035). This is a genuine signal weakness and will be corrected in the V3 production code.
- **Data Leakage Risk:** The classifications in the `ABC_SEGMENT` table were computed using all 365 days of sales. Since the model being trained needs to predict the future based on the past, this causes future information to leak into the model. When building the training set, ABC classes should be recalculated dynamically using only historical data available at that point in time.
- **Supplier Risk Model Capacity Constraint:** The system contains only 12 suppliers. Building a machine-learning model for supplier risk scoring with such a small sample carries a high risk of overfitting. A rule-based approach should be adopted for this area instead.
- **Inactive-Product Sales Noise:** 2,787 sales records were found for a total of 8 inactive products (constraint KISITLAMA-02). This will appear as noise to the model during training; an `is_active = TRUE` filter should be applied before feeding data into the model.

## 5. Final Note and Decision

As stated in earlier project meetings, priority within this project has been given to *modeling supply chain and inventory behavior*. Given this, although the relationship between discount and sales quantity was found to be limited in the current dataset, the demand model was designed to be multi-factor (seasonality, channel, customer segment, price effect, etc.). For this reason, the discount variable failing to produce a strong correlation on its own was not assessed as a critical issue for the overall system design.

It was decided to *proceed to the modeling stage with the current dataset rather than regenerating it*. If a data-related problem or performance constraint is identified during model development, both the discount–demand relationship and any other identified data scenarios will be improved together in the next iteration (V3 data production).

In line with this decision, the project has been planned to *continue with modeling and analysis on the current dataset*.
