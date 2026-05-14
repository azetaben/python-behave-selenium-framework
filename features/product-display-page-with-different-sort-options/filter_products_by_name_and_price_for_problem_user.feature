@ProductsDisplayedPage @ParallelRun @all @error_validation_tests
Feature: Product Sorting

  Background:
    Given the user navigates to the application home page

  @TC_PDP_001
  Scenario: Problem user can login and access inventory
    When the user logs in with username ref "problem_user" and password ref "secret_sauce"
    Then the user should be on the inventory page
    And the product inventory should be displayed

  @TC_PDP_002_1
  Scenario: Problem user can add product to cart
    When the user logs in with username ref "problem_user" and password ref "secret_sauce"
    And the user add a product item "Sauce Labs Backpack" to the cart
    Then the user can see remove button for "Sauce Labs Backpack"

  @TC_PDP_003
  Scenario: Problem user cart badge increments after add
    When the user logs in with username ref "problem_user" and password ref "secret_sauce"
    And the user adds the first product to the cart
    Then the cart badge should display "1"

  @TC_PDP_004
  Scenario: Problem user with invalid credentials is rejected
    When the user logs in with username ref "problem_user" and password ref "wrong_password"
    Then an error message should be displayed

