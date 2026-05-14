@login @dataDriven @csv_data @all
Feature: Data-Driven Login Tests with CSV External Data
  As a test automation engineer
  I want to execute login validations using external CSV test data
  So that test credentials and expected outcomes are maintained outside feature files
  And test coverage is comprehensive across different user types

  Background:
    Given the user navigates to the application home page
    Then the username field should be visible
    And the password field should be visible
    And the login button should be visible
    Given I load up login test data from "csvFiles/login_test_data.csv"

  # ---------------------------------------------------------------------------
  # Single test-case execution
  # ---------------------------------------------------------------------------

  @csv_single_case
  Scenario: Execute single CSV test case - standard user successful login
    When I execute login test case "CSV_LOGIN_001"
    Then the test case should result in "SUCCESS"
    And the user should be on the inventory page

  @csv_single_case
  Scenario: Execute single CSV test case - problem user successful login
    When I execute login test case "CSV_LOGIN_003"
    Then the test case should result in "SUCCESS"
    And the user should be on the inventory page

  @csv_single_case
  Scenario: Execute single CSV test case - performance glitch user successful login
    When I execute login test case "CSV_LOGIN_004"
    Then the test case should result in "SUCCESS"
    And the user should be on the inventory page

  @csv_single_case
  Scenario: Execute single CSV test case - locked user failure
    When I execute login test case "CSV_LOGIN_002"
    Then the test case should result in "FAILURE"
    And an error message should be displayed
    And the error message should match the expected message

  @csv_single_case
  Scenario: Execute single CSV test case - invalid user wrong password failure
    When I execute login test case "CSV_LOGIN_005"
    Then the test case should result in "FAILURE"
    And an error message should be displayed
    And the error message should match the expected message

  @csv_single_case
  Scenario: Execute single CSV test case - valid user wrong password failure
    When I execute login test case "CSV_LOGIN_006"
    Then the test case should result in "FAILURE"
    And an error message should be displayed
    And the error message should match the expected message

  @csv_single_case
  Scenario: Execute single CSV test case - locked user wrong password failure
    When I execute login test case "CSV_LOGIN_010"
    Then the test case should result in "FAILURE"
    And an error message should be displayed
    And the error message should match the expected message

  @csv_single_case
  Scenario: Execute single CSV test case - empty username failure
    When I execute login test case "CSV_LOGIN_007"
    Then the test case should result in "FAILURE"
    And an error message should be displayed
    And the error message should match the expected message

  @csv_single_case
  Scenario: Execute single CSV test case - empty password failure
    When I execute login test case "CSV_LOGIN_008"
    Then the test case should result in "FAILURE"
    And an error message should be displayed
    And the error message should match the expected message

  @csv_single_case
  Scenario: Execute single CSV test case - both fields empty failure
    When I execute login test case "CSV_LOGIN_009"
    Then the test case should result in "FAILURE"
    And an error message should be displayed

  # ---------------------------------------------------------------------------
  # Bulk / filter execution
  # ---------------------------------------------------------------------------

  @csv_data_filter
  Scenario: Execute all successful login test cases from CSV
    Given I filter test data for successful logins
    Then I should have 3 test cases with expected result "SUCCESS"
    When I execute all loaded login test cases
    Then all test cases should pass

  @csv_data_filter
  Scenario: Execute all failure login test cases from CSV
    Given I filter test data for failed logins
    Then I should have 7 test cases with expected result "FAILURE"
    When I execute all loaded login test cases
    Then all test cases should pass

  @csv_data_filter
  Scenario: Verify CSV test data includes failure cases
    Then I should have 7 test cases with expected result "FAILURE"
    And I print test data summary

  # ---------------------------------------------------------------------------
  # Scenario Outline — full matrix
  # ---------------------------------------------------------------------------

  @csv_inventory
  Scenario Outline: CSV test case for user type validation
    When I execute login test case "<test_case_id>"
    Then the test case should result in "<expected>"

    Examples: Standard Users Can Login
      | test_case_id  | expected |
      | CSV_LOGIN_001 | SUCCESS  |
      | CSV_LOGIN_003 | SUCCESS  |
      | CSV_LOGIN_004 | SUCCESS  |

    Examples: Locked Users Cannot Login
      | test_case_id  | expected |
      | CSV_LOGIN_002 | FAILURE  |
      | CSV_LOGIN_010 | FAILURE  |

    Examples: Invalid Credentials Cannot Login
      | test_case_id  | expected |
      | CSV_LOGIN_005 | FAILURE  |
      | CSV_LOGIN_006 | FAILURE  |

    Examples: Missing Credentials Cannot Login
      | test_case_id  | expected |
      | CSV_LOGIN_007 | FAILURE  |
      | CSV_LOGIN_008 | FAILURE  |
      | CSV_LOGIN_009 | FAILURE  |
