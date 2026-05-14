Feature: Login security checks for Sauce Demo
  As a user,
  I want to ensure that the login functionality is secure against common attack vectors
  So that my account and data are protected.

  @TC_L_LF_031 @security @login @invalidLogin @regression
  Scenario Outline: 031 - unauthenticated login attempts are rejected
    Given the user navigates to the application home page
    When the user logs in with username ref "<username_ref>" and password ref "<password_ref>"
    Then an error message should be displayed
    And the error message should contain "<error_message_contains>"

    Examples:
      | username_ref    | password_ref   | error_message_contains |
      | invalid_user    | wrong_password | do not match           |
      | locked_out_user | secret_sauce   | locked out             |
