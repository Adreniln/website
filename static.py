import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio  # Add this import
import pandas as pd
from datetime import datetime, timedelta
import sys
import platform
import os  # Add this import
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from PIL import Image  # For image processing


def create_visualizations():
    # Base date and mapping setup remains the same
    base_date = datetime(2024, 1, 1)
    final_date = datetime(2027, 6, 30)

    quarter_mapping = {
        'Year 1 Q1': base_date,
        'Year 1 Q2': base_date + timedelta(days=90),
        'Year 1 Q3': base_date + timedelta(days=180),
        'Year 1 Q4': base_date + timedelta(days=270),
        'Year 2 Q1': base_date + timedelta(days=365),
        'Year 2 Q2': base_date + timedelta(days=455),
        'Year 2 Q3': base_date + timedelta(days=545),
        'Year 2 Q4': base_date + timedelta(days=635),
        'Year 3 Q1': base_date + timedelta(days=730),
        'Year 3 Q2': base_date + timedelta(days=820),
        'Year 3 Q3': base_date + timedelta(days=910),
        'Year 3 Q4': base_date + timedelta(days=1000),
        'Year 4 Q1': base_date + timedelta(days=1095),
        'Year 4 Q2': base_date + timedelta(days=1185)
    }

    # Phase transition dates for vertical lines
    phase_transitions = {
        'Phase I': quarter_mapping['Year 1 Q1'],
        'Phase II': quarter_mapping['Year 1 Q3'],
        'Phase III': quarter_mapping['Year 2 Q3'],
        'Phase IV': quarter_mapping['Year 3 Q2']
    }

    # Timeline data remains the same as previous version
    phases = [
        # Phase I tasks
        dict(Phase="Phase I", Task="Technology Audit",
             Start=quarter_mapping['Year 1 Q1'], End=quarter_mapping['Year 1 Q2'],
             Display_Start='Year 1 Q1', Display_End='Year 1 Q2',
             Description="Initial technology audit across department",
             Category="Assessment & Planning",
             IsOngoing=False),
        dict(Phase="Phase I", Task="M365 Standards & Maintenance",
             Start=quarter_mapping['Year 1 Q1'], End=final_date,
             Display_Start='Year 1 Q1', Display_End='Ongoing',
             Description="Establish and maintain Microsoft 365 & Teams standards",
             Category="Infrastructure",
             IsOngoing=True),
        dict(Phase="Phase I", Task="Legacy Migration",
             Start=quarter_mapping['Year 1 Q2'], End=quarter_mapping['Year 1 Q4'],
             Display_Start='Year 1 Q2', Display_End='Year 1 Q4',
             Description="Phase out SharePoint On-Premises",
             Category="Infrastructure",
             IsOngoing=False),

        # Phase II - Implementation & Automation
        dict(Phase="Phase II", Task="Network Standards & Governance",
             Start=quarter_mapping['Year 1 Q3'], End=final_date,
             Display_Start='Year 1 Q3', Display_End='Ongoing',
             Description="Maintain and evolve delivery network standards",
             Category="Implementation",
             IsOngoing=True),
        dict(Phase="Phase II", Task="Process Automation",
             Start=quarter_mapping['Year 1 Q4'], End=final_date,
             Display_Start='Year 1 Q4', Display_End='Ongoing',
             Description="Develop and maintain Power Automate workflows",
             Category="Development",
             IsOngoing=True),
        dict(Phase="Phase II", Task="Custom Solutions Development",
             Start=quarter_mapping['Year 2 Q1'], End=final_date,
             Display_Start='Year 2 Q1', Display_End='Ongoing',
             Description="Create and maintain Power Apps solutions",
             Category="Development",
             IsOngoing=True),

        # Phase III - AI Integration
        dict(Phase="Phase III", Task="AI Implementation & Optimization",
             Start=quarter_mapping['Year 2 Q3'], End=final_date,
             Display_Start='Year 2 Q3', Display_End='Ongoing',
             Description="Implement and enhance AI solutions",
             Category="Innovation",
             IsOngoing=True),
        dict(Phase="Phase III", Task="Analytics Platform",
             Start=quarter_mapping['Year 2 Q4'], End=final_date,
             Display_Start='Year 2 Q4', Display_End='Ongoing',
             Description="Develop and maintain AI-powered analytics",
             Category="Analytics",
             IsOngoing=True),
        dict(Phase="Phase III", Task="Documentation Systems",
             Start=quarter_mapping['Year 3 Q1'], End=final_date,
             Display_Start='Year 3 Q1', Display_End='Ongoing',
             Description="Maintain AI-assisted documentation flows",
             Category="Process Improvement",
             IsOngoing=True),

        # Phase IV - Future Planning
        dict(Phase="Phase IV", Task="Digital Strategy",
             Start=quarter_mapping['Year 3 Q2'], End=final_date,
             Display_Start='Year 3 Q2', Display_End='Ongoing',
             Description="Lead ongoing digital transformation",
             Category="Strategy",
             IsOngoing=True),
        dict(Phase="Phase IV", Task="Emerging Tech Assessment",
             Start=quarter_mapping['Year 3 Q3'], End=final_date,
             Display_Start='Year 3 Q3', Display_End='Ongoing',
             Description="Continuous evaluation of new technologies",
             Category="Innovation",
             IsOngoing=True),
        dict(Phase="Phase IV", Task="Strategic Planning",
             Start=quarter_mapping['Year 3 Q4'], End=final_date,
             Display_Start='Year 3 Q4', Display_End='Ongoing',
             Description="Evolving technology roadmap",
             Category="Strategy",
             IsOngoing=True)
    ]

    # Create timeline
    df = pd.DataFrame(phases)

    # Custom color palette
    custom_colors = ['#2E86C1', '#3498DB', '#85C1E9',  # Blues for Phase I
                     '#27AE60', '#2ECC71', '#82E0AA',  # Greens for Phase II
                     '#8E44AD', '#9B59B6', '#D2B4DE',  # Purples for Phase III
                     '#E67E22', '#F39C12', '#F8C471']  # Oranges for Phase IV

    fig1 = px.timeline(df, x_start="Start", x_end="End", y="Task",
                       color="Phase",
                       hover_data=["Description", "Category", "Display_Start", "Display_End", "IsOngoing"],
                       color_discrete_sequence=custom_colors)

    # Add vertical lines for phase transitions with labels
    for phase, date in phase_transitions.items():
        # Add vertical line
        fig1.add_vline(x=date,
                       line_width=2,
                       line_dash="dash",
                       line_color="rgba(128, 128, 128, 0.3)")

        # Add phase label at the top
        fig1.add_annotation(
            x=date,
            y=1.02,  # Position above the plot
            yref="paper",
            text=f"{phase}",
            showarrow=False,
            font=dict(size=12, color="#2C3E50"),
            bordercolor="#2C3E50",
            borderwidth=1,
            borderpad=4,
            bgcolor="white",
            opacity=0.8
        )

    # Enhanced hover template
    fig1.update_traces(
        hovertemplate="<b>%{y}</b><br>" +
                      "<i>%{customdata[1]}</i><br>" +
                      "Start: %{customdata[2]}<br>" +
                      "Status: %{customdata[3]}<br>" +
                      "<br>%{customdata[0]}<extra></extra>"
    )

    # Customize x-axis ticks
    fig1.update_xaxes(
        ticktext=['Year 1\nQ1', 'Year 1\nQ2', 'Year 1\nQ3', 'Year 1\nQ4',
                  'Year 2\nQ1', 'Year 2\nQ2', 'Year 2\nQ3', 'Year 2\nQ4',
                  'Year 3\nQ1', 'Year 3\nQ2', 'Year 3\nQ3', 'Year 3\nQ4',
                  'Year 4\nQ1', 'Year 4\nQ2'],
        tickvals=[quarter_mapping[q] for q in quarter_mapping.keys()],
        tickangle=0,
        gridcolor='lightgray',
        linecolor='black'
    )

    # Enhanced layout
    fig1.update_layout(
        title=dict(
            text="<b>Pharmacy Technology Innovation Specialist</b><br><sup>Role Evolution & Ongoing Responsibilities</sup>",
            font=dict(size=24, family="Arial", color="#2C3E50"),
            x=0.5,
            xanchor='center',
            y=0.95
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=True,
        height=800,
        width=1600,
        font=dict(size=14, family="Arial", color="#2C3E50"),
        hoverlabel=dict(
            bgcolor="white",
            font_size=14,
            font_family="Arial"
        ),
        legend=dict(
            title="<b>Evolution Phases</b>",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(t=120, l=100, r=50, b=50)
    )

    # Add gridlines
    fig1.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')

    # Modified save section with better error handling and diagnostics
    def save_files(fig):
        print("\nStarting export process without legend...")

        try:
            html_path = os.path.abspath("pharmacy_role_timeline.html")

            # Update layout without legend
            fig.update_layout(
                title=dict(
                    text="<b>Pharmacy Technology Innovation Specialist</b><br><sup>Role Evolution & Ongoing Responsibilities</sup>",
                    font=dict(size=48, family="Arial", color="#2C3E50"),
                    x=0.5,
                    xanchor='center',
                    y=0.95
                ),
                width=3200,
                height=1600,
                font=dict(size=28, family="Arial", color="#2C3E50"),
                hoverlabel=dict(
                    bgcolor="white",
                    font_size=28,
                    font_family="Arial"
                ),
                showlegend=False,  # Remove legend
                margin=dict(t=240, l=200, r=100, b=100)
            )

            # Only keep phase marker annotations
            fig.layout.annotations = []
            for phase, date in phase_transitions.items():
                fig.add_annotation(
                    x=date,
                    y=1.05,
                    yref="paper",
                    text=f"<b>{phase}</b>",
                    showarrow=False,
                    font=dict(size=32, color="#2C3E50"),
                    bordercolor="#2C3E50",
                    borderwidth=2,
                    borderpad=8,
                    bgcolor="white",
                    opacity=0.9
                )

            fig.write_html(html_path)
            print("✓ HTML file saved successfully!")

            # Chrome setup
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--force-device-scale-factor=2')
            chrome_options.add_argument('--window-size=3400,2000')
            chrome_options.add_argument('--hide-scrollbars')

            driver = webdriver.Chrome(options=chrome_options)
            driver.set_window_size(3400, 2000)

            print("Loading visualization...")
            driver.get(f"file:///{html_path}")
            time.sleep(5)

            # Get the full content size
            total_width = driver.execute_script("return document.documentElement.scrollWidth")
            total_height = driver.execute_script("return document.documentElement.scrollHeight")
            driver.set_window_size(total_width, total_height)

            print("Capturing screenshot...")
            driver.save_screenshot("pharmacy_role_timeline_temp.png")

            # Image processing
            print("Processing image...")
            with Image.open("pharmacy_role_timeline_temp.png") as img:
                bbox = img.getbbox()
                img_cropped = img.crop(bbox)

                from PIL import ImageEnhance
                enhancer = ImageEnhance.Sharpness(img_cropped)
                img_sharp = enhancer.enhance(1.2)

                img_sharp.save("pharmacy_role_timeline.png",
                               "PNG",
                               quality=100,
                               optimize=False,
                               dpi=(300, 300))

            os.remove("pharmacy_role_timeline_temp.png")
            driver.quit()
            print("✓ High-resolution image saved successfully!")

        except Exception as e:
            print(f"Error during export: {str(e)}")
            if 'driver' in locals():
                driver.quit()

    # Call the save function with the figure
    save_files(fig1)


if __name__ == "__main__":
    create_visualizations()