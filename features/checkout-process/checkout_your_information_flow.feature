@CheckoutProcess @regression @all
Feature: Checkout your information flow

  Background:
    Given the user has successfully logged in
    And the user has added products to the cart
    When the user navigates to the shopping cart
    And the user proceeds to checkout

  @TC_CO_009
  Scenario: Enter valid checkout information
    Then the first name field should be visible
    And the last name field should be visible
    And the postal code field should be visible
    And the continue button should be visible
    When the user fills in checkout information:
      | firstName  | John  |
      | lastName   | Doe   |
      | postalCode | 12345 |
    And the user clicks the continue button
    When the user reviews the order

  @TC_CO_010
  Scenario: Empty checkout information shows validation error
    When the user clicks the continue button without filling any fields
    Then a checkout error message should be displayed
    And the error message should indicate missing fields
