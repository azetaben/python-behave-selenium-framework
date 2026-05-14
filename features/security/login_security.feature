@regression @security @auth @login
Feature: Login security and penetration testing
  As a security-conscious application owner
  I want login flows to resist common attack patterns
  So that authentication remains protected against misuse and tampering

  Background:
    Given the user navigates to the application home page
    Then the username field should be visible
    And the password field should be visible
    And the login button should be visible

  @regression @login @ui @security
  Scenario: Login form is present and standard login succeeds
    When the user logs in with username ref "standard_user" and password ref "secret_sauce"
    Then the user should be on the inventory page

  @regression @security @negative
  Scenario Outline: SQL injection prevention on login
    When the user logs in with username ref "<sqli_payload>" and password ref "Password123!"
    Then an error message should be displayed
    And the error message should contain "do not match"

    Examples:
      | sqli_payload               |
      | ' OR '1'='1                |
      | admin' --                  |
      | ' UNION SELECT NULL, NULL# |

  @regression @security @validation
  Scenario: Locked-out account remains blocked
    When the user logs in with username ref "locked_out_user" and password ref "secret_sauce"
    Then an error message should be displayed
    And the error message should contain "locked out"
