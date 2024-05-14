# EEET2574-RMIT-Big-Data-for-Engineering

# Big Data Processing and Analytics Project

## Overview

This project demonstrates a seamless integration of AWS services to create a comprehensive big data solution. It combines real-time data processing using AWS Kinesis and MongoDB with advanced analytics and visualization through SageMaker and QuickSight. The solution efficiently processes both online and offline data, providing valuable insights into various datasets.

## Solution Design

![solution design](<solution design.png>)

## Project Structure

- **Assignment3.ipynb**
  - Contains code related to the third assignment, likely featuring SageMaker and QuickSight implementations.

- **ETL.ipynb**
  - Includes code related to Extract, Transform, Load (ETL) operations, potentially integrating SageMaker and QuickSight functionalities.

- **README.md**
  - Documentation file providing an overview of the project, its structure, and instructions for usage.

- **aws-quicksight-manifest-historical-data.json**
  - JSON file with manifest data for historical data used in QuickSight.

- **aws-quicksight-manifest-prediction-data.json**
  - JSON file with manifest data for prediction data used in QuickSight.

- **get-data-from-mongo.py**
  - Python script for extracting data from MongoDB.

- **getdata.ipynb**
  - Jupyter notebook containing code for obtaining data, potentially integrating with SageMaker and QuickSight.

- **online/**
  - Folder containing files related to the online data processing flow.

    - **consumer.py**
      - Python script (consumer) for handling data consumption, updating file structure.

    - **producer.py**
      - Python script (producer) for generating or sending data, updating file structure.

    - **requirements.txt**
      - Text file listing project dependencies.

## Data Processing Flow

### Online Flow

- Starting with the OpenWeatherMap API, real-time weather predictions for the next two days are gathered.

- AWS Kinesis acts as a data buffer, streaming this information to an EC2 instance.

- The data is efficiently stored in MongoDB on the EC2 instance.

### Offline Flow

- Two historical datasets from Kaggle converge in AWS S3, providing a scalable storage solution.

- AWS SageMaker performs advanced analytics, handling data cleaning, preprocessing, and machine learning model development.

- The cleaned and processed data resides in a separate S3 bucket.

### Visualization and Business Intelligence

- AWS QuickSight connects to the cleaned data in S3, enabling the creation of insightful dashboards and reports.

## Security and Efficiency Measures

- AWS IAM is implemented for user management, ensuring security.

- AWS Budgets help control spending, ensuring financial efficiency.

- AWS CloudWatch monitors resource performance, triggering alerts for anomalies.

## Accessing Insights

Clients can access valuable insights through QuickSight, providing a user-friendly interface for exploring and understanding the data.

## How to Use

1. Clone the repository:
   ```bash
   git clone https://github.com/vananh30/asm3_bigdata.git 
   ```

2. Install dependencies:
   ```bash
   # Navigate to project directory
   cd asm3_bigdata/online
   # Install dependencies
   pip install -r requirements.txt
   ```

3. Execute the relevant scripts and notebooks based on your requirements.

## References

- [AWS Kinesis Documentation](https://docs.aws.amazon.com/kinesis/index.html)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [AWS SageMaker Documentation](https://docs.aws.amazon.com/sagemaker/index.html)
- [AWS QuickSight Documentation](https://docs.aws.amazon.com/quicksight/index.html)

Feel free to customize this README based on the specifics of your project and provide more detailed instructions if needed.