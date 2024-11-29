import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue import DynamicFrame

def sparkSqlQuery(glueContext, query, mapping, transformation_ctx) -> DynamicFrame:
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql(query)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Script generated for node s3_diagnosis
s3_diagnosis_node1732703477279 = glueContext.create_dynamic_frame.from_catalog(database="healthcare", table_name="diagnosis", transformation_ctx="s3_diagnosis_node1732703477279")

# Script generated for node s3_general_body_test
s3_general_body_test_node1732703754281 = glueContext.create_dynamic_frame.from_catalog(database="healthcare", table_name="generalbodytest", transformation_ctx="s3_general_body_test_node1732703754281")

# Script generated for node s3_patient
s3_patient_node1732703814174 = glueContext.create_dynamic_frame.from_catalog(database="healthcare", table_name="patient", transformation_ctx="s3_patient_node1732703814174")

# Script generated for node s3_patient_lab_test
s3_patient_lab_test_node1732703859405 = glueContext.create_dynamic_frame.from_catalog(database="healthcare", table_name="patientlabtest", transformation_ctx="s3_patient_lab_test_node1732703859405")

# Script generated for node s3_blood_test
s3_blood_test_node1732702914441 = glueContext.create_dynamic_frame.from_catalog(database="healthcare", table_name="bloodtest", transformation_ctx="s3_blood_test_node1732702914441")

# Script generated for node s3_heart_test
s3_heart_test_node1732703789277 = glueContext.create_dynamic_frame.from_catalog(database="healthcare", table_name="hearttest", transformation_ctx="s3_heart_test_node1732703789277")

# Script generated for node SQL Query
SqlQuery230 = '''
select 
patient.gender,
generalbodytest.hypertension,	
hearttest.heart_disease,	
generalbodytest.smoking_history,	
bloodtest.hbA1c_level,	
generalbodytest.pregnancies,	
bloodtest.glucose,	
hearttest.blood_pressure,	
generalbodytest.skin_thickness,	
bloodtest.insulin,	
generalbodytest.bmi,	
generalbodytest.diabetes_pedigree_function,	
FLOOR(DATEDIFF(CURRENT_DATE(), TO_DATE(patient.date_of_birth, 'dd-MM-yyyy')) / 365) AS age,
diagnosis.is_diabetic
from patient
left join patientlabtest on patient.patient_id=patientlabtest.patient_id
left join hearttest on hearttest.patient_id=patient.patient_id and patientlabtest.heart_test_id=hearttest.heart_test_id	
left join bloodtest on bloodtest.patient_id=patient.patient_id and patientlabtest.blood_test_id=bloodtest.blood_test_id
left join generalbodytest on generalbodytest.patient_id=patient.patient_id and patientlabtest.general_body_test_id=generalbodytest.general_body_test_id
left join diagnosis on diagnosis.patient_id=patient.patient_id;
'''
SQLQuery_node1732703925673 = sparkSqlQuery(glueContext, query = SqlQuery230, mapping = {"patientlabtest":s3_patient_lab_test_node1732703859405, "bloodtest":s3_blood_test_node1732702914441, "diagnosis":s3_diagnosis_node1732703477279, "generalbodytest":s3_general_body_test_node1732703754281, "hearttest":s3_heart_test_node1732703789277, "patient":s3_patient_node1732703814174}, transformation_ctx = "SQLQuery_node1732703925673")

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1732709806399 = glueContext.write_dynamic_frame.from_catalog(frame=SQLQuery_node1732703925673, database="aroradb", table_name="healthcare_diabetes_prediction", transformation_ctx="AWSGlueDataCatalog_node1732709806399")

# Script generated for node output_diagnosis_prediction
output_diagnosis_prediction_node1732706915175 = glueContext.write_dynamic_frame.from_options(frame=SQLQuery_node1732703925673, connection_type="s3", format="csv", connection_options={"path": "s3://laboratory-diagnostics-data/OutputData/diabeticprediction/", "partitionKeys": []}, transformation_ctx="output_diagnosis_prediction_node1732706915175")

job.commit()