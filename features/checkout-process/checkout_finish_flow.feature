@CheckoutProcess @regression @all
Feature: Checkout finish verification

  Background:
    Given the user has successfully logged in
    And the user should be on the "inventory.html" page
    And I am in "inventory.html" page
    And I close the google password popup if it is open
    And the user has added products to the cart
    When the user navigates to the shopping cart
    And the user proceeds to checkout
    And the user fills in checkout information:
      | firstName  | John  |
      | lastName   | Doe   |
      | postalCode | 12345 |
    And the user clicks the continue button

  @TC_CO_0001
  Scenario: Verify checkout finish summary page
    When the user clicks the finish button
    Then the order should be successfully completed
    And the completion message should be displayed

  @TC_CO_0002
  Scenario: Verify completion message content is present
    When the user clicks the finish button
    Then the completion message should be displayed
