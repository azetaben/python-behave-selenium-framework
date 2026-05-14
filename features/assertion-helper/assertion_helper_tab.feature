@assertion_helper_tab @regression @all
Feature: Assertion helper style checks for cart/inventory behavior

  Background:
    Given the user has successfully logged in

  @TC_AH_TAB_001
  Scenario: verify current page is inventory after login
    Then the user should be on the "inventory.html" page

  @TC_AH_TAB_002
  Scenario: verify cart count after adding one product
    When the user add a product item "Sauce Labs Backpack" to the cart
    Then the cart should contain 1 item
    And the cart badge should display "1"

  @TC_AH_TAB_003
  Scenario: verify cart page is reachable from inventory
    When the user clicks on the cart badge
    Then I am in "cart.html" page
