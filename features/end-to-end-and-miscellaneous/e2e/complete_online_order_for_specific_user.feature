@e2e @Regression @ParallelRun @all
Feature: Complete Online Order For Specific User

  @TC-e2e_001
  Scenario: End to end online order for standard user
    Given the user navigates to the application home page
    When the user logs in with username ref "standard_user" and password ref "secret_sauce"
    Then the user should be on the inventory page
    When the user adds the following products to the cart:
      | product_name            |
      | Sauce Labs Backpack     |
      | Sauce Labs Bike Light   |
      | Sauce Labs Bolt T-Shirt |
    And the user clicks on the cart badge
    And the user proceeds to checkout
    And the user fills in checkout information:
      | firstName  | John  |
      | lastName   | Doe   |
      | postalCode | 12345 |
    And the user clicks the continue button
    And the user clicks the finish button
    Then the order should be successfully completed
    And the completion message should be displayed

  @TC-e2e_001_1 @ErrorValidation
  Scenario: Locked-out user cannot complete order
    Given the user navigates to the application home page
    When the user logs in with username ref "locked_out_user" and password ref "secret_sauce"
    Then an error message should be displayed
    And the error message should contain "locked out"

  @TC-e2e_001_2
  Scenario: End to end online order for performance glitch user
    Given the user navigates to the application home page
    When the user logs in with username ref "performance_glitch_user" and password ref "secret_sauce"
    Then the user should be on the inventory page
    When the user adds the first product to the cart
    And the user navigates to the shopping cart
    And the user proceeds to checkout
    And the user fills in checkout information:
      | firstName  | John  |
      | lastName   | Doe   |
      | postalCode | 12345 |
    And the user clicks the continue button
    And the user clicks the finish button
    Then the order should be successfully completed
