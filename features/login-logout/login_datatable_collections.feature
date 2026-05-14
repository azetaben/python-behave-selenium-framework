@login_datatable_collections @regression @all
Feature: Login DataTable collection types
  Demonstrates data-driven login scenarios with supported step definitions.

  Background:
    Given the user navigates to the application home page
    Then the username field should be visible

  @TC_DT_001 @listOfLists
  Scenario Outline: Login with accepted users
    When the user logs in with username ref "<username_ref>" and password ref "secret_sauce"
    Then the user should be on the inventory page

    Examples:
      | username_ref            |
      | standard_user           |
      | problem_user            |
      | performance_glitch_user |

  @TC_DT_002 @listOfMaps
  Scenario: Locked-out user is rejected
    When the user logs in with username ref "locked_out_user" and password ref "secret_sauce"
    Then an error message should be displayed
    And the error message should contain "locked out"

  @TC_DT_003 @mapOfStrings
  Scenario: Invalid credentials show error
    When the user logs in with username ref "invalid_user" and password ref "wrong_password"
    Then an error message should be displayed
    And the error message should contain "do not match"

  @TC_DT_004 @mapOfLists
  Scenario Outline: Invalid combinations remain rejected
    When the user logs in with username ref "<username_ref>" and password ref "<password_ref>"
    Then an error message should be displayed

    Examples:
      | username_ref  | password_ref  |
      | standard_user | wrong_pass    |
      | invalid_user  | secret_sauce  |
      | locked_out_user | wrong_pass  |

  @TC_DT_005 @mapOfMaps
  Scenario: Repeated invalid login attempts remain blocked
    When the user logs in with username ref "invalid_user" and password ref "wrong_password"
    Then an error message should be displayed
    When the user logs in with username ref "standard_user" and password ref "wrong_password"
    Then an error message should be displayed
