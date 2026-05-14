@CheckoutProcess @regression @all
Feature: Checkout process functionality

  Background:
    Given the user has successfully logged in

  @TC_CO_001
  Scenario: verify online order flow to cart page
    And the user should be on the "inventory.html" page
    When the user adds the following products to the cart:
      | product_name                      |
      | Sauce Labs Backpack               |
      | Sauce Labs Bike Light             |
      | Test.allTheThings() T-Shirt (Red) |
    Then the cart should contain 3 items
    And the cart badge should display "3"
    When the user clicks on the cart badge
    Then I am in "cart.html" page
    And the cart should contain 3 items
    When the user proceeds to checkout
    Then the first name field should be visible
