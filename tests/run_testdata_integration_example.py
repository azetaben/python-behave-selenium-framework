"""
Example runner demonstrating test data integration and implementation.
Shows how to load and work with test data from CSV, JSON, and Excel sources.
"""

from pathlib import Path
from utils.testdata_loader import TestDataLoader


def example_csv_loading():
    """Example 1: Load login test data from CSV."""
    print("\n" + "="*80)
    print("EXAMPLE 1: Load Login Test Data from CSV")
    print("="*80)

    csv_path = TestDataLoader.get_test_data_path('csvFiles/login_test_data.csv')
    print(f"\n📁 Loading from: {csv_path}\n")

    test_cases = TestDataLoader.load_login_csv(csv_path)

    print(f"✅ Loaded {len(test_cases)} test cases\n")
    print("Test Case Details:")
    print("-" * 80)

    for tc in test_cases[:5]:  # Show first 5
        print(f"  ID: {tc.test_case_id}")
        print(f"     Username: {tc.username or '(empty)'}")
        print(f"     Password: {'*' * len(tc.password) if tc.password else '(empty)'}")
        print(f"     Expected: {tc.expected_result}")
        print(f"     Message: {tc.expected_message or '(no message)'}")
        print()


def example_json_loading():
    """Example 2: Load login test data from JSON."""
    print("\n" + "="*80)
    print("EXAMPLE 2: Load Login Test Data from JSON")
    print("="*80)

    json_path = TestDataLoader.get_test_data_path('jsonFiles/login_external_data.json')
    print(f"\n📁 Loading from: {json_path}\n")

    test_cases = TestDataLoader.load_login_json(json_path)

    print(f"✅ Loaded {len(test_cases)} test cases\n")

    # Count success vs failure
    success = [tc for tc in test_cases if tc.expected_result.upper() == 'SUCCESS']
    failure = [tc for tc in test_cases if tc.expected_result.upper() == 'FAILURE']

    print(f"📊 Statistics:")
    print(f"   - SUCCESS cases: {len(success)}")
    print(f"   - FAILURE cases: {len(failure)}")
    print(f"   - Total: {len(test_cases)}\n")

    print("Sample Test Cases:")
    print("-" * 80)
    for tc in test_cases[:3]:
        print(f"  {tc.test_case_id}: {tc.username} → {tc.expected_result}")


def example_excel_loading():
    """Example 3: Load login test data from Excel."""
    print("\n" + "="*80)
    print("EXAMPLE 3: Load Login Test Data from Excel")
    print("="*80)

    excel_path = TestDataLoader.get_test_data_path('excelFiles/login_external_data.xlsx')

    if not Path(excel_path).exists():
        print(f"\n⚠️  Excel file not found: {excel_path}")
        print("   Skipping Excel example. You can create one using TestDataLoader.create_sample_json()")
        return

    print(f"\n📁 Loading from: {excel_path}\n")

    try:
        test_cases = TestDataLoader.load_login_excel(excel_path, sheet_name='LoginTestData')
        print(f"✅ Loaded {len(test_cases)} test cases from 'LoginTestData' sheet\n")

        for tc in test_cases[:3]:
            print(f"  {tc.test_case_id}: {tc.expected_result}")

    except ImportError:
        print("⚠️  openpyxl not installed. Install with: pip install openpyxl")
    except Exception as e:
        print(f"⚠️  Error loading Excel: {str(e)}")


def example_auto_detect():
    """Example 4: Auto-detect format and load."""
    print("\n" + "="*80)
    print("EXAMPLE 4: Auto-Detect Format and Load")
    print("="*80)

    # Load CSV with auto-detection
    csv_path = TestDataLoader.get_test_data_path('csvFiles/login_test_data.csv')
    print(f"\n📁 Auto-detecting: {csv_path}")

    test_cases = TestDataLoader.load_login_data(csv_path)  # No format specified
    print(f"✅ Auto-detected as CSV and loaded {len(test_cases)} test cases")

    # Load JSON with auto-detection
    json_path = TestDataLoader.get_test_data_path('jsonFiles/login_external_data.json')
    print(f"\n📁 Auto-detecting: {json_path}")

    test_cases = TestDataLoader.load_login_data(json_path)  # No format specified
    print(f"✅ Auto-detected as JSON and loaded {len(test_cases)} test cases")


def example_filter_and_process():
    """Example 5: Filter and process test data."""
    print("\n" + "="*80)
    print("EXAMPLE 5: Filter and Process Test Data")
    print("="*80)

    csv_path = TestDataLoader.get_test_data_path('csvFiles/login_test_data.csv')
    test_cases = TestDataLoader.load_login_csv(csv_path)

    print(f"\n📊 Total loaded: {len(test_cases)} test cases\n")

    # Filter successful cases
    success_cases = [tc for tc in test_cases if tc.expected_result.upper() == 'SUCCESS']
    print(f"✅ SUCCESS cases: {len(success_cases)}")
    for tc in success_cases:
        print(f"   - {tc.test_case_id}: {tc.username}")

    # Filter failure cases
    failure_cases = [tc for tc in test_cases if tc.expected_result.upper() == 'FAILURE']
    print(f"\n❌ FAILURE cases: {len(failure_cases)}")
    for tc in failure_cases:
        print(f"   - {tc.test_case_id}: {tc.username} ({tc.expected_message[:40]}...)")

    # Find by username
    print(f"\n🔍 Find test cases by username:")
    standard_user_cases = [tc for tc in test_cases if tc.username == 'standard_user']
    print(f"   - standard_user: {len(standard_user_cases)} cases")

    # Empty field cases
    empty_field_cases = [tc for tc in test_cases if not tc.username or not tc.password]
    print(f"   - Empty fields: {len(empty_field_cases)} cases")


def example_test_data_path():
    """Example 6: Using get_test_data_path helper."""
    print("\n" + "="*80)
    print("EXAMPLE 6: Using get_test_data_path Helper")
    print("="*80)
    print("\nHelper method for constructing test data paths:\n")

    files = [
        'csvFiles/login_test_data.csv',
        'jsonFiles/login_external_data.json',
        'excelFiles/login_external_data.xlsx',
    ]

    for filename in files:
        path = TestDataLoader.get_test_data_path(filename)
        exists = "✅" if Path(path).exists() else "❌"
        print(f"{exists} {filename}")
        print(f"   → {path}\n")


def example_create_samples():
    """Example 7: Create sample test data files."""
    print("\n" + "="*80)
    print("EXAMPLE 7: Create Sample Test Data Files")
    print("="*80)
    print("\nYou can create sample files programmatically:\n")

    print("# Create sample CSV")
    print('TestDataLoader.create_sample_csv("testData/csvFiles/sample.csv")')
    print()

    print("# Create sample JSON")
    print('TestDataLoader.create_sample_json("testData/jsonFiles/sample.json")')

    print("\n💡 Sample files follow ExternalLoginDataRow format")
    print("   Useful as templates for new test data")


def example_integration():
    """Example 8: Integration with Behave steps."""
    print("\n" + "="*80)
    print("EXAMPLE 8: Integration with Behave Steps")
    print("="*80)

    print("\n📝 Example Behave feature file:\n")
    print("""
    @dataDriven
    Scenario: Execute data-driven login test
      Given the user navigates to the application home page
      And I load login test data from "csvFiles/login_test_data.csv"
      When I execute login test case "CSV_LOGIN_001"
      Then the test case should result in "SUCCESS"
    """)

    print("\n📝 Example Behave step definition:\n")
    print("""
    from behave import given, when, then
    from utils.testdata_loader import TestDataLoader
    
    @given('I load login test data from "{csv_file}"')
    def step_load_csv(context, csv_file):
        path = TestDataLoader.get_test_data_path(csv_file)
        context.test_data = TestDataLoader.load_login_csv(path)
    
    @when('I execute login test case "{test_case_id}"')
    def step_execute(context, test_case_id):
        tc = [t for t in context.test_data if t.test_case_id == test_case_id][0]
        context.app.login.login(tc.username, tc.password)
    """)


def main():
    """Run all examples."""
    print("\n" + "="*80)
    print("TEST DATA INTEGRATION AND IMPLEMENTATION EXAMPLES")
    print("="*80)

    try:
        example_csv_loading()
        example_json_loading()
        example_excel_loading()
        example_auto_detect()
        example_filter_and_process()
        example_test_data_path()
        example_create_samples()
        example_integration()

        print("\n" + "="*80)
        print("✅ ALL EXAMPLES COMPLETED SUCCESSFULLY")
        print("="*80)
        print("\n📚 For more information, see testData/README.md")
        print()

    except Exception as e:
        print(f"\n❌ Error running examples: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()



