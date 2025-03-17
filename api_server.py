from flask import Flask, request, jsonify
import pandas as pd
from price_adjuster import PriceAdjuster
from model_selection import load_model

app = Flask(__name__)

@app.route('/api/analyze', methods=['POST'])
def analyze_data():
    # Get data from request
    data = request.json
    data_type = data.get('data_type')
    csv_data = data.get('csv_data')
    
    # Convert to DataFrame
    df = pd.read_csv(pd.StringIO(csv_data))
    
    # Process based on data type
    if data_type == 'inventory':
        # Load models
        adjuster = PriceAdjuster('models/model.pkl', 'config/pricing_config.json')
        results = adjuster.optimize_prices(df)
    elif data_type == 'competitor':
        # Process competitor data
        results = process_competitor_data(df)
    elif data_type == 'historical':
        # Process historical data
        results = process_historical_data(df)
    else:
        return jsonify({"error": "Invalid data type"}), 400
    
    # Return JSON response
    return jsonify({"results": results.to_dict('records')})

if __name__ == '__main__':
    app.run(debug=True) 