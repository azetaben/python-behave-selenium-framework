@login_logout @all @error_validation_tests
Feature: Login Functionality

  Background: Navigate to the login page
    Given the user navigates to the application home page

  Scenario Outline: Valid login with accepted usernames
    When the user logs in with username ref "<username_ref>" and password ref "secret_sauce"
    Then the user should be on the inventory page
    Examples:
      | username_ref            |
      | standard_user           |
      | problem_user            |
      | performance_glitch_user |

  Scenario: Invalid Login
    When the user logs in with username ref "invalid_user" and password ref "wrong_password"
    Then an error message should be displayed
    And the error message should contain "do not match any user"

  Scenario: Locked-out user login
    When the user logs in with username ref "locked_out_user" and password ref "secret_sauce"
    Then an error message should be displayed
    And the error message should contain "locked out"


  Scenario Outline: Invalid login attempts
    When the user logs in with username ref "<username_ref>" and password ref "<password_ref>"
    Then an error message should be displayed
    And the error message should contain "Epic sadface"

    Examples:
      | username_ref  | password_ref   | error_message |
      | invalid_user  | secret_sauce   | Epic sadface  |
      | standard_user | wrong_password | Epic sadface  |
      | !@#$%^&*      | secret_sauce   | Epic sadface  |
      | Standard_User | secret_sauce   | Epic sadface  |


