import os
import re
from googletrans import Translator
import time
import logging

# Configuration
DIRECTORY_PATH = "videos"
SOURCE_LANG = "auto" 
TARGET_LANG = "en" 

def clean_filename(filename):
    """Remove invalid characters from filename"""
    # Replace invalid characters with underscores
    cleaned = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove multiple underscores
    cleaned = re.sub(r'_{2,}', '_', cleaned)
    return cleaned.strip('_')

def translate_filename(translator, filepath):
    """Translate a single file"""
    filename = os.path.basename(filepath)
    name, ext = os.path.splitext(filename)
    
    # Skip if filename is too short or only numbers/symbols
    if len(name) < 2 or re.match(r'^[0-9\W_]+$', name):
        return None
    
    try:
        # Translate the filename
        result = translator.translate(name, src=SOURCE_LANG, dest=TARGET_LANG)
        translated_name = result.text
        
        # Create new filepath
        directory = os.path.dirname(filepath)
        new_filepath = os.path.join(directory, translated_name + ext)
        
        return new_filepath
    except Exception as e:
        print(f"Failed to translate: {filename} - {e}")
        return None

def main():
    # Initialize translator
    translator = Translator()
    
    # Get all files in directory
    for root, dirs, files in os.walk(DIRECTORY_PATH):
        for filename in files:
            filepath = os.path.join(root, filename)
            
            # Skip hidden files
            if filename.startswith('.'):
                continue
            
            new_filepath = translate_filename(translator, filepath)
            
            if new_filepath and new_filepath != filepath:
                # Check if target file already exists
                if os.path.exists(new_filepath):
                    print(f"SKIP (exists): {filename}")
                    continue
                
                print(f"Renaming: {filename} -> {os.path.basename(new_filepath)}")
                os.rename(filepath, new_filepath)
                
                # Small delay to avoid rate limiting
                time.sleep(0.1)

if __name__ == "__main__":
    main()