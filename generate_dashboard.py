from dashboard_generator import DashboardGenerator
from pathlib import Path

# Create instance of dashboard generator
generator = DashboardGenerator(
    data_dir="data",
    output_dir="docs"
)

# Generate the dashboard
generator.generate_dashboard()

print("Dashboard generation complete. Check the docs directory.") 