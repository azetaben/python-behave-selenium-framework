@regression @auth @session @cookie-bypass
Feature: session persistence behavior
  As an authenticated user
  I want my cart/session state to persist during normal navigation
  So that I can continue shopping without re-authentication

  Background:
    Given the user has successfully logged in

  @regression @session @landing
  Scenario: cart badge persists after cart round-trip navigation
    When the user adds the first product to the cart
    And the user navigates to the shopping cart
    And the user navigates back to the inventory
    Then the cart badge should still show 1 item

  @regression @session @inventory
  Scenario: inventory page remains accessible after cart navigation
    When the user navigates to the shopping cart
    And the user navigates back to the inventory
    Then the user should be on the "inventory.html" page


