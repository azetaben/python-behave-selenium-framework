@login_assertion_helper @login_logout @regression @all
Feature: Login functionality verified with assertion-style checks

  Background:
    Given the user navigates to the application home page

  @TC_LAH_001
  Scenario: Valid login navigates to the inventory page
    When the user logs in with username ref "standard_user" and password ref "secret_sauce"
    Then the user should be on the inventory page
    And the product inventory should be displayed

  @TC_LAH_002
  Scenario: Invalid credentials show an error message
    When the user logs in with username ref "invalid_user" and password ref "wrong_password"
    Then an error message should be displayed
    And the error message should contain "do not match any user"

  @TC_LAH_003
  Scenario: Missing-like username input shows error
    When the user logs in with username ref " " and password ref "secret_sauce"
    Then an error message should be displayed
    And the error message should contain "Username"

  @TC_LAH_004
  Scenario: Missing-like credential input shows error
    When the user logs in with username ref "standard_user" and password ref " "
    Then an error message should be displayed
    And the error message should contain "Password"

  @TC_LAH_005
  Scenario: Locked out user sees locked-out error
    When the user logs in with username ref "locked_out_user" and password ref "secret_sauce"
    Then an error message should be displayed
    And the error message should contain "locked out"

  @TC_LAH_006 @smoke
  Scenario Outline: Accepted users can log in successfully
    When the user logs in with username ref "<username_ref>" and password ref "secret_sauce"
    Then the user should be on the inventory page

    Examples:
      | username_ref            |
      | standard_user           |
      | problem_user            |
      | performance_glitch_user |

  @TC_LAH_007
  Scenario: Login page fields and button are visible
    Then the username field should be visible
    And the password field should be visible
    And the login button should be visible
