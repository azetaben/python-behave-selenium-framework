@regression @auth @login @encoding
Feature: Login security encoded-input checks
  As an application user
  I want encoded credential handling to be validated
  So that login behavior remains predictable when encoded inputs are used

  Background:
    Given the user navigates to the application home page
    Then the username field should be visible
    And the password field should be visible
    And the login button should be visible

  @regression @login @encoding
  Scenario: Normal valid credentials still authenticate
    When the user logs in with username ref "standard_user" and password ref "secret_sauce"
    Then the user should be on the inventory page

  @regression @login @encoding @negative
  Scenario: Invalid encoded-looking values are rejected
    When the user logs in with username ref "d3JvbmdfdXNlcg==" and password ref "d3JvbmdfcGFzcw=="
    Then an error message should be displayed
    And the error message should contain "do not match any user"
