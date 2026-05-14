@miscellaneous @regression @all
Feature: Page Element Verification

  Background: Navigate to the login page
    Given the user navigates to the application home page

  @TC-MC_002
  Scenario: Verify login page input and button elements are visible
    Then the username field should be visible
    And the password field should be visible
    And the login button should be visible

  @TC-MC_003
  Scenario: Verify successful login reaches inventory page
    When the user logs in with username ref "standard_user" and password ref "secret_sauce"
    Then the user should be on the inventory page
    And the product inventory should be displayed

  @TC-MC_004
  Scenario: Verify invalid login shows an error
    When the user logs in with username ref "invalid_user" and password ref "wrong_password"
    Then an error message should be displayed

  @TC-MC_005
  Scenario Outline: Verify accepted users can authenticate
    When the user logs in with username ref "<username_ref>" and password ref "<password_ref>"
    Then the user should be on the inventory page
    Examples:
      | username_ref            | password_ref |
      | standard_user           | secret_sauce |
      | problem_user            | secret_sauce |
      | performance_glitch_user | secret_sauce |
