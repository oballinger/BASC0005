# Assessed Questions Comparison: Original vs DAP Version

This document provides a comparison between the original assessed questions and the new DAP (Data Analysis Project) versions.

## W01. Python Recap

**Original Question:**
- Dataset: Spotify 2023 streaming data
- Task: Find streams of most danceable song

**DAP Version:**
- Dataset: IMDB movies data
- Task: Calculate average revenue of Action genre movies released after 2010
- Skills: Filtering with multiple conditions, aggregation, rounding

---

## W02. Pandas

**Original Question:**
- Dataset: Wikipedia traffic-related death rates
- Task: Calculate average road fatalities per 100,000 in Asia in 2019
- Methods: `read_html()`, `groupby()`

**DAP Version:**
- Dataset: Wikipedia GDP data
- Task: Calculate total GDP of top 10 countries
- Methods: `read_html()`, data aggregation
- Skills: Similar web scraping approach with different aggregation

---

## W03. Spatial Data

**Original Question:**
- Dataset: Air quality data
- Task: Find day with worst AQI and visualize satellite image
- Methods: Grouping by date, sorting, custom plotting function

**DAP Version:**
- Dataset: Same air quality data
- Task: Calculate monthly AQI averages, identify best/worst months, visualize trends
- Methods: Date manipulation, groupby, visualization, percentage calculations
- Skills: Time series aggregation and comparison

---

## W04. Natural Language Processing

**Original Question:**
- Dataset: 1000 sample tweets
- Task: Find "biggest hater" - most negative subjective tweet author
- Methods: Sentiment polarity and subjectivity filtering

**DAP Version:**
- Dataset: Same tweet sample
- Task: Find users with highest and lowest average polarity, calculate difference
- Methods: Sentiment analysis, groupby user, comparative analysis
- Skills: User-level aggregation of sentiment

---

## W05. Distributions and Basic Statistics

**Original Question:**
- Task: Compare years of schooling between men and women
- Method: 99.7% confidence intervals, visual interpretation
- Question: Determine if difference is statistically significant

**DAP Version:**
- Task: Compare wages between White and Black workers
- Method: 95% confidence intervals, visual interpretation with custom function
- Question: Calculate difference in means, determine significance
- Skills: Similar statistical comparison with different demographic variable

---

## W06. Hypothesis Testing

**Original Question:**
- Task: Find occupation with lowest income disparity between men and women
- Method: Loop through occupations, use `manual_ttest()` function

**DAP Version:**
- Task: Find occupation with smallest wage gap between racial groups
- Method: Loop through occupations, t-tests comparing White and Black workers
- Skills: Same methodology applied to different demographic comparison

---

## W07. Linear Regression

**Original Question:**
- Model: Log wages ~ gender + controls (schooling, age, state, race, occupation)
- Task: Report percentage difference for women, test significance at 99% level

**DAP Version:**
- Model: Log wages ~ schooling + controls (age, race, state, occupation)
- Task: Report percentage increase per year of schooling, test significance at 99% level
- Skills: Similar OLS regression with focus on different predictor

---

## W08. Difference-in-Differences

**Original Question:**
- Task: Find state with largest minimum wage increase in 1990s
- Window: 5 years on each side
- Control: Alabama
- Output: Percentage change in unemployment, significance

**DAP Version:**
- Task: Find state with second largest minimum wage increase in 1990s
- Window: 7 years on each side
- Control: Florida
- Output: Treatment effect coefficient, significance
- Skills: Same DiD methodology with different specifications

---

## W09. Regression Discontinuity

**Original Question:**
- Task: Compare Linear Same Slopes vs Linear Different Slopes
- Analysis: Treatment effect consistency, model fit comparison

**DAP Version:**
- Task: Compare three models: Quadratic Same Slopes, Quadratic Different Slopes, Linear Different Slopes
- Analysis: Treatment effects, R-squared comparison, best model identification
- Skills: Extended comparison including polynomial terms

---

## W10. Machine Learning

**Original Question:**
- None explicitly defined in original notebook

**DAP Version (New):**
- Dataset: Titanic survival data
- Task: Build Random Forest with feature engineering
- Requirements: Create 2+ new features, 5-fold cross-validation, compare tree counts (50, 100, 200)
- Output: Best cross-validation accuracy
- Skills: Feature engineering, cross-validation, hyperparameter comparison

---

## Key Differences

### Pedagogical Approach
- **Original**: Often focused on finding specific values or categories
- **DAP**: More emphasis on analytical process and model comparison

### Complexity
- **Original**: Straightforward single-task questions
- **DAP**: Multi-step analysis with interpretation requirements

### Consistency
- Both versions test the same core competencies
- DAP versions often require additional steps (e.g., visualization, percentage calculations)
- Solutions in DAP include more detailed output and interpretation

### Skills Coverage
Both versions ensure students demonstrate:
1. Data manipulation (filtering, grouping, aggregating)
2. Statistical analysis (confidence intervals, hypothesis tests)
3. Modeling (regression, DiD, RD, ML)
4. Interpretation (translating results to meaningful conclusions)

---

*This comparison demonstrates that the DAP versions maintain pedagogical alignment while providing fresh assessment material.*
