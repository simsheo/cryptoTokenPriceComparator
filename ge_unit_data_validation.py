import time
import requests
import pandas as pd
import great_expectations as ge
from great_expectations.core.expectation_configuration import ExpectationConfiguration
from great_expectations.core.batch import RuntimeBatchRequest

# Set up the DataContext
context = ge.get_context()
datasource_config = {
    "name": "api_datasource",
    "class_name": "Datasource",
    "module_name": "great_expectations.datasource",
    "execution_engine": {
        "module_name": "great_expectations.execution_engine",
        "class_name": "PandasExecutionEngine",
    },
    "data_connectors": {
        "default_runtime_data_connector_name": {
            "class_name": "RuntimeDataConnector",
            "module_name": "great_expectations.datasource.data_connector",
            "batch_identifiers": ["default_identifier_name"],
        },
    },
}
context.add_datasource(**datasource_config)

suite = context.create_expectation_suite(expectation_suite_name="api_data_validation_suite", overwrite_existing=True)

# Add Expectations
# Expectation-1: Schema (Column Names and Positions) Validation
expectation_configuration_1 = ExpectationConfiguration(
    # Name of expectation type being added
    expectation_type="expect_table_columns_to_match_ordered_list",
    kwargs={
        "column_list": [
            "Symbol",
            "Name",
            "Address",
            "Blockchain",
            "Price",
            "PriceYesterday",
            "VolumeYesterdayUSD",
            "Time",
            "Source",
            "Signature"
        ]
    },
    # `This is to add comments to Expectations and display them in Data Docs`.
    meta={
        "notes": {
            "format": "markdown",
            "content": "Schema Validation",
        }
    },
)
# Expectation-2: Column Value is Not Null
expectation_configuration_2 = ExpectationConfiguration(
    expectation_type="expect_column_values_to_not_be_null",
    kwargs={
        "column": "Name",
        "mostly": 1.0,
    },
    meta={
        "notes": {
            "format": "markdown",
            "content": "Integrity Check",
        }
    },
)

# Expectation-3: Timestamp and Signature is unique
expectation_configuration_3 = ExpectationConfiguration(
    expectation_type="expect_column_values_to_be_unique",
    kwargs={
        "column": "Time"
    },
    meta={
        "notes": {
            "format": "markdown",
            "content": "Uniqueness Check",
        }
    },
)

# Expectation-4: Consistency Check
expectation_configuration_4 = ExpectationConfiguration(
    expectation_type="expect_column_values_to_be_between",
    kwargs={
        "column": "Price",
        "min_value":0.5,
        "max_value":3.5
               
    },
    meta={
        "notes": {
            "format": "markdown",
            "content": "Data Consistency Check",
        }
    },
)



suite.add_expectation(expectation_configuration=expectation_configuration_1)
suite.add_expectation(expectation_configuration=expectation_configuration_2)
suite.add_expectation(expectation_configuration=expectation_configuration_3)
suite.add_expectation(expectation_configuration=expectation_configuration_4)
context.save_expectation_suite(suite, "api_data_validation_suite")

def main():
    try:
        api_url = "https://api.diadata.org/v1/assetQuotation/Fantom/0xfB98B335551a418cD0737375a2ea0ded62Ea213b"
        response = requests.get(api_url)
        data = response.json()

        data_dict = {key: [value] for key, value in data.items()}
        df = pd.DataFrame(data_dict)
        batch_request = RuntimeBatchRequest(
        datasource_name="api_datasource",
        data_connector_name="default_runtime_data_connector_name",
        data_asset_name="api_data",
        runtime_parameters={"batch_data":df},
        batch_identifiers={"default_identifier_name":"default_identifier"}
        )
        checkpoint_config = {
            "name": "api_data_validation_checkpoint",
            "config_version": 1,
            "class_name":"SimpleCheckpoint",
            "expectation_suite_name": "api_data_validation_suite"
        }
        context.add_checkpoint(**checkpoint_config)
        results = context.run_checkpoint(
            checkpoint_name="api_data_checkpoint",
            validations=[
                {"batch_request": batch_request}
            ]
        )
        print(results)
        print("Validation completed")

    except Exception as e:
        print("An error occurred:", str(e))

if __name__ == "__main__":
    main()
