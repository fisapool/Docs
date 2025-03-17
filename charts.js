// Chart initialization with loading states
function initializeChart(chartId) {
    const ctx = document.getElementById(chartId);
    if (!ctx) return;
    
    // Show loading indicator inside the chart area
    ctx.parentNode.innerHTML = `
        <div class="chart-loading">
            <div class="loading-spinner"></div>
            <p>Preparing chart...</p>
        </div>
        <canvas id="${chartId}"></canvas>
    `;
    
    // Get the new canvas (after DOM update)
    const newCtx = document.getElementById(chartId);
    
    // Create chart based on chart ID
    setTimeout(() => {
        if (chartId === 'price-trend-chart') {
            createPriceTrendChart(newCtx);
        } else if (chartId === 'market-segment-chart') {
            createMarketSegmentChart(newCtx);
        }
        
        // Remove the loading indicator
        const loadingElement = newCtx.parentNode.querySelector('.chart-loading');
        if (loadingElement) {
            loadingElement.remove();
        }
    }, 600); // Small delay to show loading state
} 