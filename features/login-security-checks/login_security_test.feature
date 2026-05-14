Feature: Login security checks for Sauce Demo
  As a user,
  I want to ensure that the login functionality is secure against common attack vectors
  So that my account and data are protected.


  Background:
    Given the user navigates to the application home page

  @TC_L_LF_023 @security @login @invalidLogin @regression
  Scenario: 023 - reject SQL injection style payload
    When the user logs in with username ref "' OR '1'='1" and password ref "' OR '1'='1"
    Then an error message should be displayed
    And the error message should contain "do not match any user"

  @TC_L_LF_024 @security @login @invalidLogin @regression
  Scenario: 024 - reject XSS style payload in username
    When the user logs in with username ref "<script>alert('xss')</script>" and password ref "secret_sauce"
    Then an error message should be displayed
    And the error message should contain "do not match any user"

  @TC_L_LF_025 @security @login @invalidLogin @regression
  Scenario Outline: 025 - repeated invalid credential attempts do not grant access
    When the user logs in with username ref "standard_user" and password ref "<password_ref>"
    Then an error message should be displayed
    And the error message should contain "do not match any user"
    Examples:
      | password_ref    |
      | wrong_password1 |
      | wrong_password2 |
      | wrong_password3 |
      | wrong_password4 |
      | wrong_password5 |

  @TC_L_LF_026 @security @login @invalidLogin @regression
  Scenario: 026 - consistent error message for invalid user and invalid credentials
    When the user logs in with username ref "non_existing_user_123" and password ref "secret_sauce"
    Then an error message should be displayed
    When the user logs in with username ref "standard_user" and password ref "wrong_password"
    Then an error message should be displayed

  @TC_L_LF_027 @security @login @regression
  Scenario: 027 - locked-out account remains blocked
    When the user logs in with username ref "locked_out_user" and password ref "secret_sauce"
    Then an error message should be displayed
    And the error message should contain "locked out"
