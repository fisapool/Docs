import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# Create directory for sample data
os.makedirs('data', exist_ok=True)

# Generate gift card brands and types
gift_card_brands = ['Amazon', 'Walmart', 'Target', 'Best Buy', 'Starbucks', 
                    'iTunes', 'Google Play', 'Nike', 'Visa', 'Mastercard']

# Generate sample historical sales data
def generate_historical_sales(num_records=1000):
    data = []
    
    # Start date - 6 months ago
    start_date = datetime.now() - timedelta(days=180)
    
    for i in range(num_records):
        brand = random.choice(gift_card_brands)
        face_value = random.choice([25, 50, 100, 200, 500])
        
        # Generate random sale date
        days_from_start = random.randint(0, 180)
        sale_date = (start_date + timedelta(days=days_from_start)).strftime('%Y-%m-%d')
        
        # Generate moderately realistic pricing based on brand and face value
        brand_discount = {
            'Amazon': 0.05,
            'Walmart': 0.08,
            'Target': 0.10,
            'Best Buy': 0.12,
            'Starbucks': 0.06,
            'iTunes': 0.15,
            'Google Play': 0.15,
            'Nike': 0.10,
            'Visa': 0.03,
            'Mastercard': 0.04
        }
        
        # Apply some randomness and seasonal effects
        base_discount = brand_discount.get(brand, 0.10)
        month = (start_date + timedelta(days=days_from_start)).month
        
        # Higher discounts during holiday seasons
        if month in [11, 12]:  # November, December
            seasonal_effect = random.uniform(0.02, 0.05)
        elif month in [1, 6, 7]:  # January, June, July
            seasonal_effect = random.uniform(0.01, 0.03)
        else:
            seasonal_effect = random.uniform(-0.01, 0.01)
            
        total_discount = base_discount + seasonal_effect
        
        # Apply day of week effect (weekend vs weekday)
        day_of_week = (start_date + timedelta(days=days_from_start)).weekday()
        if day_of_week >= 5:  # Weekend
            total_discount += random.uniform(0.01, 0.02)
            
        # Ensure discount is within reasonable bounds
        total_discount = max(0.01, min(0.25, total_discount))
        
        sale_price = round(face_value * (1 - total_discount), 2)
        
        data.append({
            'gift_card_id': f"GC-{i+1}",
            'gift_card_type': brand,
            'face_value': face_value,
            'sale_date': sale_date,
            'sale_price': sale_price,
            'customer_rating': random.randint(3, 5),
            'days_to_expiry': random.randint(90, 730),
            'is_digital': random.choice([0, 1]),
            'brand_popularity': random.randint(60, 100)  # Brand popularity score
        })
    
    return pd.DataFrame(data)

# Generate sample inventory data
def generate_inventory(num_records=100):
    data = []
    
    for i in range(num_records):
        brand = random.choice(gift_card_brands)
        face_value = random.choice([25, 50, 100, 200, 500])
        
        # Base price with brand-specific discount
        brand_discount = {
            'Amazon': 0.05,
            'Walmart': 0.08,
            'Target': 0.10,
            'Best Buy': 0.12,
            'Starbucks': 0.06,
            'iTunes': 0.15,
            'Google Play': 0.15,
            'Nike': 0.10,
            'Visa': 0.03,
            'Mastercard': 0.04
        }
        
        discount = brand_discount.get(brand, 0.10) + random.uniform(-0.02, 0.02)
        current_price = round(face_value * (1 - discount), 2)
        
        data.append({
            'gift_card_id': f"GC-INV-{i+1}",
            'gift_card_type': brand,
            'face_value': face_value,
            'current_price': current_price,
            'acquisition_price': round(current_price * 0.9, 2),
            'days_in_inventory': random.randint(0, 60),
            'is_digital': random.choice([0, 1]),
            'brand_popularity': random.randint(60, 100)
        })
    
    return pd.DataFrame(data)

# Generate sample competitor pricing data
def generate_competitor_data():
    data = {}
    
    for brand in gift_card_brands:
        brand_data = []
        
        for face_value in [25, 50, 100, 200, 500]:
            # Different competitors have different pricing strategies
            competitor1_discount = random.uniform(0.03, 0.12)
            competitor2_discount = random.uniform(0.05, 0.15)
            competitor3_discount = random.uniform(0.02, 0.10)
            
            brand_data.append({
                'face_value': face_value,
                'competitor1_price': round(face_value * (1 - competitor1_discount), 2),
                'competitor2_price': round(face_value * (1 - competitor2_discount), 2),
                'competitor3_price': round(face_value * (1 - competitor3_discount), 2)
            })
        
        data[brand] = brand_data
    
    return data

# Generate the data
historical_sales = generate_historical_sales(5000)
current_inventory = generate_inventory(200)
competitor_data = generate_competitor_data()

# Save to CSV files
historical_sales.to_csv('data/historical_sales.csv', index=False)
current_inventory.to_csv('data/current_inventory.csv', index=False)

# Save competitor data to JSON
import json
with open('data/competitor_prices.json', 'w') as f:
    json.dump(competitor_data, f, indent=2)

print("Sample data generated successfully!") 