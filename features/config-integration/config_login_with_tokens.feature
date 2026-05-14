@config @login @smoke
Feature: Login using integrated Python config tokens

  Scenario: Successful login with user token credentials
    Given the user navigates to the application home page
    When the user logs in with username ref "user:STANDARD_USERNAME" and password ref "user:PASSWORD"
    Then the user should be on the inventory page

  Scenario Outline: Negative login matrix with table-driven references
    Given the user navigates to the application home page
    When the user logs in with username ref "<username_ref>" and password ref "<password_ref>"
    Then an error message should be displayed
    And the login error should match constant "<expected_error_constant>"

    Examples:
      | username_ref     | password_ref         | expected_error_constant |
      | faker:username   | faker:wrong_password | ERR_WRONG_CREDENTIALS   |
      | USER_LOCKED_OUT  | USER_PASSWORD        | ERR_LOCKED_OUT          |
      | EMPTY            | USER_PASSWORD        | ERR_USERNAME_REQUIRED   |
      | USER_STANDARD    | EMPTY                | ERR_PASSWORD_REQUIRED   |
