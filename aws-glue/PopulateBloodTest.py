import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Script generated for node s3_Blood_Test
s3_Blood_Test_node1732696342624 = glueContext.create_dynamic_frame.from_catalog(database="healthcare", table_name="bloodtest", transformation_ctx="s3_Blood_Test_node1732696342624")

# Script generated for node Arora_Blood_Test_Insert
Arora_Blood_Test_Insert_node1732696929373 = glueContext.write_dynamic_frame.from_catalog(frame=s3_Blood_Test_node1732696342624, database="aroradb", table_name="healthcare_blood_test", transformation_ctx="Arora_Blood_Test_Insert_node1732696929373")

job.commit()