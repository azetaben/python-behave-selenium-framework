@login_transformer @regression @all
Feature: Login using LoginDataTransformer
  Verifies data-driven login behavior with supported step definitions.

  Background:
    Given the user navigates to the application home page

  @TC_LT_001 @positive
  Scenario: Successful login with standard user
    When the user logs in with username ref "standard_user" and password ref "secret_sauce"
    Then the user should be on the inventory page

  @TC_LT_002 @negative
  Scenario: Failed login with wrong credentials
    When the user logs in with username ref "invalid_user" and password ref "wrong_password"
    Then an error message should be displayed
    And the error message should contain "do not match any user"

  @TC_LT_003 @negative
  Scenario: Failed login for locked-out user
    When the user logs in with username ref "locked_out_user" and password ref "secret_sauce"
    Then an error message should be displayed
    And the error message should contain "locked out"

  @TC_LT_005
  Scenario Outline: Login outcome matrix
    When the user logs in with username ref "<username_ref>" and password ref "<password_ref>"
    Then <expectedResult>

    Examples:
      | username_ref            | password_ref   | expectedResult                          |
      | standard_user           | secret_sauce   | the user should be on the inventory page |
      | problem_user            | secret_sauce   | the user should be on the inventory page |
      | performance_glitch_user | secret_sauce   | the user should be on the inventory page |
      | invalid_user            | wrong_password | an error message should be displayed      |
