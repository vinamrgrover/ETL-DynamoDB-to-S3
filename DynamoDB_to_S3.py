import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
import re
from datetime import datetime

def check_datetime(datetime_string : str) -> bool:
    return datetime.strftime(datetime.now(), '%Y-%m-%d %H') == datetime_string
    
args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

source_node = glueContext.create_dynamic_frame.from_catalog(
    database = "nosql_crawl_db",
    table_name = "flowers",
    transformation_ctx = "source_node"
)

# Filter Transformations

filter_node = Filter.apply(
    frame = source_node,
    f = lambda row : check_datetime(row['created_at']),
    transformation_ctx = 'filter_node_1'
)

filter_node = Filter.apply(
    frame = filter_node,
    f = lambda row : not (bool(re.match("undefined", row["color"]))),
    transformation_ctx = "filter_node_2"
)

filter_node = Filter.apply(
    frame = filter_node,
    f = lambda row : not (row['quantity'] == None),
    transformation_ctx = "filter_node_3"
)

filter_node = filter_node.drop_fields(['created_at'])

target_node = glueContext.write_dynamic_frame.from_options(
    frame = filter_node,
    connection_type = "s3",
    format = "glueparquet",
    connection_options = {
        "path": "s3://dynamodb-flowers-bucket/transformed/",
        "partitionKeys": ["color"]
    },
    format_options = {"compression": "snappy"},
    transformation_ctx = "target_node"
)

job.commit()

