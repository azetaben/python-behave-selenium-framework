# Test Data Integration and Implementation Guide

## Overview

This guide explains how to use the Test Data Integration system for data-driven login tests. The framework supports loading test data from multiple external sources (CSV, JSON, Excel) and executing comprehensive login validations.

## 📁 Test Data Directory Structure

```
testData/
├── application.yml                    # Application configuration
├── csvFiles/
│   ├── login_logout_edge_url_outerhtml_matrix.csv
│   └── login_test_data.csv           # ✨ New: CSV login test data (ExternalLoginDataRow format)
├── jsonFiles/
│   ├── login.json                    # Simple credential pairs
│   ├── login_external_data.json      # ✨ Full test data (ExternalLoginDataRow format)
│   └── helper_utilities_path_manifest.json
└── excelFiles/
    ├── testData.xlsx
    └── login_external_data.xlsx      # ✨ Excel test data (ExternalLoginDataRow format)
```

## 🔧 Test Data Loader Utility

### Location
`utils/testdata_loader.py`

### Core Classes

#### `TestDataLoader`
Main utility class for loading external test data.

**Key Methods:**

```python
# Load from JSON
TestDataLoader.load_login_json(json_file_path) -> List[ExternalLoginDataRow]

# Load from CSV
TestDataLoader.load_login_csv(csv_file_path) -> List[ExternalLoginDataRow]

# Load from Excel
TestDataLoader.load_login_excel(excel_file_path, sheet_name='LoginTestData') -> List[ExternalLoginDataRow]

# Auto-detect format and load
TestDataLoader.load_login_data(file_path, file_format=None) -> List[ExternalLoginDataRow]

# Get path to testData file
TestDataLoader.get_test_data_path(filename: str) -> str

# Create sample files
TestDataLoader.create_sample_csv(output_path: str)
TestDataLoader.create_sample_json(output_path: str)
```

## 📊 Test Data Format

### ExternalLoginDataRow Structure

All test data files should follow this structure with these columns/fields:

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `test_case_id` | string | Unique test case identifier | `CSV_LOGIN_001` |
| `username` | string | Username for login attempt | `standard_user` |
| `password` | string | Password for login attempt | `secret_sauce` |
| `expected_result` | string | Expected outcome: SUCCESS or FAILURE | `SUCCESS` |
| `expected_message` | string | Expected error message (if FAILURE) | `Epic sadface: ...` |

### CSV Format

**File:** `testData/csvFiles/login_test_data.csv`

```csv
test_case_id,username,password,expected_result,expected_message
CSV_LOGIN_001,standard_user,secret_sauce,SUCCESS,
CSV_LOGIN_002,locked_out_user,secret_sauce,FAILURE,Epic sadface: Sorry, this user has been locked out.
CSV_LOGIN_003,invalid_user,wrong_password,FAILURE,Epic sadface: Username and password do not match any user in this service
CSV_LOGIN_004,,secret_sauce,FAILURE,Epic sadface: Username is required
```

### JSON Format

**File:** `testData/jsonFiles/login_external_data.json`

```json
[
  {
    "testCaseId": "JSON_TC_001",
    "username": "standard_user",
    "password": "secret_sauce",
    "expectedResult": "SUCCESS",
    "expectedMessage": ""
  },
  {
    "testCaseId": "JSON_TC_002",
    "username": "locked_out_user",
    "password": "secret_sauce",
    "expectedResult": "FAILURE",
    "expectedMessage": "Epic sadface: Sorry, this user has been locked out."
  }
]
```

### Excel Format

**File:** `testData/excelFiles/login_external_data.xlsx`

**Sheet Name:** `LoginTestData`

| test_case_id | username | password | expected_result | expected_message |
|---|---|---|---|---|
| XL_LOGIN_001 | standard_user | secret_sauce | SUCCESS | |
| XL_LOGIN_002 | locked_out_user | secret_sauce | FAILURE | Epic sadface: Sorry, this user has been locked out. |

## 📝 Step Definitions

### Location
`steps/data_driven_login_steps.py`

### Available Steps

#### Loading Test Data

```gherkin
# Load test data from CSV
Given I load login test data from "csvFiles/login_test_data.csv"

# Load test data from JSON
Given I load login test data from "jsonFiles/login_external_data.json"

# Load test data from Excel with specific sheet
Given I load login test data from "excelFiles/login_external_data.xlsx" sheet "LoginTestData"
```

#### Filtering Test Data

```gherkin
# Filter to successful login cases only
Given I filter test data for successful logins

# Filter to failed login cases only
Given I filter test data for failed logins
```

#### Verification Steps

```gherkin
# Verify count of loaded test cases
Given I have {count} login test cases loaded

# Verify count of test cases with specific expected result
Then I should have {count} test cases with expected result "{result}"

# Print test data summary
Then I print test data summary
```

#### Execution Steps

```gherkin
# Execute a specific test case by ID
When I execute login test case "{test_case_id}"

# Execute all loaded test cases sequentially
When I execute all loaded login test cases

# Verify test case result
Then the test case should result in "{expected_result}"

# Verify error message matches expected
Then the error message should match the expected message

# Verify all test cases passed
Then all test cases should pass
```

## 🚀 Usage Examples

### Example 1: Simple CSV Data-Driven Test

**Feature File:** `features/Data-Driven-Test/data_driven_csv_login.feature`

```gherkin
@csv_data
Scenario: Execute single CSV test case
  Given the user navigates to the application home page
  And I load login test data from "csvFiles/login_test_data.csv"
  When I execute login test case "CSV_LOGIN_001"
  Then the test case should result in "SUCCESS"
  And the user should be on the inventory page
```

### Example 2: JSON Data-Driven Test with Filtering

**Feature File:** `features/Data-Driven-Test/data_driven_json_login.feature`

```gherkin
Scenario: Execute all successful JSON login cases
  Given the user navigates to the application home page
  And I load login test data from "jsonFiles/login_external_data.json"
  Given I filter test data for successful logins
  Then I should have 5 test cases with expected result "SUCCESS"
```

### Example 3: Excel Data-Driven Test

```gherkin
Scenario: Execute all Excel test cases
  Given the user navigates to the application home page
  And I load login test data from "excelFiles/login_external_data.xlsx" sheet "LoginTestData"
  When I execute all loaded login test cases
  Then all test cases should pass
```

### Example 4: Python Step Definition using Loader

```python
from utils.testdata_loader import TestDataLoader
from models import ExternalLoginDataRow

# Load test data
test_cases = TestDataLoader.load_login_csv('testData/csvFiles/login_test_data.csv')

# Execute tests
for test_case in test_cases:
    context.app.login.login(test_case.username, test_case.password)
    
    if test_case.expected_result == 'SUCCESS':
        assert products_visible()
    else:
        assert error_message_contains(test_case.expected_message)
```

## 📋 Provided Test Data Files

### CSV Test Data
**File:** `testData/csvFiles/login_test_data.csv`
- 10 test cases covering:
  - ✅ Standard user login (SUCCESS)
  - ✅ Various user types (problem_user, performance_glitch_user)
  - ❌ Locked-out user (FAILURE)
  - ❌ Invalid credentials (FAILURE)
  - ❌ Empty fields (FAILURE)

### JSON Test Data
**File:** `testData/jsonFiles/login_external_data.json`
- 12 test cases provided with complementary coverage:
  - ✅ 5 successful scenarios
  - ❌ 7 failure scenarios
  - Comprehensive error message validation

## 🔄 Integration with Existing Code

### Using TestDataLoader in Step Definitions

```python
from behave import given, when, then
from utils.testdata_loader import TestDataLoader

@given('I load login test data from "{csv_file}"')
def step_load_csv_test_data(context, csv_file):
    file_path = TestDataLoader.get_test_data_path(csv_file)
    context.test_data = TestDataLoader.load_login_csv(file_path)

@when('I execute test case "{test_case_id}"')
def step_execute_test_case(context, test_case_id):
    test_case = next(
        (tc for tc in context.test_data if tc.test_case_id == test_case_id),
        None
    )
    if test_case:
        context.app.login.login(test_case.username, test_case.password)
```

### Using TestDataLoader in Python Scripts

```python
from utils.testdata_loader import TestDataLoader

# Load and process test data
csv_data = TestDataLoader.load_login_csv('testData/csvFiles/login_test_data.csv')

for row in csv_data:
    print(f"{row.test_case_id}: {row.username} → {row.expected_result}")
```

## 🎯 Best Practices

### 1. Organize Test Data by Format
- Keep test data organized in dedicated directories
- Use descriptive filenames: `login_test_data.csv`, not `data.csv`

### 2. Maintain Expected Messages
- Keep expected error messages accurate to application responses
- Update when application error messages change
- Test message variations with regex patterns when needed

### 3. Test Case Coverage
- **Positive Cases:** Valid credentials with various user types
- **Negative Cases:** Invalid credentials, missing fields, locked accounts
- **Edge Cases:** Empty strings, special characters, boundary values

### 4. Data-Driven Test Naming
- Use meaningful test case IDs: `CSV_LOGIN_001` not `TC001`
- Include source in ID: `CSV_`, `JSON_`, `XL_` prefixes
- Number sequentially for easy reference

### 5. Parameter Management
- Never hard-code credentials in feature files
- Use external test data for all credential combinations
- Keep testData separate from feature files

## 🔧 Adding New Test Data

### Create Sample Files

```python
from utils.testdata_loader import TestDataLoader

# Create sample CSV
TestDataLoader.create_sample_csv('testData/csvFiles/my_test_data.csv')

# Create sample JSON
TestDataLoader.create_sample_json('testData/jsonFiles/my_test_data.json')
```

### Manual File Creation

1. **CSV:** Add rows following the format in `login_test_data.csv`
2. **JSON:** Add entries matching `login_external_data.json` structure
3. **Excel:** Create sheet named `LoginTestData` with required columns

## 📚 Related Files

| File | Purpose |
|------|---------|
| `models/external_login_data_row.py` | Data model for external test data |
| `steps/data_driven_login_steps.py` | Step definitions for data-driven tests |
| `features/Data-Driven-Test/data_driven_csv_login.feature` | CSV test scenarios |
| `features/Data-Driven-Test/data_driven_json_login.feature` | JSON test scenarios |
| `steps/login_steps.py` | Core login step definitions |

## 🧪 Running Data-Driven Tests

### Run All Data-Driven Tests
```bash
behave features/Data-Driven-Test/ --tags @dataDriven
```

### Run CSV Tests Only
```bash
behave features/Data-Driven-Test/ --tags @csv_data
```

### Run JSON Tests Only
```bash
behave features/Data-Driven-Test/ --tags @json_data
```

### Run Specific Feature
```bash
behave features/Data-Driven-Test/data_driven_csv_login.feature
```

## 🐛 Troubleshooting

### FileNotFoundError: Test Data File Not Found
- Verify file path is correct
- Ensure file exists in `testData/` directory
- Use `TestDataLoader.get_test_data_path()` for correct path construction

### Excel Import Error
- Ensure `openpyxl` is installed: `pip install openpyxl`
- Verify sheet name matches exactly (case-sensitive)

### Test Data Not Loaded in Context
- Use `Given I load login test data from "..."` step before executing tests
- Verify step definition is imported in feature environment

### Expected Message Not Matching
- Check message casing (may need case-insensitive comparison)
- Verify message in actual application matches test data
- Use `the error message should contain` for partial matches

## 📖 Further Reading

- See `models/model_usage_examples.py` for comprehensive code examples
- See `models/quick_reference.py` for quick API reference
- See `doc/JAVA_TO_PYTHON_MODELS_CONVERSION.md` for model details

