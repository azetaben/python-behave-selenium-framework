@CheckoutProcess @regression @all
Feature: Checkout overview flow

  Background:
    Given the user has successfully logged in
    And the user has added products to the cart
    When the user navigates to the shopping cart
    And the user proceeds to checkout

  @TC_CO_005
  Scenario: Verify checkout summary is displayed after continue
    When the user fills in checkout information:
      | firstName  | John  |
      | lastName   | Doe   |
      | postalCode | 12345 |
    And the user clicks the continue button
    When the user reviews the order

  @TC_CO_006
  Scenario: Verify order review contains items
    When the user fills in checkout information:
      | firstName  | John  |
      | lastName   | Doe   |
      | postalCode | 12345 |
    And the user clicks the continue button
    When the user reviews the order

  @TC_CO_007
  Scenario: Verify finish button completes order from overview
    When the user fills in checkout information:
      | firstName  | John  |
      | lastName   | Doe   |
      | postalCode | 12345 |
    And the user clicks the continue button
    And the user clicks the finish button
    Then the order should be successfully completed
