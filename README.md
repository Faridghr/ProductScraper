# ProductScraper
This Python project scrapes product information from the Digikala e-commerce website to extract details about available laptops, such as price, model, CPU, GPU, RAM, screen size, etc. The extracted data is stored in a MySQL database using the mysql library. Additionally, the project includes a simple machine learning model built with scikit-learn for predicting laptop prices based on user input configurations.

## Features
- **Web Scraping:** Scrapes product information from Digikala's laptop category.
- **Data Extraction:** Collects details like price, model, CPU, GPU, RAM, screen size, etc., from each laptop listing.
- **Database Storage:** Stores the extracted data in a MySQL database.
- **Machine Learning Model:** Develops a simple price prediction model based on laptop configurations.

## How It Works
1. **Find Number of Pages:** Determines the number of pages available for the laptop category on the Digikala website.
2. **Loop and Extract Links:** Iterates through each page, extracting links to individual laptop listings.
3. **Retrieve and Collect Data:** Requests each laptop's URL and collects desired information.
4. **Decode and Store:** Decodes the extracted information and stores it in a MySQL database.
5. **Model Creation:** Builds a machine learning model using scikit-learn to predict laptop prices based on user-specified configurations.

## Requirements
- Python 3
- Requests library
- BeautifulSoup library
- mysql library
- scikit-learn library
- MySQL database

## Usage
1. Clone the repository: git clone `https://github.com/Faridghr/ProductScraper.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Set up MySQL database and configure connection settings.
4. Run the main script to scrape data and store it in the database: `python src/ProductScraper.py`