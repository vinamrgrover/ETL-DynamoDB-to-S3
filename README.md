# Batch ETL Pipeline - NoSQL

## Architecture Diagram

![NoSQL_ETL drawio](https://github.com/vinamrgrover/ETL-DynamoDB-to-S3/assets/100070155/66479527-05e8-40e6-9325-0783b9d40359)


## Description

This project is based on a Batch ETL Pipeline built on AWS

+ First, the Data is extracted using Lambda Function ***(API_Extract.py)*** from  a Mock Data API
+ The Data is then transformed using Pandas and loaded into a DynamoDB Table
+ A Glue ETL Job ***(DynamoDB_to_S3.py)*** is set up to crawl the Data from DynamoDB Table apply necessary filter transformations and write the Data to an S3 Bucket as Parquet file with appropriate Partitions
+ The ETL Pipeline runs every hour and this process is automated by a CloudWatch Event Rule

**Note : A Mock Data API is required to perform this project. 
You can create your own Mock Data API here : https://www.mockaroo.com**

## Workflow


1. A Lambda Function *(API_Extract)* is created to extract data from a mock data API. The function's runtime set to Python 3.9.

<img width="865" alt="Screenshot 2023-06-15 at 9 22 33 PM" src="https://github.com/vinamrgrover/ETL-DynamoDB-to-S3/assets/100070155/86522afc-571f-497d-aabd-f199cb7d6aa2">


The API Key is set as an Environment Variable under the Lambda Function's Settings. 



2. The Data is then transformed using Pandas and loaded into a DynamoDB Table *(Flowers)*.
The Transformed Data can be seen by clicking on the **Explore Items** Tab in the DynamoDB Console. 


<img width="996" alt="Screenshot 2023-06-15 at 9 30 21 PM" src="https://github.com/vinamrgrover/ETL-DynamoDB-to-S3/assets/100070155/0d0e8db9-e4c0-42d4-826e-8582cdd39466">


3. A Glue Crawler is created to crawl the DynamoDB Table. Then, a Glue ETL Job is set up to apply Filter Transformations and load the Data into an S3 Bucket, partitioned by column - *color*.

Here's the Transformed Data in an **S3 Bucket** : 

<img width="1127" alt="Screenshot 2023-06-16 at 3 33 37 PM" src="https://github.com/vinamrgrover/ETL-DynamoDB-to-S3/assets/100070155/10047dff-567d-4946-8ac9-5528cce0e079">

## Automation

The ETL Pipeline runs every hour and scheduled by a CloudWatch Events Rule

Here's the Cron Expression that triggers the Lambda Function every hour -  ```0 * * * ? *```


## Incremental ETL

The ```check_datetime()``` function of the Glue ETL Job's Script *(DynamoDB_to_S3.py)*, is used to Filter out the most recent rows in the DynamicFrame. 

This function compares the current day, month, year and hour to the DynamicFrame's **created_at** column and filters out the rows that are updated in the current hour.


