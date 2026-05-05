# Module 11 Assignment: Data Visualization with Matplotlib
# SunCoast Retail Visual Analysis

# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Welcome message
print("=" * 60)
print("SUNCOAST RETAIL VISUAL ANALYSIS")
print("=" * 60)

# ----- USE THE FOLLOWING CODE TO CREATE SAMPLE DATA (DO NOT MODIFY) -----
# Create a seed for reproducibility
np.random.seed(42)

# Generate dates for 8 quarters (Q1 2022 - Q4 2023)
quarters = pd.date_range(start='2022-01-01', periods=8, freq='Q')
quarter_labels = ['Q1 2022', 'Q2 2022', 'Q3 2022', 'Q4 2022', 
                 'Q1 2023', 'Q2 2023', 'Q3 2023', 'Q4 2023']

# Store locations
locations = ['Tampa', 'Miami', 'Orlando', 'Jacksonville']

# Product categories
categories = ['Electronics', 'Clothing', 'Home Goods', 'Sporting Goods', 'Beauty']

# Generate quarterly sales data for each location and category
quarterly_data = []

for quarter_idx, quarter in enumerate(quarters):
    for location in locations:
        for category in categories:
            # Base sales with seasonal pattern (Q4 higher, Q1 lower)
            base_sales = np.random.normal(loc=100000, scale=20000)
            seasonal_factor = 1.0
            if quarter.quarter == 4:  # Q4 (holiday boost)
                seasonal_factor = 1.3
            elif quarter.quarter == 1:  # Q1 (post-holiday dip)
                seasonal_factor = 0.8
            
            # Location effect
            location_factor = {
                'Tampa': 1.0,
                'Miami': 1.2,
                'Orlando': 0.9,
                'Jacksonville': 0.8
            }[location]
            
            # Category effect
            category_factor = {
                'Electronics': 1.5,
                'Clothing': 1.0,
                'Home Goods': 0.8,
                'Sporting Goods': 0.7,
                'Beauty': 0.9
            }[category]
            
            # Growth trend over time (5% per year, quarterly compounded)
            growth_factor = (1 + 0.05/4) ** quarter_idx
            
            # Calculate sales with some randomness
            sales = base_sales * seasonal_factor * location_factor * category_factor * growth_factor
            sales = sales * np.random.normal(loc=1.0, scale=0.1)  # Add noise
            
            # Advertising spend (correlated with sales but with diminishing returns)
            ad_spend = (sales ** 0.7) * 0.05 * np.random.normal(loc=1.0, scale=0.2)
            
            # Record
            quarterly_data.append({
                'Quarter': quarter,
                'QuarterLabel': quarter_labels[quarter_idx],
                'Location': location,
                'Category': category,
                'Sales': round(sales, 2),
                'AdSpend': round(ad_spend, 2),
                'Year': quarter.year
            })

# Create customer data
customer_data = []
total_customers = 2000

# Age distribution parameters for each location
age_params = {
    'Tampa': (45, 15),      # Older demographic
    'Miami': (35, 12),      # Younger demographic
    'Orlando': (38, 14),    # Mixed demographic
    'Jacksonville': (42, 13)  # Middle-aged demographic
}

for location in locations:
    # Generate ages based on location demographics
    mean_age, std_age = age_params[location]
    customer_count = int(total_customers * {
        'Tampa': 0.3,
        'Miami': 0.35,
        'Orlando': 0.2,
        'Jacksonville': 0.15
    }[location])
    
    ages = np.random.normal(loc=mean_age, scale=std_age, size=customer_count)
    ages = np.clip(ages, 18, 80).astype(int)  # Ensure ages are between 18-80
    
    # Generate purchase amounts
    for age in ages:
        # Younger and older customers spend differently across categories
        if age < 30:
            category_preference = np.random.choice(categories, p=[0.3, 0.3, 0.1, 0.2, 0.1])
        elif age < 50:
            category_preference = np.random.choice(categories, p=[0.25, 0.2, 0.25, 0.15, 0.15])
        else:
            category_preference = np.random.choice(categories, p=[0.15, 0.1, 0.35, 0.1, 0.3])
        
        # Purchase amount based on age and category
        base_amount = np.random.gamma(shape=5, scale=20)
        
        # Product tier (budget, mid-range, premium)
        price_tier = np.random.choice(['Budget', 'Mid-range', 'Premium'], 
                                     p=[0.3, 0.5, 0.2])
        
        tier_factor = {'Budget': 0.7, 'Mid-range': 1.0, 'Premium': 1.8}[price_tier]
        
        purchase_amount = base_amount * tier_factor
        
        customer_data.append({
            'Location': location,
            'Age': age,
            'Category': category_preference,
            'PurchaseAmount': round(purchase_amount, 2),
            'PriceTier': price_tier
        })

# Create DataFrames
sales_df = pd.DataFrame(quarterly_data)
customer_df = pd.DataFrame(customer_data)

# Add some calculated columns
sales_df['Quarter_Num'] = sales_df['Quarter'].dt.quarter
sales_df['SalesPerDollarSpent'] = sales_df['Sales'] / sales_df['AdSpend']

# Print data info
print("\nSales Data Sample:")
print(sales_df.head())
print("\nCustomer Data Sample:")
print(customer_df.head())
print("\nDataFrames created successfully. Ready for visualization!")
# ----- END OF DATA CREATION -----


# TODO 1: Time Series Visualization - Sales Trends
# 1.1 Create a line chart showing overall quarterly sales trends
# REQUIRED: Function must create and return a matplotlib figure
def plot_quarterly_sales_trend():
    """
    Create a line chart showing total sales for each quarter.
    REQUIRED: Return the figure object
    """
    quarterly_sales = sales_df.groupby('QuarterLabel')['Sales'].sum().reindex(quarter_labels)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(quarterly_sales.index, quarterly_sales.values, marker='o', linewidth=2)
    ax.set_title('Overall Quarterly Sales Trend')
    ax.set_xlabel('Quarter')
    ax.set_ylabel('Total Sales ($)')
    ax.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

# 1.2 Create a multi-line chart comparing sales trends across locations
# REQUIRED: Function must create and return a matplotlib figure
def plot_location_sales_comparison():
    """
    Create a multi-line chart comparing quarterly sales across different locations.
    REQUIRED: Return the figure object
    """
    location_sales = sales_df.groupby(['QuarterLabel', 'Location'])['Sales'].sum().unstack()
    location_sales = location_sales.reindex(quarter_labels)

    fig, ax = plt.subplots(figsize=(10, 5))
    markers = ['o', 's', '^', 'D']

    for i, location in enumerate(location_sales.columns):
        ax.plot(location_sales.index, location_sales[location], marker=markers[i], linewidth=2, label=location)

    ax.set_title('Quarterly Sales Comparison by Location')
    ax.set_xlabel('Quarter')
    ax.set_ylabel('Total Sales ($)')
    ax.legend(title='Location')
    ax.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig


# TODO 2: Categorical Comparison - Product Performance by Location
# 2.1 Create a grouped bar chart comparing category performance by location
# REQUIRED: Function must create and return a matplotlib figure
def plot_category_performance_by_location():
    """
    Create a grouped bar chart showing how each product category performs in different locations.
    REQUIRED: Return the figure object
    """
    most_recent_quarter = sales_df['Quarter'].max()
    recent_data = sales_df[sales_df['Quarter'] == most_recent_quarter]

    grouped_data = recent_data.groupby(['Category', 'Location'])['Sales'].sum().unstack()
    grouped_data = grouped_data.reindex(categories)

    x = np.arange(len(categories))
    width = 0.2

    fig, ax = plt.subplots(figsize=(12, 6))
    for i, location in enumerate(grouped_data.columns):
        ax.bar(x + i * width, grouped_data[location], width, label=location)

    ax.set_title('Category Performance by Location (Most Recent Quarter)')
    ax.set_xlabel('Product Category')
    ax.set_ylabel('Sales ($)')
    ax.set_xticks(x + width * 1.5)
    ax.set_xticklabels(categories, rotation=20)
    ax.legend(title='Location')
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    return fig

# 2.2 Create a stacked bar chart showing the composition of sales in each location
# REQUIRED: Function must create and return a matplotlib figure
def plot_sales_composition_by_location():
    """
    Create a stacked bar chart showing the composition of sales across categories for each location.
    REQUIRED: Return the figure object
    """
    composition = sales_df.groupby(['Location', 'Category'])['Sales'].sum().unstack()
    composition = composition.reindex(index=locations, columns=categories)

    percentage_composition = composition.div(composition.sum(axis=1), axis=0) * 100

    fig, ax = plt.subplots(figsize=(10, 6))
    bottom = np.zeros(len(percentage_composition))

    for category in percentage_composition.columns:
        ax.bar(percentage_composition.index, percentage_composition[category], bottom=bottom, label=category)
        bottom += percentage_composition[category].values

    ax.set_title('Sales Composition by Location (Percentage)')
    ax.set_xlabel('Location')
    ax.set_ylabel('Percentage of Total Sales (%)')
    ax.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    return fig


# TODO 3: Relationship Analysis - Advertising and Sales
# 3.1 Create a scatter plot to examine the relationship between ad spend and sales
# REQUIRED: Function must create and return a matplotlib figure
def plot_ad_spend_vs_sales():
    """
    Create a scatter plot to visualize the relationship between advertising spend and sales.
    REQUIRED: Return the figure object
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(sales_df['AdSpend'], sales_df['Sales'], alpha=0.7)

    # Best-fit line
    coeffs = np.polyfit(sales_df['AdSpend'], sales_df['Sales'], 1)
    best_fit = np.poly1d(coeffs)
    x_vals = np.linspace(sales_df['AdSpend'].min(), sales_df['AdSpend'].max(), 100)
    ax.plot(x_vals, best_fit(x_vals), linestyle='--', linewidth=2)

    # Annotate notable outliers based on residuals
    predicted_sales = best_fit(sales_df['AdSpend'])
    residuals = np.abs(sales_df['Sales'] - predicted_sales)
    outliers = sales_df.loc[residuals.nlargest(3).index]

    for _, row in outliers.iterrows():
        ax.annotate(
            f"{row['Location']} - {row['Category']}",
            (row['AdSpend'], row['Sales']),
            textcoords="offset points",
            xytext=(5, 5),
            fontsize=8
        )

    ax.set_title('Ad Spend vs. Sales')
    ax.set_xlabel('Advertising Spend ($)')
    ax.set_ylabel('Sales ($)')
    ax.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    return fig

# 3.2 Create a line chart showing sales per dollar spent on advertising over time
# REQUIRED: Function must create and return a matplotlib figure
def plot_ad_efficiency_over_time():
    """
    Create a line chart showing how efficient advertising spend has been over time.
    REQUIRED: Return the figure object
    """
    efficiency = sales_df.groupby('QuarterLabel')['SalesPerDollarSpent'].mean().reindex(quarter_labels)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(efficiency.index, efficiency.values, marker='o', linewidth=2)

    max_q = efficiency.idxmax()
    min_q = efficiency.idxmin()

    ax.annotate(f'Highest: {max_q}', xy=(max_q, efficiency[max_q]),
                xytext=(0, 10), textcoords='offset points', ha='center')
    ax.annotate(f'Lowest: {min_q}', xy=(min_q, efficiency[min_q]),
                xytext=(0, -15), textcoords='offset points', ha='center')

    ax.set_title('Advertising Efficiency Over Time')
    ax.set_xlabel('Quarter')
    ax.set_ylabel('Sales per Advertising Dollar')
    ax.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig


# TODO 4: Distribution Analysis - Customer Demographics
# 4.1 Create histograms of customer age distribution
# REQUIRED: Function must create and return a matplotlib figure with subplots
def plot_customer_age_distribution():
    """
    Create histograms showing the age distribution of customers, both overall and by location.
    REQUIRED: Return the figure object
    """
    fig, axes = plt.subplots(3, 2, figsize=(12, 12))
    axes = axes.flatten()

    # Overall distribution
    axes[0].hist(customer_df['Age'], bins=15, edgecolor='black')
    axes[0].axvline(customer_df['Age'].mean(), linestyle='--', linewidth=2, label='Mean')
    axes[0].axvline(customer_df['Age'].median(), linestyle=':', linewidth=2, label='Median')
    axes[0].set_title('Overall Customer Age Distribution')
    axes[0].set_xlabel('Age')
    axes[0].set_ylabel('Frequency')
    axes[0].legend()

    # By location
    for i, location in enumerate(locations, start=1):
        location_ages = customer_df[customer_df['Location'] == location]['Age']
        axes[i].hist(location_ages, bins=15, edgecolor='black')
        axes[i].axvline(location_ages.mean(), linestyle='--', linewidth=2, label='Mean')
        axes[i].axvline(location_ages.median(), linestyle=':', linewidth=2, label='Median')
        axes[i].set_title(f'Age Distribution - {location}')
        axes[i].set_xlabel('Age')
        axes[i].set_ylabel('Frequency')
        axes[i].legend()

    # Remove extra subplot
    fig.delaxes(axes[5])

    plt.tight_layout()
    return fig

# 4.2 Create box plots comparing purchase amounts by age groups
# REQUIRED: Function must create and return a matplotlib figure
def plot_purchase_by_age_group():
    """
    Create box plots showing purchase amounts across different age groups.
    REQUIRED: Return the figure object
    """
    age_group_df = customer_df.copy()
    age_group_df['AgeGroup'] = pd.cut(
        age_group_df['Age'],
        bins=[17, 30, 45, 60, 100],
        labels=['18-30', '31-45', '46-60', '61+']
    )

    grouped = [
        age_group_df[age_group_df['AgeGroup'] == group]['PurchaseAmount']
        for group in ['18-30', '31-45', '46-60', '61+']
    ]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.boxplot(grouped, labels=['18-30', '31-45', '46-60', '61+'], patch_artist=True)
    ax.set_title('Purchase Amount by Age Group')
    ax.set_xlabel('Age Group')
    ax.set_ylabel('Purchase Amount ($)')
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    return fig


# TODO 5: Sales Distribution - Pricing Tiers
# 5.1 Create a histogram of purchase amounts
# REQUIRED: Function must create and return a matplotlib figure
def plot_purchase_amount_distribution():
    """
    Create a histogram showing the distribution of purchase amounts.
    REQUIRED: Return the figure object
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(customer_df['PurchaseAmount'], bins=20, edgecolor='black')
    ax.set_title('Purchase Amount Distribution')
    ax.set_xlabel('Purchase Amount ($)')
    ax.set_ylabel('Frequency')
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    return fig

# 5.2 Create a pie chart showing sales breakdown by price tier
# REQUIRED: Function must create and return a matplotlib figure
def plot_sales_by_price_tier():
    """
    Create a pie chart showing the breakdown of sales by price tier.
    REQUIRED: Return the figure object
    """
    tier_sales = customer_df.groupby('PriceTier')['PurchaseAmount'].sum()
    tier_sales = tier_sales.reindex(['Budget', 'Mid-range', 'Premium'])

    explode = [0] * len(tier_sales)
    explode[np.argmax(tier_sales.values)] = 0.1

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(
        tier_sales.values,
        labels=tier_sales.index,
        autopct='%1.1f%%',
        explode=explode,
        startangle=90
    )
    ax.set_title('Sales by Price Tier')
    plt.tight_layout()
    return fig


# TODO 6: Market Share Analysis
# 6.1 Create a pie chart showing sales breakdown by category
# REQUIRED: Function must create and return a matplotlib figure
def plot_category_market_share():
    """
    Create a pie chart showing the market share of each product category.
    REQUIRED: Return the figure object
    """
    category_sales = sales_df.groupby('Category')['Sales'].sum().reindex(categories)

    explode = [0] * len(category_sales)
    explode[np.argmax(category_sales.values)] = 0.1

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(
        category_sales.values,
        labels=category_sales.index,
        autopct='%1.1f%%',
        explode=explode,
        startangle=90
    )
    ax.set_title('Category Market Share')
    plt.tight_layout()
    return fig

# 6.2 Create a pie chart showing sales breakdown by location
# REQUIRED: Function must create and return a matplotlib figure
def plot_location_sales_distribution():
    """
    Create a pie chart showing the distribution of sales across different store locations.
    REQUIRED: Return the figure object
    """
    location_sales = sales_df.groupby('Location')['Sales'].sum().reindex(locations)

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(
        location_sales.values,
        labels=location_sales.index,
        autopct='%1.1f%%',
        startangle=90
    )
    ax.set_title('Location Sales Distribution')
    plt.tight_layout()
    return fig


# TODO 7: Comprehensive Dashboard
# REQUIRED: Function must create and return a matplotlib figure with at least 4 subplots
def create_business_dashboard():
    """
    Create a comprehensive dashboard with multiple subplots highlighting key business insights.
    REQUIRED: Return the figure object with at least 4 subplots
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('SunCoast Retail Business Dashboard', fontsize=16)

    # 1. Overall sales trend
    quarterly_sales = sales_df.groupby('QuarterLabel')['Sales'].sum().reindex(quarter_labels)
    axes[0, 0].plot(quarterly_sales.index, quarterly_sales.values, marker='o', linewidth=2)
    axes[0, 0].set_title('Overall Quarterly Sales Trend')
    axes[0, 0].tick_params(axis='x', rotation=45)
    axes[0, 0].grid(True, linestyle='--', alpha=0.6)

    # 2. Sales by location
    location_sales = sales_df.groupby('Location')['Sales'].sum().reindex(locations)
    axes[0, 1].bar(location_sales.index, location_sales.values)
    axes[0, 1].set_title('Total Sales by Location')
    axes[0, 1].set_ylabel('Sales ($)')
    axes[0, 1].grid(axis='y', linestyle='--', alpha=0.6)

    # 3. Category market share
    category_sales = sales_df.groupby('Category')['Sales'].sum().reindex(categories)
    axes[1, 0].pie(category_sales.values, labels=category_sales.index, autopct='%1.1f%%', startangle=90)
    axes[1, 0].set_title('Category Market Share')

    # 4. Purchase amount distribution
    axes[1, 1].hist(customer_df['PurchaseAmount'], bins=20, edgecolor='black')
    axes[1, 1].set_title('Purchase Amount Distribution')
    axes[1, 1].set_xlabel('Purchase Amount ($)')
    axes[1, 1].set_ylabel('Frequency')
    axes[1, 1].grid(axis='y', linestyle='--', alpha=0.6)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    return fig


# Main function to execute all visualizations
# REQUIRED: Do not modify this function name
def main():
    print("\n" + "=" * 60)
    print("SUNCOAST RETAIL VISUAL ANALYSIS RESULTS")
    print("=" * 60)
    
    # REQUIRED: Call all visualization functions and store figures
    # Store each figure in a variable for potential saving/display
    
    # Time Series Analysis
    fig1 = plot_quarterly_sales_trend()
    fig2 = plot_location_sales_comparison()
    
    # Categorical Comparison
    fig3 = plot_category_performance_by_location()
    fig4 = plot_sales_composition_by_location()
    
    # Relationship Analysis
    fig5 = plot_ad_spend_vs_sales()
    fig6 = plot_ad_efficiency_over_time()
    
    # Distribution Analysis
    fig7 = plot_customer_age_distribution()
    fig8 = plot_purchase_by_age_group()
    
    # Sales Distribution
    fig9 = plot_purchase_amount_distribution()
    fig10 = plot_sales_by_price_tier()
    
    # Market Share Analysis
    fig11 = plot_category_market_share()
    fig12 = plot_location_sales_distribution()
    
    # Comprehensive Dashboard
    fig13 = create_business_dashboard()
    
    # REQUIRED: Add business insights summary
    print("\nKEY BUSINESS INSIGHTS:")
    
    total_sales_by_quarter = sales_df.groupby('QuarterLabel')['Sales'].sum().reindex(quarter_labels)
    best_quarter = total_sales_by_quarter.idxmax()
    worst_quarter = total_sales_by_quarter.idxmin()
    
    total_sales_by_location = sales_df.groupby('Location')['Sales'].sum()
    best_location = total_sales_by_location.idxmax()
    
    total_sales_by_category = sales_df.groupby('Category')['Sales'].sum()
    top_category = total_sales_by_category.idxmax()
    
    avg_age_by_location = customer_df.groupby('Location')['Age'].mean()
    youngest_location = avg_age_by_location.idxmin()
    oldest_location = avg_age_by_location.idxmax()
    
    price_tier_sales = customer_df.groupby('PriceTier')['PurchaseAmount'].sum()
    top_tier = price_tier_sales.idxmax()

    print(f"- Sales were highest in {best_quarter} and lowest in {worst_quarter}.")
    print(f"- {best_location} generated the highest total sales among all store locations.")
    print(f"- {top_category} was the top-performing product category overall.")
    print(f"- {youngest_location} had the youngest customer base on average, while {oldest_location} had the oldest.")
    print(f"- {top_tier} products contributed the largest share of customer purchase revenue.")
    print("- The ad spend vs. sales chart suggests a positive relationship between advertising and sales performance.")
    
    print("\nBUSINESS RECOMMENDATIONS:")
    print(f"- Increase focus on {top_category} products since they lead total category sales.")
    print(f"- Study {best_location}'s strategy and apply successful practices to lower-performing locations.")
    print("- Use advertising budget more strategically in periods with stronger efficiency.")
    print("- Tailor product promotions by location based on customer age patterns and buying behavior.")

    # Display all figures
    plt.show()

# Run the main function
if __name__ == "__main__":
    main()