@e2e @regression @all
Feature: Complete Online Order

  @TC-e2e_003
  Scenario Outline: End to end online order for accepted users
    Given the user navigates to the application home page
    When the user logs in with username ref "<username_ref>" and password ref "<password_ref>"
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
    Examples:
      | username_ref            | password_ref |
      | standard_user           | secret_sauce |
      | performance_glitch_user | secret_sauce |
