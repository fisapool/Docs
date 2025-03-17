// Data processing functionality
document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('upload-form');
    const resultArea = document.getElementById('upload-result');
    const resultsContainer = document.getElementById('results-container');
    
    uploadForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const fileInput = document.getElementById('data-file');
        const dataType = document.getElementById('data-type').value;
        
        if (fileInput.files.length === 0) {
            alert('Please select a file to upload');
            return;
        }
        
        const file = fileInput.files[0];
        
        // Display loading message
        resultArea.innerHTML = '<p>Processing data...</p>';
        resultArea.classList.add('active');
        
        // Read the CSV file
        const reader = new FileReader();
        
        reader.onload = function(e) {
            const csvData = e.target.result;
            processData(csvData, dataType);
        };
        
        reader.onerror = function() {
            resultArea.innerHTML = '<p>Error reading file</p>';
        };
        
        reader.readAsText(file);
    });
    
    function processData(csvData, dataType) {
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
                resultArea.innerHTML = '<p>Unknown data type</p>';
                return;
        }
        
        displayResults(results, dataType);
    }
    
    function processInventoryData(data) {
        // Use the advanced analysis instead of the simple algorithm
        return advancedPriceOptimization(data);
    }
    
    function processCompetitorData(data) {
        // Simulate ML processing for competitor data
        return data.map(item => {
            const competitorPrice = parseFloat(item.competitor_price || 0);
            
            // Simple competitive pricing strategy
            const recommendedPrice = competitorPrice * 0.95;
            
            return {
                ...item,
                recommended_price: recommendedPrice.toFixed(2),
                strategy: 'Undercut by 5%'
            };
        });
    }
    
    function processHistoricalData(data) {
        // Simulate ML processing for historical data
        // Calculate average prices by product type
        const productTypes = {};
        
        data.forEach(item => {
            const type = item.product_type || 'Unknown';
            const price = parseFloat(item.price || 0);
            
            if (!productTypes[type]) {
                productTypes[type] = {
                    count: 0,
                    total: 0
                };
            }
            
            productTypes[type].count++;
            productTypes[type].total += price;
        });
        
        return Object.keys(productTypes).map(type => {
            const avg = productTypes[type].total / productTypes[type].count;
            return {
                product_type: type,
                average_price: avg.toFixed(2),
                data_points: productTypes[type].count,
                trend: avg > 50 ? 'Upward' : 'Downward'
            };
        });
    }
    
    function displayResults(results, dataType) {
        if (!results || results.length === 0) {
            resultArea.innerHTML = '<p>No results to display</p>';
            return;
        }
        
        // Create table to display results
        let tableHtml = '<table><thead><tr>';
        
        // Table headers based on first result object
        const headers = Object.keys(results[0]);
        headers.forEach(header => {
            tableHtml += `<th>${header.replace('_', ' ')}</th>`;
        });
        
        tableHtml += '</tr></thead><tbody>';
        
        // Table rows
        results.forEach(result => {
            tableHtml += '<tr>';
            headers.forEach(header => {
                tableHtml += `<td>${result[header]}</td>`;
            });
            tableHtml += '</tr>';
        });
        
        tableHtml += '</tbody></table>';
        
        // Display results
        resultArea.innerHTML = `
            <h3>Analysis Results (${dataType})</h3>
            <p>${results.length} items processed</p>
            ${tableHtml}
        `;
        
        // Also show in results container
        resultsContainer.innerHTML = `
            <h3>Latest Analysis</h3>
            <p>Data type: ${dataType}</p>
            <p>Items processed: ${results.length}</p>
            <button id="view-details" class="btn-primary">View Details</button>
        `;
        
        document.getElementById('view-details').addEventListener('click', function() {
            resultArea.scrollIntoView({ behavior: 'smooth' });
        });
    }
});