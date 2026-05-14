@regression @performance
Feature: Page load performance metrics
  As an application user
  I want key pages to load within acceptable performance thresholds
  So that the application feels responsive during normal use

  Background:
    Given the user navigates to the application home page

  @regression @performance @login
  Scenario: Verify login page baseline availability
    Then the username field should be visible
    And the password field should be visible
    And the login button should be visible

  @regression @performance @inventory
  Scenario: Verify inventory page is reachable
    Given the user navigates to the application home page
    When the user logs in with username ref "standard_user" and password ref "secret_sauce"
    Then the user should be on the inventory page

  @regression @performance @checkout
  Scenario: Verify checkout page is reachable after cart navigation
    Given the user has successfully logged in
    When the user adds the first product to the cart
    And the user navigates to the shopping cart
    And the user proceeds to checkout
    Then the continue button should be visible
