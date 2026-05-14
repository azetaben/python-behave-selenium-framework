Feature: Login Functionality
  As a user
  I want to log into the Sauce Demo application
  So that I can access the shopping features

  Background:
    Given the user navigates to the application home page

  @smoke @regression
  Scenario: Successful login with valid credentials
    When the user logs in with username ref "standard_user" and password ref "secret_sauce"
    Then the user should be on the inventory page
    And the product inventory should be displayed

  @regression
  Scenario: Login with invalid username
    When the user logs in with username ref "invalid_user" and password ref "secret_sauce"
    Then an error message should be displayed
    And the error message should contain "user"

  @regression
  Scenario: Login with invalid credentials
    When the user logs in with username ref "standard_user" and password ref "wrong_password"
    Then an error message should be displayed
    And the error message should contain "password"

  @regression
  Scenario: Login page elements are visible
    Then the username field should be visible
    And the password field should be visible
    And the login button should be visible


  @regression
  Scenario Outline: Attempt login with invalid credentials
    When the user logs in with username ref "<username_ref>" and password ref "<password_ref>"
    Then an error message should be displayed
    And the error message should contain "user"
    Examples:
      | username_ref        | password_ref   |
      | standard_user       | wrong_password |
      | wrong_standard_user | wrong_password |
