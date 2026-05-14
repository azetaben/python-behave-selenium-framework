@login_logout @all
Feature: Login Functionality

  Background:
    Given the user navigates to the application home page
    Then the username field should be visible
    And the password field should be visible
    And the login button should be visible

  @TC_LLF_001 @validLogin @smoke
  Scenario: login with valid credentials as standard user
    When the user logs in with username ref "standard_user" and password ref "secret_sauce"
    Then the user should be on the inventory page
    And the product inventory should be displayed

  @TC_LLF_002 @invalidLogin
  Scenario: locked out user shows locked-out error
    When the user logs in with username ref "locked_out_user" and password ref "secret_sauce"
    Then an error message should be displayed
    And the error message should contain "locked out"

  @TC_LLF_003 @invalidLogin
  Scenario Outline: invalid credentials show error banner
    When the user logs in with username ref "<username_ref>" and password ref "<password_ref>"
    Then an error message should be displayed
    And the error message should contain "Epic sadface"

    Examples:
      | username_ref  | password_ref   |
      | invalid_user  | wrong_password |
      | standard_user | wrong_password |


