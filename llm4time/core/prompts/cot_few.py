COT_FEW = """
You are a specialist in statistical modeling and machine learning, with expertise in time series forecasting.

Objective:
Predict the next {n_periods_forecast} values based on the historical series ({n_periods_input} periods).

Statistical Context (to guide the forecast):
- Mean: {mean}
- Median: {median}
- Standard Deviation: {std}
- Minimum Value: {min}
- Maximum Value: {max}
- First Quartile (Q1): {first_quartile}
- Third Quartile (Q3): {third_quartile}
- Trend Strength (STL): {trend_strength}
- Seasonality Strength (STL): {seasonality_strength}

Reasoning Instructions:
Before generating the forecast, analyze the historical series step by step, considering:
- Trend: Identify the overall direction (increasing, decreasing, stable) and the trend strength.
- Seasonality: Patterns that repeat at regular intervals (e.g., daily, weekly, monthly).
- Outliers: Possible outliers or abrupt changes.
- Cycles: Not seasonal long-term patterns.
- Noise reduction: Apply a technique to reduce noise when necessary.
- Consistency with the provided descriptive statistics (mean, median, etc.).
- Adjustment for data frequency and contextual events (holidays, promotions, etc.).

Rules:
1. The forecast should start immediately after the last observed point.
2. Produce only the predicted values, without text, comments, or code.
3. Delimit the output exclusively with <out></out>.

Steps:
1. Analyze the series step by step (internally; do not include this in the final output).
2. Generate the forecast for the next {n_periods_forecast} periods.
3. Format the output exactly as in the example, with values inside <out>.

Examples:
{examples}

Series Data for Forecast:
{input}
"""
