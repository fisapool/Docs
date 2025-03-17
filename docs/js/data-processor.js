// Data processing functionality
document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('upload-form');
    const resultArea = document.getElementById('upload-result');
    const resultsContainer = document.getElementById('results-container');
    
    // Update dashboard metrics with empty state initially
    updateDashboardMetrics({
        productsCount: '-',
        avgPrice: '-',
        marketCoverage: '-',
        lastUpdate: 'Waiting for data...'
    });
    
    uploadForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const fileInput = document.getElementById('data-file');
        const dataType = document.getElementById('data-type').value;
        
        if (fileInput.files.length === 0) {
            showNotification('Please select a file to upload', 'error');
            return;
        }
        
        const file = fileInput.files[0];
        
        // Display loading message with spinner
        resultArea.innerHTML = `
            <div class="loading-container">
                <div class="loading-spinner"></div>
                <p class="loading-text">Processing ${file.name}...</p>
                <p class="loading-subtext">Analyzing data patterns and optimizing prices</p>
            </div>
        `;
        resultArea.classList.add('active');
        
        // Show processing status in results container
        resultsContainer.innerHTML = `
            <div class="processing-status">
                <i class="fas fa-sync fa-spin"></i>
                <span>Processing ${dataType} data...</span>
            </div>
        `;
        resultsContainer.style.display = 'block';
        
        // Update dashboard metrics to loading state
        updateDashboardMetrics({
            productsCount: '<i class="fas fa-spinner fa-spin"></i>',
            avgPrice: '<i class="fas fa-spinner fa-spin"></i>',
            marketCoverage: '<i class="fas fa-spinner fa-spin"></i>',
            lastUpdate: 'Processing...'
        });
        
        // Read the CSV file
        const reader = new FileReader();
        
        reader.onload = function(e) {
            const csvData = e.target.result;
            // Simulate network delay for demo purposes
            setTimeout(() => {
                processData(csvData, dataType);
            }, 800); // Small delay to show loading state
        };
        
        reader.onerror = function() {
            resultArea.innerHTML = '<div class="error-message"><i class="fas fa-exclamation-triangle"></i> Error reading file</div>';
            showNotification('Failed to read the file', 'error');
        };
        
        reader.readAsText(file);
    });
    
    function processData(csvData, dataType) {
        // Show processing status
        showNotification('Processing data...', 'info');
        
        // Parse CSV
        const rows = csvData.split('\n');
        const headers = rows[0].split(',');
        const data = [];
        
        for (let i = 1; i < rows.length; i++) {
            if (rows[i].trim() === '') continue;
            
            const values = rows[i].split(',');
            const row = {};
            
            for (let j = 0; j < headers.length; j++) {
                row[headers[j].trim()] = values[j].trim();
            }
            
            data.push(row);
        }
        
        // Process based on data type
        let results;
        try {
            switch(dataType) {
                case 'inventory':
                    results = processInventoryData(data);
                    break;
                case 'competitor':
                    results = processCompetitorData(data);
                    break;
                case 'historical':
                    results = processHistoricalData(data);
                    break;
                default:
                    resultArea.innerHTML = '<div class="error-message"><i class="fas fa-exclamation-triangle"></i> Unknown data type</div>';
                    showNotification('Unknown data type', 'error');
                    return;
            }
            
            // Update charts with the processed data
            updateChartsWithData(data, dataType);
            
            // Update dashboard metrics
            updateDashboardMetrics({
                productsCount: data.length,
                avgPrice: calculateAveragePrice(data),
                marketCoverage: calculateMarketCoverage(data, dataType),
                lastUpdate: new Date().toLocaleString()
            });
            
            displayResults(results, dataType);
            showNotification('Analysis complete!', 'success');
        } catch (error) {
            console.error('Error processing data:', error);
            resultArea.innerHTML = `<div class="error-message"><i class="fas fa-exclamation-triangle"></i> Error processing data: ${error.message}</div>`;
            showNotification('Error during analysis', 'error');
        }
    }
    
    function calculateAveragePrice(data) {
        if (!data.length) return '$0.00';
        
        let totalPrice = 0;
        let count = 0;
        
        data.forEach(item => {
            const price = parseFloat(item.current_price || item.competitor_price || item.price || 0);
            if (price > 0) {
                totalPrice += price;
                count++;
            }
        });
        
        return count > 0 ? '$' + (totalPrice / count).toFixed(2) : '$0.00';
    }
    
    function calculateMarketCoverage(data, dataType) {
        if (dataType === 'competitor') {
            // For competitor data, estimate market coverage based on number of competitors
            const uniqueCompetitors = new Set();
            data.forEach(item => {
                if (item.competitor_name) {
                    uniqueCompetitors.add(item.competitor_name);
                }
            });
            
            // Simplified calculation - in real system would be more sophisticated
            return Math.min(uniqueCompetitors.size * 15, 95) + '%';
        } else {
            // For other data types, show a placeholder percentage
            return ((data.length / 10) * 5) + '%';
        }
    }
    
    function updateDashboardMetrics(metrics) {
        document.getElementById('products-count').innerHTML = metrics.productsCount;
        document.getElementById('avg-price').innerHTML = metrics.avgPrice;
        document.getElementById('market-coverage').innerHTML = metrics.marketCoverage;
        document.getElementById('last-update').innerHTML = metrics.lastUpdate;
    }
    
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        
        const icon = type === 'success' ? 'check-circle' : 
                    type === 'error' ? 'exclamation-triangle' : 
                    type === 'warning' ? 'exclamation-circle' : 'info-circle';
        
        notification.innerHTML = `
            <i class="fas fa-${icon}"></i>
            <span>${message}</span>
            <button class="close-btn"><i class="fas fa-times"></i></button>
        `;
        
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.classList.add('show');
        }, 10);
        
        // Auto remove after delay
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 5000);
        
        // Close button
        notification.querySelector('.close-btn').addEventListener('click', function() {
            notification.classList.remove('show');
            setTimeout(() => {
                notification.remove();
            }, 300);
        });
    }
    
    // Rest of your processing functions...
});