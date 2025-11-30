#!/usr/bin/env python3
"""
Test samples for the AI Data Pipeline Design Assistant
"""

# Sample pipeline descriptions for testing
SAMPLE_DESCRIPTIONS = {
    "azure_batch": {
        "name": "Azure Batch ETL with Delta Lake",
        "description": "I have CSV files landing in Azure Blob (~200GB/day) and want to build a bronze-silver-gold Delta Lake in Azure Databricks and expose curated tables to Power BI. Daily batch is fine, there is customer PII like email and phone."
    },
    
    "aws_streaming": {
        "name": "AWS Streaming Pipeline",
        "description": "Design a real-time data pipeline for IoT sensor data. We have 10,000 sensors sending JSON data every second to AWS Kinesis. Need to process streams in real-time using AWS Glue Streaming, store processed data in S3, and enable analytics with Athena. Data includes temperature, humidity, and location."
    },
    
    "hybrid_cloud": {
        "name": "Hybrid Cloud Data Warehouse",
        "description": "We have on-premise Oracle databases with sales data and want to replicate to cloud for analytics. Looking for a solution that works with both AWS and Azure. Need daily sync of ~500GB data, with data warehouse capabilities and ML model training. Sensitive financial data requires strong security."
    },
    
    "gcp_bigquery": {
        "name": "GCP BigQuery Analytics Pipeline", 
        "description": "Build a data pipeline for e-commerce analytics using Google Cloud Platform. Source data comes from Shopify API, Google Analytics, and on-premise inventory system. Need to load into BigQuery with daily incremental updates (~100GB/day). Enable real-time dashboards and ML predictions for customer behavior."
    },
    
    "kafka_spark": {
        "name": "Kafka + Spark Structured Streaming",
        "description": "Create a streaming analytics pipeline using Apache Kafka and Spark Structured Streaming. We have application logs flowing into Kafka topics at ~5000 messages/second. Need to process streams for real-time fraud detection, aggregate metrics, and store results in both real-time database (Redis) and data lake (S3) for historical analysis."
    },
    
    "data_lakehouse": {
        "name": "Modern Data Lakehouse",
        "description": "Design a data lakehouse architecture for a healthcare organization. Need to ingest EHR data from multiple hospitals (~1TB/day), ensure HIPAA compliance, perform data quality checks, and enable both SQL analytics and ML workflows. Looking for open-source solutions with Delta Lake, Apache Iceberg, or similar technologies."
    },
    
    "etl_testing": {
        "name": "ETL Testing Framework",
        "description": "Create a comprehensive ETL testing framework for data quality validation. Need to validate data completeness, accuracy, consistency, and referential integrity across multiple data sources including SQL Server, MongoDB, and flat files. Should include automated testing, data profiling, and reporting capabilities."
    }
}

def get_sample_descriptions():
    """Return all sample descriptions as a list"""
    return [sample["description"] for sample in SAMPLE_DESCRIPTIONS.values()]

def get_sample_by_name(name):
    """Get a specific sample by name"""
    return SAMPLE_DESCRIPTIONS.get(name, {}).get("description", "")

def print_all_samples():
    """Print all available test samples"""
    print("Available test samples for AI Data Pipeline Design Assistant:")
    print("=" * 60)
    for key, sample in SAMPLE_DESCRIPTIONS.items():
        print(f"\n{sample['name']} ({key}):")
        print(f"Description: {sample['description']}")
        print("-" * 60)

if __name__ == "__main__":
    print_all_samples()