# Batch ETL Pipeline - NoSQL

## Description

This project is based on a Batch ETL Pipeline built on AWS

+ First, the Data is extracted using Lambda Function ***(API_Extract)*** from  a Mock Data API
+ The Data is then transformed using Pandas and loaded into a DynamoDB Table
+ A Glue ETL Job is set up to crawl the Data from DynamoDB Table apply necessary filter transformations and write the Data to an S3 Bucket as Parquet file with appropriate Partitions
+ The ETL Pipeline runs every hour and this process is automated by a CloudWatch Event Rule

## Workflow


1. A Lambda Function *(API_Extract)* is created to extract data from a mock data API. The function's runtime set to Python 3.9.

<img width="865" alt="Screenshot 2023-06-15 at 9 22 33 PM" src="https://github.com/vinamrgrover/ETL-DynamoDB-to-S3/assets/100070155/86522afc-571f-497d-aabd-f199cb7d6aa2">


The API Key is set as an Environment Variable under the Lambda Function's Settings. 



2. The Data is then transformed using Pandas and loaded into a DynamoDB Table *(Flowers)*.
The Transformed Data can be seen by clicking on the **Explore Items** Tab in the DynamoDB Console. 


<img width="996" alt="Screenshot 2023-06-15 at 9 30 21 PM" src="https://github.com/vinamrgrover/ETL-DynamoDB-to-S3/assets/100070155/0d0e8db9-e4c0-42d4-826e-8582cdd39466">
