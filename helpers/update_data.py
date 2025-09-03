import requests
import os
from datetime import datetime

def get_csv_files_from_github():
    """Get list of CSV files from GitHub API"""
    api_url = "https://api.github.com/repos/GuySchnidrig/ManaCore/contents/data/processed"
    
    try:
        response = requests.get(api_url, timeout=30)
        response.raise_for_status()
        files = response.json()
        
        # Filter for CSV files only
        csv_files = [file['name'] for file in files if file['name'].endswith('.csv')]
        return csv_files
        
    except Exception as e:
        print(f"Failed to get file list: {e}")
        return []

def download_data():
    base_url = "https://raw.githubusercontent.com/GuySchnidrig/ManaCore/main/data/processed/"
    data_dir = "/home/GuySchnidrig/mysite/data/" 
     # use only locally 
    data_dir = "G:/My Drive/MTG/ManaDash/data"
    
    # Get CSV files dynamically
    csv_files = get_csv_files_from_github()
    
    if not csv_files:
        print("No CSV files found or API call failed")
        return
    
    print(f"Found {len(csv_files)} CSV files")
    os.makedirs(data_dir, exist_ok=True)
    
    success_count = 0
    for file in csv_files:
        try:
            url = f"{base_url}{file}"
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            with open(f"{data_dir}/{file}", 'wb') as f:
                f.write(response.content)
                
            print(f"Downloaded {file}")
            success_count += 1
            
        except Exception as e:
            print(f"Failed to download {file}: {e}")
    
    print(f"Data update completed at {datetime.now()}")
    print(f"Successfully downloaded {success_count}/{len(csv_files)} files")

if __name__ == "__main__":
    download_data()