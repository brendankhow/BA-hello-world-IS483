# Telegram Data Transformer

A Python script to transform SMU Confess Telegram channel data by extracting topics, cleaning text content, and generating summaries from confession posts.

## What it does

This tool processes CSV data from Telegram posts and performs the following transformations:

1. **Topic Extraction**: Extracts topic categories from hashtags at the beginning of each post
2. **Text Cleaning**: Removes pre-text hashtags and post-text metadata to isolate the main content
3. **Summary Generation**: Creates concise summaries of each post using either AI (OpenAI) or rule-based methods
4. **Data Restructuring**: Outputs a clean CSV with organized columns: `post_id`, `timestamp`, `topic`, `summary`, `text`

### Supported Topics

The script recognizes the following topic categories:

-   `#studies✍🏼` → studies
-   `#advice🗣️` → advice
-   `#random✨` → random
-   `#love❤️` → love
-   `#campus🏛` → campus
-   `#rant🤬` → rant

## Project Structure

```
Telegram/
├── data transformer.py          # Main transformation script
├── Pre-data notes.txt          # Topic format documentation
├── Telegram - SMU Confess - Posts.csv    # Original data file
├── Telegram - SMU Confess - Posts_Transformed.csv  # Output file (generated)
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── .venv/                     # Virtual environment (created during setup)
```

## First-Time Setup

### Prerequisites

-   Python 3.7 or higher
-   Windows PowerShell (for the setup commands below)

### Step 1: Clone or Download the Project

Ensure you have all the project files in your working directory.

### Step 2: Set up Python Virtual Environment

1. Open PowerShell and navigate to the project directory:

```powershell
cd "path\to\your\telegram\project"
```

2. Create a virtual environment:

```powershell
python -m venv .venv
```

3. Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 3: Install Required Dependencies

Install the required Python packages using the requirements file:

```powershell
pip install -r requirements.txt
```

Alternatively, you can install packages individually:

```powershell
pip install pandas openai
```

### Step 4: Configure the Script (Optional)

If you want to use AI-powered summaries, you'll need an OpenAI API key:

1. Get an API key from [OpenAI](https://platform.openai.com/api-keys)
2. Edit the `main()` function in `data transformer.py`:

```python
# Replace this line:
transformer = TelegramDataTransformer(input_file)

# With this line (insert your actual API key):
transformer = TelegramDataTransformer(input_file, openai_api_key="your-api-key-here")
```

3. Change `use_ai_summary=False` to `use_ai_summary=True` in the `transform_data()` call

## Usage

### Running the Transformation

With the virtual environment activated, run the script:

```powershell
python "data transformer.py"
```

### What the Script Does

1. **Preview Mode**: Shows a preview of how the first 5 rows will be transformed
2. **Full Transformation**: Processes all rows in the CSV file
3. **Output Generation**: Creates a new file `Telegram - SMU Confess - Posts_Transformed.csv`
4. **File Management**: Automatically handles existing output files by creating backups
5. **Statistics Display**: Shows the distribution of topics found in the data

### Output Format

The transformed CSV will have the following columns:

-   `post_id`: Original post ID
-   `timestamp`: Original timestamp
-   `topic`: Extracted topic category (studies, advice, random, etc.)
-   `summary`: AI or rule-based summary of the post content
-   `text`: Cleaned text with hashtags and metadata removed

## Configuration Options

### Summary Generation Methods

The script supports two summary generation methods:

1. **AI Summaries** (requires OpenAI API key):

    - More intelligent and context-aware summaries
    - Uses GPT-3.5-turbo model
    - Costs money per API call
    - Set `use_ai_summary=True`

2. **Rule-based Summaries** (default):
    - Free and fast
    - Uses the first sentence or first 100 characters
    - Set `use_ai_summary=False`

### File Paths

You can modify the input and output file paths in the `main()` function:

```python
input_file = r"path\to\your\input\file.csv"
output_file = r"path\to\your\output\file.csv"
```

## Troubleshooting

### Common Issues

1. **Module not found errors**: Make sure you've activated the virtual environment and installed dependencies
2. **File path errors**: Ensure the CSV file exists and the path is correct
3. **Permission errors**: Make sure you have write permissions in the output directory
4. **OpenAI API errors**: Check your API key and ensure you have sufficient credits
5. **Output file already exists**: The script automatically creates backups of existing files with timestamps

### File Handling Features

The script includes robust file handling:

-   **Automatic Backup**: If the output file already exists, it's automatically renamed with a timestamp backup
-   **Fallback Saving**: If the primary save location fails, the script tries alternative filenames
-   **Error Recovery**: Comprehensive error handling for file operations

### Virtual Environment Issues

If you encounter issues with the virtual environment:

```powershell
# Deactivate current environment
deactivate

# Remove and recreate the virtual environment
Remove-Item -Recurse -Force .venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Memory Issues with Large Files

For very large CSV files, you might want to process data in chunks. The script includes progress logging every 100 rows to help monitor processing.

## Sample Usage Example

```powershell
# Navigate to project directory
cd "path\to\your\telegram\project"

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run the transformation
python "data transformer.py"
```

Expected output:

```
=== DATA TRANSFORMATION PREVIEW ===
2025-09-05 10:30:00,000 - INFO - Previewing transformation on first 5 rows

=== ORIGINAL DATA ===
Row 1:
Text: #studies✍🏼  Y1S1: CS1101S Programming Methodology...

=== TRANSFORMED DATA ===
Row 1:
Topic: studies
Summary: Student shares detailed study plan for DDP CS and Math program
Cleaned Text: Y1S1: CS1101S Programming Methodology...

=== STARTING FULL TRANSFORMATION ===
2025-09-05 10:30:01,000 - INFO - Loading data from input file
2025-09-05 10:30:01,100 - INFO - Loaded 1000 rows
...
```

## Contributing

Feel free to modify the script for your specific needs:

-   Add new topic categories to `topic_mappings`
-   Improve the regex patterns for better text cleaning
-   Enhance the rule-based summary generation logic
-   Add additional output formats

## License

This project is for academic/research purposes as part of the IS483 Project Experience course at SMU.
