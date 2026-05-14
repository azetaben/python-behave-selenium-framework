@login @dataDriven @json_data @all
Feature: Data-Driven Login Tests with JSON External Data
  As a test automation engineer
  I want to execute login validations using external JSON test data
  So that test credentials and expected outcomes are maintained in portable JSON format
  And tests can be easily integrated with external test management systems

  Background:
    Given the user navigates to the application home page
    Then the username field should be visible
    And the password field should be visible
    And the login button should be visible
    Given I load login test data from "jsonFiles/login_external_data.json"

  @json_data_count
  Scenario: Verify JSON test data is loaded correctly
    Given I have 12 login test cases loaded
    Then I print test data summary

  @json_success_cases
  Scenario: Execute all successful JSON login cases
    Given I filter test data for successful logins
    Then I should have 5 test cases with expected result "SUCCESS"

  @json_failure_cases
  Scenario: Verify JSON includes failure test cases
    Given I filter test data for failed logins
    Then I should have 7 test cases with expected result "FAILURE"

  @json_single_standard_user
  Scenario: JSON standard user can login successfully
    When I execute login test case "JSON_TC_001"
    Then the test case should result in "SUCCESS"
    And the user should be on the inventory page

  @json_single_locked_user
  Scenario: JSON locked-out user cannot login
    When I execute login test case "JSON_TC_002"
    Then the test case should result in "FAILURE"
    And an error message should be displayed
    And the error message should match the expected message

  @json_single_invalid_creds
  Scenario: JSON invalid credentials cannot login
    When I execute login test case "JSON_TC_007"
    Then the test case should result in "FAILURE"
    And an error message should be displayed

  @json_single_empty_username
  Scenario: JSON empty username shows required error
    When I execute login test case "JSON_TC_009"
    Then the test case should result in "FAILURE"
    And the error message should contain "Username is required"

  @json_single_empty_password
  Scenario: JSON empty password shows required error
    When I execute login test case "JSON_TC_010"
    Then the test case should result in "FAILURE"
    And the error message should contain "Password is required"

  @json_inventory @data_variety
  Scenario Outline: JSON success cases - various user types
    When I execute login test case "<test_case_id>"
    Then the test case should result in "<expected>"

    Examples: Valid Users Can Login
      | test_case_id | expected |
      | JSON_TC_001  | SUCCESS  |
      | JSON_TC_003  | SUCCESS  |
      | JSON_TC_005  | SUCCESS  |

  @json_inventory @data_variety
  Scenario Outline: JSON failure cases - various error scenarios
    When I execute login test case "<test_case_id>"
    Then the test case should result in "<expected>"
    And the error message should contain "<error_hint>"

    Examples: Locked Users Cannot Login
      | test_case_id | expected | error_hint |
      | JSON_TC_002  | FAILURE  | locked out |

    Examples: Invalid Credentials Cannot Login
      | test_case_id | expected | error_hint  |
      | JSON_TC_007  | FAILURE  | do not match |
      | JSON_TC_008  | FAILURE  | do not match |

    Examples: Missing Fields Show Required Errors
      | test_case_id | expected | error_hint |
      | JSON_TC_009  | FAILURE  | Username   |
      | JSON_TC_010  | FAILURE  | Password   |
