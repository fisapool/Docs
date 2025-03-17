import pandas as pd
import numpy as np
import json
from pathlib import Path
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os

class DashboardGenerator:
    def __init__(self, data_dir, output_dir):
        self.data_dir = Path(data_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def generate_dashboard(self):
        """Generate the complete dashboard"""
        # Create dashboard directory structure
        (self.output_dir / 'js').mkdir(exist_ok=True)
        (self.output_dir / 'css').mkdir(exist_ok=True)
        (self.output_dir / 'data').mkdir(exist_ok=True)
        
        # Create basic HTML files
        self._create_html_files()
        self._create_css_files()
        self._create_js_files()
        
        print(f"Dashboard generated at {self.output_dir}")
        
    def _create_html_files(self):
        """Create the HTML files for the dashboard"""
        html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Business Pricing Dashboard</title>
    <link rel="stylesheet" href="css/styles.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        /* Inline critical styles for initial loading */
        .page-loader {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: #f8f9fa;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 9999;
            transition: opacity 0.5s, visibility 0.5s;
        }
        .page-loader.loaded {
            opacity: 0;
            visibility: hidden;
        }
        .page-loader-spinner {
            width: 60px;
            height: 60px;
            border: 6px solid #f3f3f3;
            border-top: 6px solid #4361ee;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-bottom: 20px;
        }
        .page-loader-text {
            font-family: 'Segoe UI', 'Roboto', sans-serif;
            font-size: 18px;
            color: #4361ee;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <!-- Page loading overlay -->
    <div class="page-loader" id="page-loader">
        <div class="page-loader-spinner"></div>
        <p class="page-loader-text">Loading Dashboard...</p>
    </div>

    <div class="dashboard-container">
        <aside class="sidebar">
            <div class="brand">
                <i class="fas fa-chart-line"></i>
                <h2>Price Optimizer</h2>
            </div>
            <nav class="main-nav">
                <ul>
                    <li class="active"><a href="#"><i class="fas fa-home"></i> Dashboard</a></li>
                    <li><a href="#"><i class="fas fa-upload"></i> Upload Data</a></li>
                    <li><a href="#"><i class="fas fa-chart-bar"></i> Analytics</a></li>
                    <li><a href="#"><i class="fas fa-cog"></i> Settings</a></li>
                </ul>
            </nav>
        </aside>

        <main class="main-content">
            <header class="top-bar">
                <div class="search-container">
                    <i class="fas fa-search"></i>
                    <input type="text" placeholder="Search..." id="search-input">
                </div>
                <div class="user-menu">
                    <span>Welcome, Admin</span>
                    <i class="fas fa-user-circle"></i>
                </div>
            </header>

            <div class="content-area">
                <div class="dashboard-header">
                    <h1>Pricing Dashboard</h1>
                    <div class="date-display" id="current-date">Loading date...</div>
                </div>

                <div class="metrics-cards">
                    <div class="metric-card">
                        <div class="metric-icon bg-blue">
                            <i class="fas fa-tags"></i>
                        </div>
                        <div class="metric-content">
                            <h3>Products Analyzed</h3>
                            <p class="metric-value" id="products-count">0</p>
                            <p class="metric-change positive"><i class="fas fa-arrow-up"></i> 12% from last month</p>
                        </div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-icon bg-green">
                            <i class="fas fa-dollar-sign"></i>
                        </div>
                        <div class="metric-content">
                            <h3>Avg. Price</h3>
                            <p class="metric-value" id="avg-price">$0.00</p>
                            <p class="metric-change negative"><i class="fas fa-arrow-down"></i> 3% from last month</p>
                        </div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-icon bg-orange">
                            <i class="fas fa-chart-pie"></i>
                        </div>
                        <div class="metric-content">
                            <h3>Market Coverage</h3>
                            <p class="metric-value" id="market-coverage">0%</p>
                            <p class="metric-change positive"><i class="fas fa-arrow-up"></i> 5% from last month</p>
                        </div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-icon bg-purple">
                            <i class="fas fa-sync"></i>
                        </div>
                        <div class="metric-content">
                            <h3>Last Update</h3>
                            <p class="metric-value" id="last-update">Never</p>
                            <p class="metric-note">Real-time data</p>
                        </div>
                    </div>
                </div>
                
                <div class="dashboard-row">
                    <div class="dashboard-card wide-card">
                        <div class="card-header">
                            <h2><i class="fas fa-chart-line"></i> Price Trends</h2>
                            <div class="card-actions">
                                <select id="trend-period">
                                    <option value="7">Last 7 days</option>
                                    <option value="30" selected>Last 30 days</option>
                                    <option value="90">Last 90 days</option>
                                </select>
                            </div>
                        </div>
                        <div class="card-body">
                            <canvas id="price-trend-chart"></canvas>
                        </div>
                    </div>
                </div>

                <div class="dashboard-row">
                    <div class="dashboard-card">
                        <div class="card-header">
                            <h2><i class="fas fa-upload"></i> Data Upload</h2>
                        </div>
                        <div class="card-body">
                            <form id="upload-form" class="styled-form">
                                <div class="form-group">
                                    <label for="data-file">Select CSV File:</label>
                                    <div class="file-input-container">
                                        <input type="file" id="data-file" accept=".csv" required>
                                        <div class="file-input-button">
                                            <i class="fas fa-file-upload"></i> Choose File
                                        </div>
                                        <div class="file-name" id="file-name">No file chosen</div>
                                    </div>
                                </div>
                                <div class="form-group">
                                    <label for="data-type">Data Type:</label>
                                    <div class="select-wrapper">
                                        <select id="data-type" required>
                                            <option value="inventory">Current Inventory</option>
                                            <option value="competitor">Competitor Prices</option>
                                            <option value="historical">Historical Sales</option>
                                        </select>
                                        <i class="fas fa-chevron-down"></i>
                                    </div>
                                </div>
                                <button type="submit" class="btn-primary"><i class="fas fa-cogs"></i> Process Data</button>
                            </form>
                        </div>
                    </div>
                    
                    <div class="dashboard-card">
                        <div class="card-header">
                            <h2><i class="fas fa-chart-pie"></i> Market Segments</h2>
                        </div>
                        <div class="card-body">
                            <canvas id="market-segment-chart"></canvas>
                        </div>
                    </div>
                </div>

                <div class="dashboard-card results-table-card">
                    <div class="card-header">
                        <h2><i class="fas fa-table"></i> Analysis Results</h2>
                        <div class="card-actions">
                            <input type="text" id="table-search" placeholder="Filter results..." class="table-filter">
                            <button id="export-csv" class="btn-export"><i class="fas fa-download"></i> Export</button>
                        </div>
                    </div>
                    <div class="card-body">
                        <div id="upload-result" class="result-area active">
                            <div class="table-container" id="results-table-container">
                                <!-- Table will be inserted here -->
                            </div>
                        </div>
                    </div>
                </div>
                
                <div id="results-container" class="dashboard-notification"></div>
            </div>
        </main>
    </div>
    
    <script>
        // Remove loader when page is fully loaded
        window.addEventListener('load', function() {
            setTimeout(function() {
                document.getElementById('page-loader').classList.add('loaded');
            }, 500); // Short delay for smoother transition
        });
    </script>
    <script src="js/dashboard.js"></script>
    <script src="js/advanced-analysis.js"></script>
    <script src="js/data-processor.js"></script>
    <script src="js/charts.js"></script>
</body>
</html>"""

        with open(self.output_dir / 'index.html', 'w') as f:
            f.write(html)
            
    def _create_css_files(self):
        """Create CSS files for styling"""
        css = """/* Modern Dashboard Styles */
:root {
    --primary-color: #4361ee;
    --secondary-color: #3f37c9;
    --accent-color: #4895ef;
    --text-color: #333;
    --text-light: #767676;
    --background-color: #f8f9fa;
    --card-color: #ffffff;
    --border-color: #e4e4e4;
    --success-color: #4caf50;
    --warning-color: #ff9800;
    --danger-color: #f44336;
    --sidebar-width: 250px;
    --header-height: 60px;
    --shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

/* Base styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
    line-height: 1.6;
    color: var(--text-color);
    background-color: var(--background-color);
    overflow-x: hidden;
}

/* Dashboard container */
.dashboard-container {
    display: flex;
    min-height: 100vh;
}

/* Sidebar */
.sidebar {
    width: var(--sidebar-width);
    background: linear-gradient(180deg, var(--primary-color), var(--secondary-color));
    color: white;
    padding: 20px 0;
    position: fixed;
    height: 100vh;
    overflow-y: auto;
    z-index: 10;
}

.brand {
    display: flex;
    align-items: center;
    padding: 0 20px 20px 20px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    margin-bottom: 20px;
}

.brand i {
    font-size: 24px;
    margin-right: 10px;
}

.brand h2 {
    font-size: 18px;
    font-weight: 600;
}

.main-nav ul {
    list-style: none;
    padding: 0;
}

.main-nav ul li {
    padding: 10px 20px;
    margin: 5px 0;
    position: relative;
}

.main-nav ul li.active {
    background-color: rgba(255, 255, 255, 0.1);
}

.main-nav ul li.active::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    width: 4px;
    height: 100%;
    background-color: white;
}

.main-nav ul li a {
    color: white;
    text-decoration: none;
    display: flex;
    align-items: center;
}

.main-nav ul li a i {
    margin-right: 10px;
    width: 20px;
    text-align: center;
}

/* Main content */
.main-content {
    flex: 1;
    margin-left: var(--sidebar-width);
    position: relative;
}

.top-bar {
    height: var(--header-height);
    background-color: var(--card-color);
    box-shadow: var(--shadow);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 20px;
    position: sticky;
    top: 0;
    z-index: 5;
}

.search-container {
    position: relative;
    width: 300px;
}

.search-container i {
    position: absolute;
    left: 10px;
    top: 50%;
    transform: translateY(-50%);
    color: var(--text-light);
}

.search-container input {
    width: 100%;
    padding: 8px 10px 8px 35px;
    border: 1px solid var(--border-color);
    border-radius: 20px;
    outline: none;
    font-size: 14px;
}

.user-menu {
    display: flex;
    align-items: center;
    cursor: pointer;
}

.user-menu span {
    margin-right: 10px;
    font-size: 14px;
}

.user-menu i {
    font-size: 24px;
    color: var(--primary-color);
}

.content-area {
    padding: 20px;
    padding-bottom: 40px;
}

.dashboard-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.dashboard-header h1 {
    font-size: 24px;
    font-weight: 600;
}

.date-display {
    font-size: 14px;
    color: var(--text-light);
}

/* Metric cards */
.metrics-cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
    margin-bottom: 20px;
}

.metric-card {
    background-color: var(--card-color);
    border-radius: 8px;
    box-shadow: var(--shadow);
    padding: 20px;
    display: flex;
    align-items: center;
}

.metric-icon {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 15px;
    font-size: 18px;
    color: white;
}

.bg-blue {
    background-color: #4361ee;
}

.bg-green {
    background-color: #4caf50;
}

.bg-orange {
    background-color: #ff9800;
}

.bg-purple {
    background-color: #9c27b0;
}

.metric-content {
    flex: 1;
}

.metric-content h3 {
    font-size: 14px;
    font-weight: 500;
    color: var(--text-light);
    margin-bottom: 5px;
}

.metric-value {
    font-size: 24px;
    font-weight: 600;
    margin-bottom: 5px;
}

.metric-change {
    font-size: 12px;
}

.metric-change.positive {
    color: var(--success-color);
}

.metric-change.negative {
    color: var(--danger-color);
}

.metric-note {
    font-size: 12px;
    color: var(--text-light);
}

/* Dashboard cards and rows */
.dashboard-row {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
    gap: 20px;
    margin-bottom: 20px;
}

.dashboard-card {
    background-color: var(--card-color);
    border-radius: 8px;
    box-shadow: var(--shadow);
    margin-bottom: 20px;
    overflow: hidden;
}

.wide-card {
    grid-column: 1 / -1;
}

.card-header {
    padding: 15px 20px;
    border-bottom: 1px solid var(--border-color);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.card-header h2 {
    font-size: 16px;
    font-weight: 600;
    display: flex;
    align-items: center;
}

.card-header h2 i {
    margin-right: 10px;
    color: var(--primary-color);
}

.card-actions {
    display: flex;
    align-items: center;
}

.card-actions select {
    padding: 5px 10px;
    border: 1px solid var(--border-color);
    border-radius: 4px;
    font-size: 14px;
    outline: none;
}

.card-body {
    padding: 20px;
}

/* Form styles */
.styled-form {
    max-width: 100%;
}

.form-group {
    margin-bottom: 20px;
}

.form-group label {
    display: block;
    margin-bottom: 8px;
    font-weight: 500;
    font-size: 14px;
}

.file-input-container {
    position: relative;
    display: flex;
    align-items: center;
}

.file-input-container input[type="file"] {
    position: absolute;
    width: 0.1px;
    height: 0.1px;
    opacity: 0;
    overflow: hidden;
    z-index: -1;
}

.file-input-button {
    background-color: var(--primary-color);
    color: white;
    padding: 8px 15px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    display: inline-flex;
    align-items: center;
}

.file-input-button i {
    margin-right: 8px;
}

.file-name {
    margin-left: 10px;
    font-size: 14px;
    color: var(--text-light);
}

.select-wrapper {
    position: relative;
}

.select-wrapper select {
    appearance: none;
    width: 100%;
    padding: 10px 15px;
    border: 1px solid var(--border-color);
    border-radius: 4px;
    background-color: white;
    font-size: 14px;
    cursor: pointer;
}

.select-wrapper i {
    position: absolute;
    right: 10px;
    top: 50%;
    transform: translateY(-50%);
    pointer-events: none;
    color: var(--text-light);
}

.btn-primary {
    background-color: var(--primary-color);
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    display: inline-flex;
    align-items: center;
    transition: background-color 0.3s;
}

.btn-primary:hover {
    background-color: var(--secondary-color);
}

.btn-primary i {
    margin-right: 8px;
}

.btn-export {
    background-color: transparent;
    color: var(--primary-color);
    border: 1px solid var(--primary-color);
    padding: 5px 10px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    display: inline-flex;
    align-items: center;
    margin-left: 10px;
}

.btn-export i {
    margin-right: 5px;
}

/* Table styles */
.results-table-card {
    margin-bottom: 40px;
}

.table-filter {
    padding: 5px 10px;
    border: 1px solid var(--border-color);
    border-radius: 4px;
    font-size: 14px;
    width: 200px;
}

.table-container {
    overflow-x: auto;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
    font-size: 14px;
}

thead th {
    background-color: #f1f3f9;
    color: var(--primary-color);
    font-weight: 600;
    text-align: left;
    padding: 12px 15px;
    border-bottom: 2px solid var(--primary-color);
    position: sticky;
    top: 0;
    z-index: 1;
}

tbody tr {
    border-bottom: 1px solid var(--border-color);
}

tbody tr:nth-child(even) {
    background-color: #f9f9f9;
}

tbody tr:hover {
    background-color: #f1f3f9;
}

td {
    padding: 12px 15px;
    max-width: 300px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

td a {
    color: var(--primary-color);
    text-decoration: none;
}

td a:hover {
    text-decoration: underline;
}

/* Result area */
.result-area {
    display: none;
}

.result-area.active {
    display: block;
}

.dashboard-notification {
    background-color: var(--primary-color);
    color: white;
    padding: 15px;
    border-radius: 4px;
    margin-bottom: 20px;
    display: none;
}

/* Responsive adjustments */
@media (max-width: 1024px) {
    .sidebar {
        width: 60px;
        overflow: visible;
    }
    
    .brand h2, .main-nav ul li a span {
        display: none;
    }
    
    .main-nav ul li a i {
        margin-right: 0;
    }
    
    .main-content {
        margin-left: 60px;
    }
    
    .dashboard-row {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 768px) {
    .metrics-cards {
        grid-template-columns: 1fr;
    }
    
    .top-bar {
        padding: 0 10px;
    }
    
    .search-container {
        width: 200px;
    }
    
    .card-header {
        flex-direction: column;
        align-items: flex-start;
    }
    
    .card-actions {
        margin-top: 10px;
    }
}

@media (max-width: 480px) {
    .content-area {
        padding: 10px;
    }
    
    .search-container {
        display: none;
    }
}

/* Add these loading indicator styles */
.loading-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px 20px;
    text-align: center;
}

.loading-spinner {
    width: 50px;
    height: 50px;
    border: 5px solid #f3f3f3;
    border-top: 5px solid var(--primary-color);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 20px;
}

.loading-text {
    font-size: 18px;
    margin-bottom: 10px;
    color: var(--primary-color);
}

.loading-subtext {
    font-size: 14px;
    color: var(--text-light);
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.notification {
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 15px 20px;
    background: white;
    border-left: 4px solid var(--primary-color);
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.15);
    display: flex;
    align-items: center;
    border-radius: 4px;
    z-index: 1000;
    transform: translateX(120%);
    transition: transform 0.3s ease;
    max-width: 350px;
}

.notification.show {
    transform: translateX(0);
}

.notification i {
    margin-right: 10px;
    font-size: 18px;
}

.notification-success {
    border-left-color: var(--success-color);
}

.notification-success i {
    color: var(--success-color);
}

.notification-error {
    border-left-color: var(--danger-color);
}

.notification-error i {
    color: var(--danger-color);
}

.notification-warning {
    border-left-color: var(--warning-color);
}

.notification-warning i {
    color: var(--warning-color);
}

.notification-info {
    border-left-color: var(--accent-color);
}

.notification-info i {
    color: var(--accent-color);
}

.notification .close-btn {
    margin-left: 10px;
    background: none;
    border: none;
    cursor: pointer;
    font-size: 14px;
    color: #aaa;
}

.notification .close-btn:hover {
    color: #666;
}

.processing-status {
    display: flex;
    align-items: center;
    background-color: var(--primary-color);
    color: white;
    padding: 10px 15px;
    border-radius: 4px;
    margin-bottom: 15px;
    animation: pulse 2s infinite;
}

.processing-status i {
    margin-right: 10px;
}

@keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.8; }
    100% { opacity: 1; }
}"""

        with open(self.output_dir / 'css' / 'styles.css', 'w') as f:
            f.write(css)
            
    def _create_js_files(self):
        """Create JavaScript files for interactivity"""
        # Original dashboard.js
        js = """// Dashboard functionality
document.addEventListener('DOMContentLoaded', function() {
    console.log('Dashboard loaded');
    
    // You can add more interactive features here
    // This is just a placeholder for now
});"""

        with open(self.output_dir / 'js' / 'dashboard.js', 'w') as f:
            f.write(js)
        
        # Update data processor with loading indicators
        data_processor_js = """// Data processing functionality
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
        const rows = csvData.split('\\n');
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
});"""

        with open(self.output_dir / 'js' / 'data-processor.js', 'w') as f:
            f.write(data_processor_js)
        
        # Add this optimization
        charts_js = """// Only load data that's visible
        function lazyLoadCharts() {
            // Only initialize charts when in viewport
            const observers = [];
            document.querySelectorAll('canvas').forEach(canvas => {
                const observer = new IntersectionObserver(entries => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            // Initialize chart when visible
                            initializeChart(canvas.id);
                            observer.disconnect();
                        }
                    });
                });
                observer.observe(canvas);
                observers.push(observer);
            });
        }
        
        document.addEventListener('DOMContentLoaded', lazyLoadCharts);
        """
        
        # Add this to your charts.js file
        
        with open(self.output_dir / 'js' / 'charts.js', 'w') as f:
            f.write(charts_js) 