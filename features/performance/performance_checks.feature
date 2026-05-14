@regression @performance
Feature: Performance checks
  As an application user
  I want the main pages to meet practical speed expectations
  So that performance regressions are detected before release

  Background:
    Given the user navigates to the application home page

  @regression @performance @login
  Scenario: Login page controls are available
    Then the username field should be visible
    And the password field should be visible
    And the login button should be visible

  @regression @performance @inventory
  Scenario: Product page is reachable after login
    When the user logs in with username ref "standard_user" and password ref "secret_sauce"
    Then the user should be on the inventory page



