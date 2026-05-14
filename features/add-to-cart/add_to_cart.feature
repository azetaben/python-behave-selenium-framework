@Add2Cart @regression @all @ShippingCart
Feature: Verify Add-To-Cart Functionality

  Background:
    Given the user has successfully logged in

  @TC_ATC_002 @Add2Cart
  Scenario: should be able to navigate to products to cart page
    When the user clicks on the cart badge
    Then I am in "cart.html" page

  @SelectionState @Smoke @regression @inventory
  Scenario: Verify add to cart button becomes remove after selection
    And the user should be on the "inventory.html" page
    When the user add a product item "Sauce Labs Backpack" to the cart
    Then the user can see remove button for "Sauce Labs Backpack"

  @TC_ATC_003 @Add2Cart @regression @inventory @cart
  Scenario: Should be able to add items to cart
    And the user should be on the "inventory.html" page
    When the user adds the following products to the cart:
      | product_name            |
      | Sauce Labs Backpack     |
      | Sauce Labs Bike Light   |
      | Sauce Labs Bolt T-Shirt |
    Then the cart should contain 3 items
    And the cart badge should display "3"

  @TC_ATC_004 @Add2Cart
  Scenario Outline: Should be able to add to cart above products and verify in the cart
    And the user should be on the "inventory.html" page
    When the user add a product item "<product_name>" to the cart
    Then the user can see remove button for "<product_name>"
    And the cart should contain 1 item

    Examples:
      | product_name          |
      | Sauce Labs Backpack   |
      | Sauce Labs Bike Light |

  @DisplayedAndEnabled @regression @checkout
  Scenario: Verify checkout form elements are displayed and enabled
    And the user should be on the "inventory.html" page
    When the user adds the first product to the cart
    And the user clicks on the cart badge
    And the user proceeds to checkout
    Then the first name field should be visible
    And the last name field should be visible
    And the postal code field should be visible
    And the continue button should be visible





