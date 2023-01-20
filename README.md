# NOAA-Weather-Records-ETL-Pipeline-with-AWS

## Objective
The objective of the project is to build an ETL pipeline with Amazon Kinesis. The National Oceanic and Atmospheric Administration (NOAA) Climate Data contains weather records in the US. In the project, the daily weather parameters in ”GHCND” data set including precipitation, snowfall, and min/max temperature, in Maryland state from October 1, 2021 to October 31, 2021 will be requested from NOAA Climate Data REST API. The records will be extract to a JSON file which contains the date/time, station, location, datatype, and value information. The records will be insert to AWS Kinesis by a EC2 producer and retrieved by a Lambda consumer. The Lambda consumer will remove records from Kinesis, and send the records to two DynamoDB tables, Precipitation table and Temperature table, based on the datatype in the records. The information in the DynamoDB table will include the timestamp, the weather station, and the value. The information in DynamoDB can be retrieved by location, and sorted by timestamp value.
![Request](https://user-images.githubusercontent.com/80618804/213613425-a391b36f-c29e-4728-bbb0-2f27ad464930.png)


## Files
The report.pdf file contains the AWS resource introduction and instructions to build the AWS architecture.  
The ec2_bash_code.sh is used to ssh into the ec2 instance, install required library, and run the ec2_producer_code.py.  
The ec2_producer_code.py contains the code to request NOAA REST API data, parse the JSON file, and extract the desire information.  
The lambda_consumer_code.py contains the code to get records in Kinesis Data Steam and insert them to DynamoDB.
