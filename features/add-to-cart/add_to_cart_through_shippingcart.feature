@Add2Cart @ShippingCart @regression @all
Feature: Shopping Cart Functionality

  Background:
    Given the user has successfully logged in

  @TC_ATC_001
  Scenario: Add and remove items to/from the cart
    And the user should be on the "inventory.html" page
    When the user adds the following products to the cart:
      | product_name                      |
      | Sauce Labs Backpack               |
      | Sauce Labs Bike Light             |
      | Test.allTheThings() T-Shirt (Red) |
    Then the cart should contain 3 items
    And the cart badge should display "3"
    When the user clicks on the cart badge
    And I am in "cart.html" page
    And the user removes the first item from the cart
    Then the cart should contain 2 items


