# Youth Mental Well-being EDA Project

This project explores social media data (Instagram, Reddit, Telegram) to uncover insights related to mental well-being in youths. The analysis is performed in a Jupyter Notebook using Python data science libraries.

## Tech Stack

### **Programming Language**

-   **Python 3.8+**: Core programming language for data analysis

### **Data Analysis Libraries**

-   **pandas**: Data manipulation and analysis
-   **numpy**: Numerical computing and array operations
-   **matplotlib**: Data visualization and plotting
-   **seaborn**: Statistical data visualization

### **Development Environment**

-   **Jupyter Notebook**: Interactive computing environment
-   **VS Code** (optional): Code editor with Jupyter support

### **Data Sources**

-   **CSV files**: Social media data from Instagram, Reddit, and Telegram
-   **Platform APIs**: Data collected from social media platforms

### **Analysis Techniques**

-   **Exploratory Data Analysis (EDA)**: Statistical summaries and data exploration
-   **Keyword Analysis**: Mental health term frequency analysis
-   **Time Series Analysis**: Temporal patterns and trends
-   **Correlation Analysis**: Relationship identification between variables
-   **Data Visualization**: Charts, heatmaps, and interactive plots

## Project Structure

-   `Youth_Mental_Wellbeing_EDA.ipynb`: Main notebook for exploratory data analysis (EDA).
-   `data sources/`: Folder containing the three CSV data sources.
-   `requirements.txt`: List of required Python packages.

## Setup Instructions

1. **Install Python**

    - Download and install Python 3.8 or newer from [python.org](https://www.python.org/downloads/).

2. **Create a Virtual Environment (Recommended)**

    - Open a terminal in this project folder.
    - Run:
        ```
        python -m venv venv
        venv\Scripts\activate  # On Windows
        # or
        source venv/bin/activate  # On Mac/Linux
        ```

3. **Install Required Packages**

    - With the virtual environment activated, run:
        ```
        pip install -r requirements.txt
        ```

4. **Start Jupyter Notebook**
    - Run:
        ```
        jupyter notebook
        ```
    - Open `Youth_Mental_Wellbeing_EDA.ipynb` in your browser.

## Notes

-   Make sure the `data sources` folder is in the same directory as the notebook.
-   If you encounter missing package errors, re-run the install command above.
-   The notebook is structured to guide you through data loading, cleaning, EDA, and insight generation.

## About

This project is for exploring mental well-being in youths using real-world social media data. You are encouraged to extend the analysis with NLP, sentiment analysis, or other advanced techniques as needed.
