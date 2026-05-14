@TC_ATC_004 @inventory-item @Add2Cart @regression @cart @complete_order
Feature: Verify complete order functionality
  As a user,
  I want to be able to add items to the cart,
  view the cart details and complete the order successfully.

  Scenario: Should add items to cart and complete the order
    Given the user navigates to the application home page
    When the user logs in with username ref "standard_user" and password ref "secret_sauce"
    Then the user should be on the inventory page
    When the user adds the following products to the cart:
      | product_name            |
      | Sauce Labs Backpack     |
      | Sauce Labs Bike Light   |
      | Sauce Labs Bolt T-Shirt |
    Then the cart should contain 3 items
    When the user clicks on the cart badge
    And I am in "cart.html" page
    And the user proceeds to checkout
    And the user fills in checkout information:
      | firstName  | John  |
      | lastName   | Doe   |
      | postalCode | 12345 |
    And the user clicks the continue button
    And the user reviews the order
    And the user clicks the finish button
    Then the order should be successfully completed
    And the completion message should be displayed
