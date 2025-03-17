// Add this new file with more sophisticated algorithms
function advancedPriceOptimization(data) {
    // More sophisticated pricing algorithm
    return data.map(item => {
        const faceValue = parseFloat(item.face_value || 0);
        const currentPrice = parseFloat(item.current_price || 0);
        const daysInInventory = parseFloat(item.days_in_inventory || 0);
        
        // Apply more factors to the pricing decision
        let discount = 0.15; // Base discount
        
        // Factor in inventory age
        if (daysInInventory > 30) {
            discount += 0.05; // Increase discount for older inventory
        } else if (daysInInventory < 7) {
            discount -= 0.03; // Reduce discount for fresh inventory
        }
        
        // Factor in face value
        if (faceValue > 100) {
            discount += 0.02; // Higher discount for higher value cards
        }
        
        // Ensure discount is within reasonable bounds
        discount = Math.max(0.05, Math.min(0.25, discount));
        
        const optimizedPrice = faceValue * (1 - discount);
        const priceChange = ((optimizedPrice - currentPrice) / currentPrice * 100).toFixed(2);
        
        return {
            ...item,
            optimized_price: optimizedPrice.toFixed(2),
            price_change: priceChange,
            discount_percentage: (discount * 100).toFixed(2) + '%',
            confidence: calculateConfidence(item)
        };
    });
}

function calculateConfidence(item) {
    // Algorithm to determine confidence in the pricing recommendation
    const daysInInventory = parseFloat(item.days_in_inventory || 0);
    
    // Lower confidence for very new or very old inventory
    if (daysInInventory < 3 || daysInInventory > 60) {
        return 'Low';
    } else if (daysInInventory >= 7 && daysInInventory <= 30) {
        return 'High';
    } else {
        return 'Medium';
    }
} 