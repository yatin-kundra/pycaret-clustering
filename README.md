# CSV File Processor

This Streamlit application processes uploaded CSV files and performs clustering analysis using various algorithms provided by the `pycaret` library. It evaluates clustering performance metrics such as Silhouette score, Calinski-Harabasz score, and Davies-Bouldin index for different preprocessing techniques including normalization, transformation, and PCA.

## Features

- Upload CSV files for clustering analysis.
- Perform clustering using K-means, Hierarchical clustering, and Mean shift clustering algorithms.
- Evaluate clustering performance metrics for different preprocessing techniques.
- Download clustering results as Excel or CSV files.

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/your-username/csv-file-processor.git
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the Streamlit app:

    ```bash
    streamlit run app.py
    ```

## Usage

1. Open the Streamlit application in your browser.
2. Upload a CSV file containing the data you want to analyze.
3. Select the clustering algorithm you want to use (K-means, Hierarchical clustering, or Mean shift clustering).
4. View the clustering performance metrics for different preprocessing techniques.
5. Download the clustering results in Excel or CSV format.

## Dependencies

- Python 3.x
- pandas
- pycaret
- streamlit

## Contributors

- [Yatin Kundra](https://github.com/your-username)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
