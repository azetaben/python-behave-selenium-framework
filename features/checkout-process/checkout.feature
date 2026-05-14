Feature: Checkout Process
  As a user
  I want to complete a purchase
  So that my order is successfully placed

  Background:
    Given the user has successfully logged in
    And the user has added products to the cart

  @smoke @e2e
  Scenario: Complete full checkout flow
    When the user navigates to the shopping cart
    And the user proceeds to checkout
    And the user fills in checkout information:
      | firstName  | John    |
      | lastName   | Doe     |
      | postalCode | 12345   |
    And the user clicks the continue button
    And the user reviews the order
    And the user clicks the finish button
    Then the order should be successfully completed
    And the completion message should be displayed

  @functional
  Scenario: Checkout without filling required fields
    When the user navigates to the shopping cart
    And the user proceeds to checkout
    And the user clicks the continue button without filling any fields
    Then a checkout error message should be displayed
    And the error message should indicate missing fields

  @functional
  Scenario: Order summary shows correct items
    When the user navigates to the shopping cart
    Then the cart should show all added products
    And the item count should match the products count

  @regression
  Scenario: Checkout page elements are available
    When the user navigates to the shopping cart
    And the user proceeds to checkout
    Then the first name field should be visible
    And the last name field should be visible
    And the postal code field should be visible
    And the continue button should be visible
