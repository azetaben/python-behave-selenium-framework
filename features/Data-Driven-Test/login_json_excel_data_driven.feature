@login_logout @dataDriven @externalData18 @all
Feature: Login Data-Driven Tests From External Sources
  As a user
  I want to execute login validations using external test data
  So that credentials and expected outcomes are maintained outside feature files

  Background:
    Given the user navigates to the application home page
    Then the username field should be visible
    And the password field should be visible
    And the login button should be visible

  @jsonData @excelData @regression @ErrorValidation
  Scenario Outline: <source> <testCaseId> accepted-user login validation
    When the user logs in with username ref "<username_ref>" and password ref "<password_ref>"
    Then the user should be on the inventory page

    Examples:
      | source | testCaseId  | username_ref            | password_ref |
      | json   | JSON_TC_001 | standard_user           | secret_sauce |
      | json   | JSON_TC_002 | problem_user            | secret_sauce |
      | excel  | XL_TC_001   | performance_glitch_user | secret_sauce |

  Scenario: Invalid login data shows external-data-like error handling
    When the user logs in with username ref "invalid_user" and password ref "wrong_password"
    Then an error message should be displayed
    And the error message should contain "do not match any user"

  Scenario: Locked user data row shows locked-out error handling
    When the user logs in with username ref "locked_out_user" and password ref "secret_sauce"
    Then an error message should be displayed
    And the error message should contain "locked out"
