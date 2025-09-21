import pandas as pd
import re
from typing import Tuple, Optional
import openai
from openai import OpenAI
import time
import logging
import os
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TelegramDataTransformer:
    def __init__(self, csv_file_path: str, openai_api_key: Optional[str] = None):
        """
        Initialize the data transformer
        
        Args:
            csv_file_path (str): Path to the CSV file
            openai_api_key (str, optional): OpenAI API key for generating summaries
        """
        self.csv_file_path = csv_file_path
        self.openai_client = None
        
        # Initialize OpenAI client if API key is provided
        if openai_api_key:
            self.openai_client = OpenAI(api_key=openai_api_key)
        
        # Define topic mappings based on Pre-data notes.txt
        self.topic_mappings = {
            '#studies✍🏼': 'studies',
            '#advice🗣️': 'advice', 
            '#random✨': 'random',
            '#love❤️': 'love',
            '#campus🏛': 'campus',
            '#rant🤬': 'rant'
        }
        
        # Post-text pattern to remove
        self.post_text_pattern = r'#[A-Z]\d{8}\s*\|\s*SMU Confess Channel.*$'
        
    def extract_topic_and_clean_text(self, text: str) -> Tuple[str, str]:
        """
        Extract topic from text and clean the main content
        
        Args:
            text (str): Original text from CSV
            
        Returns:
            Tuple[str, str]: (topic, cleaned_text)
        """
        # Extract topic (hashtag at the beginning)
        topic_match = re.match(r'^(#\w+[^\s]*)', text)
        topic = 'unknown'
        
        if topic_match:
            topic_tag = topic_match.group(1)
            # Map to predefined topics or use the tag itself
            topic = self.topic_mappings.get(topic_tag, topic_tag.replace('#', ''))
        
        # Remove topic from the beginning
        cleaned_text = re.sub(r'^#\w+[^\s]*\s*', '', text)
        
        # Remove post-text from the end
        cleaned_text = re.sub(self.post_text_pattern, '', cleaned_text, flags=re.MULTILINE)
        
        # Clean up extra whitespace
        cleaned_text = cleaned_text.strip()
        
        return topic, cleaned_text
    
    def generate_summary_openai(self, text: str, max_retries: int = 3) -> str:
        """
        Generate AI summary using OpenAI API
        
        Args:
            text (str): Text to summarize
            max_retries (int): Maximum number of retry attempts
            
        Returns:
            str: Generated summary
        """
        if not self.openai_client:
            return "AI summary unavailable - no API key provided"
        
        for attempt in range(max_retries):
            try:
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that creates concise summaries of social media posts. Keep summaries to 1-2 sentences and focus on the main point or sentiment."},
                        {"role": "user", "content": f"Please provide a brief summary of this confession post: {text}"}
                    ],
                    max_tokens=100,
                    temperature=0.7
                )
                return response.choices[0].message.content.strip()
                
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logger.error(f"Failed to generate summary after {max_retries} attempts")
                    return f"Summary generation failed: {str(e)}"
    
    def generate_summary_simple(self, text: str) -> str:
        """
        Generate a simple rule-based summary (fallback when no AI available)
        
        Args:
            text (str): Text to summarize
            
        Returns:
            str: Generated summary
        """
        # Simple extractive summary - take first sentence or first 100 characters
        sentences = re.split(r'[.!?]+', text)
        if sentences and len(sentences[0].strip()) > 10:
            first_sentence = sentences[0].strip()
            if len(first_sentence) > 100:
                return first_sentence[:97] + "..."
            return first_sentence
        else:
            # Fallback to first 100 characters
            return text[:97] + "..." if len(text) > 100 else text
    
    def handle_existing_output_file(self, output_file: str) -> str:
        """
        Handle existing output file by creating backup or asking user preference
        
        Args:
            output_file (str): Path to the output file
            
        Returns:
            str: Final output file path to use
        """
        if not os.path.exists(output_file):
            return output_file
        
        logger.warning(f"Output file already exists: {output_file}")
        
        # Create backup filename with timestamp
        base_name, ext = os.path.splitext(output_file)
        timestamp = datetime.now().strftime("%Y%m%d_%I%M%S%p")
        backup_file = f"{base_name}_backup_{timestamp}{ext}"
        
        try:
            # Rename existing file to backup
            os.rename(output_file, backup_file)
            logger.info(f"Existing file backed up as: {backup_file}")
            return output_file
        except OSError as e:
            # If backup fails, create new file with timestamp
            new_output_file = f"{base_name}_{timestamp}{ext}"
            logger.info(f"Could not backup existing file. Using new filename: {new_output_file}")
            return new_output_file

    def transform_data(self, use_ai_summary: bool = True, output_file: Optional[str] = None) -> pd.DataFrame:
        """
        Transform the CSV data according to requirements
        
        Args:
            use_ai_summary (bool): Whether to use AI for summary generation
            output_file (str, optional): Path to save the transformed data
            
        Returns:
            pd.DataFrame: Transformed dataframe
        """
        logger.info(f"Loading data from {self.csv_file_path}")
        
        # Check if input file exists
        if not os.path.exists(self.csv_file_path):
            raise FileNotFoundError(f"Input file not found: {self.csv_file_path}")
        
        # Load the CSV file
        try:
            df = pd.read_csv(self.csv_file_path)
            logger.info(f"Loaded {len(df)} rows")
        except Exception as e:
            logger.error(f"Error loading CSV file: {e}")
            raise
        
        # Initialize new columns
        df['topic'] = ''
        df['summary'] = ''
        df['cleaned_text'] = ''
        
        # Process each row
        for index, row in df.iterrows():
            if index % 100 == 0:
                logger.info(f"Processing row {index + 1}/{len(df)}")
            
            text = str(row['text'])
            
            # Extract topic and clean text
            topic, cleaned_text = self.extract_topic_and_clean_text(text)
            
            # Generate summary
            if use_ai_summary and self.openai_client:
                summary = self.generate_summary_openai(cleaned_text)
            else:
                summary = self.generate_summary_simple(cleaned_text)
            
            # Update dataframe
            df.at[index, 'topic'] = topic
            df.at[index, 'summary'] = summary
            df.at[index, 'cleaned_text'] = cleaned_text
        
        # Replace the original text column with cleaned text
        df['text'] = df['cleaned_text']
        df = df.drop('cleaned_text', axis=1)
        
        # Reorder columns
        df = df[['post_id', 'timestamp', 'topic', 'summary', 'text']]
        
        # Save to file if specified
        if output_file:
            try:
                # Handle existing output file
                final_output_file = self.handle_existing_output_file(output_file)
                df.to_csv(final_output_file, index=False)
                logger.info(f"Transformed data saved to {final_output_file}")
            except Exception as e:
                logger.error(f"Error saving output file: {e}")
                # Try to save with timestamp as fallback
                base_name, ext = os.path.splitext(output_file)
                timestamp = datetime.now().strftime("%Y%m%d_%I%M%S%p")
                fallback_file = f"{base_name}_emergency_{timestamp}{ext}"
                try:
                    df.to_csv(fallback_file, index=False)
                    logger.info(f"Saved to fallback file: {fallback_file}")
                except Exception as e2:
                    logger.error(f"Failed to save even to fallback file: {e2}")
                    raise
        
        logger.info("Data transformation completed successfully")
        return df
    
    def preview_transformation(self, num_rows: int = 5) -> None:
        """
        Preview the transformation on a few rows
        
        Args:
            num_rows (int): Number of rows to preview
        """
        logger.info(f"Previewing transformation on first {num_rows} rows")
        
        # Check if input file exists
        if not os.path.exists(self.csv_file_path):
            logger.error(f"Input file not found: {self.csv_file_path}")
            return
        
        try:
            df = pd.read_csv(self.csv_file_path)
            df_preview = df.head(num_rows)
        except Exception as e:
            logger.error(f"Error loading CSV file for preview: {e}")
            return
        
        print("=== ORIGINAL DATA ===")
        for index, row in df_preview.iterrows():
            print(f"\nRow {index + 1}:")
            print(f"Text: {row['text']}")
            
        print("\n=== TRANSFORMED DATA ===")
        for index, row in df_preview.iterrows():
            text = str(row['text'])
            topic, cleaned_text = self.extract_topic_and_clean_text(text)
            summary = self.generate_summary_simple(cleaned_text)
            
            print(f"\nRow {index + 1}:")
            print(f"Topic: {topic}")
            print(f"Summary: {summary}")
            print(f"Cleaned Text: {cleaned_text[:200]}...")

def main():
    """
    Main function to run the data transformation
    """
    # File paths
    input_file = r"c:\Users\Admin\Desktop\Personal Folder\University\SMU\2. SMU Academic Modules\2025-2026 Y4Term1\IS483 Project Experience (Applications)\Data Collection\15June Analysis\Telegram\Telegram - SMU Confess - Posts.csv"
    output_file = r"c:\Users\Admin\Desktop\Personal Folder\University\SMU\2. SMU Academic Modules\2025-2026 Y4Term1\IS483 Project Experience (Applications)\Data Collection\15June Analysis\Telegram\Telegram - SMU Confess - Posts_Transformed.csv"
    
    try:
        # Initialize transformer
        # For AI summaries, provide your OpenAI API key:
        # transformer = TelegramDataTransformer(input_file, openai_api_key="your-api-key-here")
        transformer = TelegramDataTransformer(input_file)
        
        print("=== DATA TRANSFORMATION PREVIEW ===")
        transformer.preview_transformation()
        
        print("\n=== STARTING FULL TRANSFORMATION ===")
        # Transform the data (set use_ai_summary=True if you have OpenAI API key)
        transformed_df = transformer.transform_data(use_ai_summary=False, output_file=output_file)
        
        print(f"\n=== TRANSFORMATION COMPLETE ===")
        print(f"Transformed {len(transformed_df)} rows")
        print(f"Output saved successfully")
        
        # Display statistics
        print(f"\n=== TOPIC DISTRIBUTION ===")
        print(transformed_df['topic'].value_counts())
        
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        print("Please ensure the input CSV file exists in the correct location.")
    except Exception as e:
        print(f"ERROR: An unexpected error occurred: {e}")
        logger.error(f"Unexpected error in main: {e}", exc_info=True)

if __name__ == "__main__":
    main()