# Test Data Integration - Quick Start Guide

## 🚀 Quick Start (5 minutes)

### 1. Load Test Data in Your Feature

```gherkin
@dataDriven @csv
Scenario: Login with CSV test data
  Given the user navigates to the application home page
  And I load login test data from "csvFiles/login_test_data.csv"
  When I execute login test case "CSV_LOGIN_001"
  Then the test case should result in "SUCCESS"
```

### 2. Run Your Tests

```bash
# Run all data-driven tests
behave features/Data-Driven-Test/ --tags @dataDriven

# Run just CSV tests
behave features/Data-Driven-Test/data_driven_csv_login.feature

# Run specific scenario
behave features/Data-Driven-Test/data_driven_json_login.feature -n "JSON standard user can login"
```

### 3. Verify It Works

```bash
# Try the example runner to see all features
python run_testdata_integration_example.py
```

## 📊 Available Test Data Files

| File | Format | Cases | Coverage |
|------|--------|-------|----------|
| `csvFiles/login_test_data.csv` | CSV | 10 | Users, locked accounts, invalid creds, empty fields |
| `jsonFiles/login_external_data.json` | JSON | 12 | All user types, comprehensive scenarios |
| `excelFiles/login_external_data.xlsx` | Excel | varies | Requires openpyxl |

## 🔧 Common Tasks

### Load CSV Data
```python
from utils.testdata_loader import TestDataLoader

test_cases = TestDataLoader.load_login_csv('testData/csvFiles/login_test_data.csv')
for tc in test_cases:
    print(f"{tc.test_case_id}: {tc.username} → {tc.expected_result}")
```

### Load JSON Data
```python
test_cases = TestDataLoader.load_login_json('testData/jsonFiles/login_external_data.json')
```

### Auto-Detect Format
```python
# Automatically detects CSV/JSON/Excel from file extension
test_cases = TestDataLoader.load_login_data('testData/csvFiles/login_test_data.csv')
```

### Filter Test Data
```python
# Success cases only
success_cases = [tc for tc in test_cases if tc.expected_result == 'SUCCESS']

# Specific username
locked_user_cases = [tc for tc in test_cases if tc.username == 'locked_out_user']
```

## 📁 File Locations

```
testData/
├── README.md                          ← Full documentation
├── csvFiles/
│   └── login_test_data.csv           ← Example CSV data
├── jsonFiles/
│   └── login_external_data.json      ← Example JSON data
└── excelFiles/
    └── login_external_data.xlsx      ← Example Excel data (optional)

features/
├── Data-Driven-Test/
│   ├── data_driven_csv_login.feature  ← CSV feature examples
│   ├── data_driven_json_login.feature ← JSON feature examples
│   └── login_json_excel_data_driven.feature
└── steps/
    ├── login_steps.py                ← Core login steps
    └── data_driven_login_steps.py     ← Data-driven step definitions

utils/
└── testdata_loader.py                ← Test data loading utility
```

## 💡 Example Scenarios

### Basic Data-Driven Test
```gherkin
Scenario: Execute single test case
  Given the user navigates to the application home page
  And I load login test data from "csvFiles/login_test_data.csv"
  When I execute login test case "CSV_LOGIN_001"
  Then the test case should result in "SUCCESS"
```

### Filter and Execute
```gherkin
Scenario: Execute all successful cases
  Given the user navigates to the application home page
  And I load login test data from "jsonFiles/login_external_data.json"
  Given I filter test data for successful logins
  When I execute all loaded login test cases
  Then all test cases should pass
```

### Verify Data Coverage
```gherkin
Scenario: Verify test data completeness
  Given I load login test data from "csvFiles/login_test_data.csv"
  Then I should have 3 test cases with expected result "SUCCESS"
  And I should have 6 test cases with expected result "FAILURE"
  And I print test data summary
```

## 🎯 Key Features

| Feature | Description |
|---------|-------------|
| **Multi-format** | Load from CSV, JSON, or Excel |
| **Auto-detect** | Automatically determine file format |
| **Filtering** | Filter by expected result, username, etc. |
| **Lazy loading** | Load only when needed |
| **Type-safe** | Uses ExternalLoginDataRow dataclass |
| **Extensible** | Easy to add more loaders |

## 📝 Test Data Format

All test data files use the **ExternalLoginDataRow** format:

```
test_case_id        | string  | Unique identifier (e.g., CSV_LOGIN_001)
username            | string  | Login username (or empty for test empty fields)
password            | string  | Login password (or empty for test empty fields)
expected_result     | string  | SUCCESS or FAILURE
expected_message    | string  | Expected error message (if FAILURE)
```

## ✅ Next Steps

1. **Run Examples**: `python run_testdata_integration_example.py`
2. **Review Features**: Check `features/Data-Driven-Test/data_driven_csv_login.feature`
3. **Add Test Data**: Create new CSV/JSON files following the format
4. **Write Tests**: Create feature scenarios using the data-driven steps
5. **Execute Tests**: Run with Behave tags: `behave --tags @dataDriven`

## 🔗 Related Documentation

- **Full Guide**: `testData/README.md`
- **Step Definitions**: `steps/data_driven_login_steps.py`
- **Examples**: `run_testdata_integration_example.py`
- **Feature Files**: `features/Data-Driven-Test/`

## ⚠️ Troubleshooting

### File Not Found
```
Error: FileNotFoundError: CSV file not found
```
**Solution:** Use `TestDataLoader.get_test_data_path()` to get correct path

### Excel Import Error
```
Error: openpyxl not installed
```
**Solution:** `pip install openpyxl`

### Circular Import Error
```
Error: ImportError: circular import
```
**Solution:** Don't import testdata_loader at module level in config files

### Unicode Error
```
Error: UnicodeEncodeError
```
**Solution:** Ensure file encoding is UTF-8

## 🤝 Contributing

To add new test data files:

1. Create CSV/JSON in the appropriate directory
2. Follow the ExternalLoginDataRow format
3. Use descriptive test case IDs (e.g., FEATURE_TC_001)
4. Add scenarios to the feature files

## 📞 Support

For questions about test data integration:
- Check `testData/README.md` for detailed documentation
- Review examples in `run_testdata_integration_example.py`
- See step definitions in `steps/data_driven_login_steps.py`

