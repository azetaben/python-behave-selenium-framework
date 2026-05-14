@login_logout @performance @click_performance @all
Feature: Login and navigation performance smoke checks

  Background:
    Given the user navigates to the application home page

  @TC_PERF_LL_001 @Smoke @regression
  Scenario: Standard user login reaches inventory
    When the user logs in with username ref "standard_user" and password ref "secret_sauce"
    Then the user should be on the inventory page

  @TC_PERF_LL_002 @regression
  Scenario: Inventory to cart navigation works
    Given the user has successfully logged in
    When the user clicks on the cart badge
    Then I am in "cart.html" page

  @TC_PERF_LL_003 @regression
  Scenario: Performance glitch user can reach checkout step one
    Given the user navigates to the application home page
    When the user logs in with username ref "performance_glitch_user" and password ref "secret_sauce"
    And the user adds the first product to the cart
    And the user navigates to the shopping cart
    And the user proceeds to checkout
    Then the continue button should be visible
