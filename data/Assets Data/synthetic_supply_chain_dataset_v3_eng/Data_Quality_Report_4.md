# Data Quality Report 4 — ABC Product Segmentation Analysis

*Source: `ABC_Product_Segmentation_Report.docx`*

## 1. Purpose of the Analysis

The purpose of this report is to identify the most important products in the supply chain based on their revenue contribution and to evaluate how inventory behaves across different product classes.

ABC analysis is a common inventory management technique used to categorize products according to their economic importance. By identifying high-impact products, resources, inventory space, and monitoring efforts can be allocated more effectively.

This report aims to answer the following questions:

- Which products generate the majority of revenue?
- How are products distributed across A, B, and C segments?
- How do inventory levels differ between these segments?
- Do products change segments over time?

## 2. Revenue Calculation

Product revenue was calculated using the following formula:

**Revenue = Quantity × Unit Price × (1 − Discount Rate)**

This ensures that discounts applied during sales are reflected in the revenue calculation. Total revenue was aggregated for each product in order to determine the contribution of each product to the overall revenue.

## 3. Pareto Analysis

Products were sorted by their revenue contribution and cumulative revenue share was calculated.

The Pareto principle suggests that a small number of products generate the majority of revenue. Based on cumulative contribution:

- Top 80% of revenue → A Class
- Next 15% → B Class
- Remaining 5% → C Class

The Pareto curve confirms that a limited number of products generate most of the total revenue.

## 4. ABC Segmentation

Using cumulative revenue share, products were classified into three categories:

**A Class** — High-value products that generate the majority of revenue. These products require strict monitoring and careful inventory planning.

**B Class** — Products with moderate revenue contribution. These items require periodic monitoring and balanced inventory levels.

**C Class** — Low-impact products with minimal revenue contribution. These items typically require simpler inventory management strategies.

The results show that Class A products represent a small portion of total products but contribute the largest share of revenue.

## 5. Inventory Behavior by ABC Segment

Inventory levels were analyzed using the `on_hand_qty` variable. The analysis indicates:

- Class A products tend to maintain higher inventory priority
- Class B products maintain moderate stock levels
- Class C products typically hold lower inventory levels

This aligns with standard supply chain management practices, where high-value products are prioritized to prevent stockouts.

## 6. Dynamic ABC Class Changes

An additional analysis examined whether products change ABC classes over time. By counting the number of unique ABC classes for each product across different periods, it was possible to identify products that move between segments.

This dynamic behavior suggests that product importance can change due to demand fluctuations, pricing changes, or promotional campaigns. Therefore, ABC classification should be reviewed periodically rather than treated as a static categorization.

## 7. Business Insights

Several insights emerge from this analysis:

- A small number of products generate the majority of revenue
- Inventory management should prioritize Class A products
- Class B products may have potential to grow into Class A
- Class C products should be monitored to avoid excessive inventory costs
- Some products change segments over time, indicating demand volatility

## 8. Conclusion

The ABC analysis successfully identifies the most important products based on revenue contribution. The findings support the Pareto principle and highlight the importance of differentiated inventory management strategies for different product segments.

Additionally, the identification of dynamic ABC changes demonstrates that product importance can shift over time. Continuous monitoring of product performance is therefore essential for effective supply chain decision making.
