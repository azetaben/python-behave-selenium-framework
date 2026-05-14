@performance @page_load_time @all
Feature: Page load time from login to all application pages
  As a performance engineer
  I want to measure the exact page load time for every page transition starting from the login page
  So that regressions are caught early and each page meets its SLA threshold

  # ---------------------------------------------------------------------------
  # Thresholds used throughout:
  #   Login page initial load   <= 4 000 ms
  #   Login -> Inventory        <= 5 000 ms  (performance_glitch_user gets 12 000 ms)
  #   Inventory -> Cart         <= 3 000 ms
  #   Cart -> Checkout-step-1   <= 3 000 ms
  #   Checkout-step-1 -> step-2 <= 3 000 ms
  #   Checkout-step-2 -> done   <= 3 000 ms
  #   Inventory -> Product page <= 3 000 ms
  # ---------------------------------------------------------------------------

  Background:
    Given the user navigates to the application home page

  # -- TC-PLT-001 -------------------------------------------------------------
  @TC_PLT_001 @Smoke @regression
  Scenario: Login page loads within threshold
    Then the page load time for "Login page" should be recorded
    And  the page should have loaded within 4000 milliseconds

  # -- TC-PLT-002 -------------------------------------------------------------
  @TC_PLT_002 @Smoke @regression
  Scenario: Standard user login to inventory page load time
    When  the user starts a page load timer
    And   the user logs in with username ref "standard_user" and password ref "secret_sauce"
    Then  the user should be on the inventory page
    And   the page load time for "Login to Inventory" should be recorded
    And   the page should have loaded within 5000 milliseconds

  # -- TC-PLT-003 -------------------------------------------------------------
  @TC_PLT_003 @regression
  Scenario: Inventory to cart page load time
    Given the user has successfully logged in
    When  the user starts a page load timer
    And   the user navigates to the shopping cart
    Then  I am in "cart.html" page
    And   the page load time for "Inventory to Cart" should be recorded
    And   the page should have loaded within 3000 milliseconds

  # -- TC-PLT-004 -------------------------------------------------------------
  @TC_PLT_004 @regression
  Scenario: Cart to checkout step-1 page load time
    Given the user has successfully logged in
    When  the user adds the first product to the cart
    And   the user starts a page load timer
    And   the user navigates to the shopping cart
    And   the user proceeds to checkout
    Then  the continue button should be visible
    And   the page load time for "Cart to Checkout Step 1" should be recorded
    And   the page should have loaded within 3000 milliseconds

  # -- TC-PLT-005 -------------------------------------------------------------
  @TC_PLT_005 @regression
  Scenario: Checkout step-1 to step-2 page load time
    Given the user has successfully logged in
    When  the user adds the first product to the cart
    And   the user navigates to the shopping cart
    And   the user proceeds to checkout
    And   the user fills in checkout information:
      | firstName  | Jane        |
      | lastName   | Performance |
      | postalCode | 90210       |
    And   the user starts a page load timer
    And   the user clicks the continue button
    Then  the page load time for "Checkout Step 1 to Step 2" should be recorded
    And   the page should have loaded within 3000 milliseconds

  # -- TC-PLT-006 -------------------------------------------------------------
  @TC_PLT_006 @regression
  Scenario: Checkout step-2 to order-complete page load time
    Given the user has successfully logged in
    When  the user adds the first product to the cart
    And   the user navigates to the shopping cart
    And   the user proceeds to checkout
    And   the user fills in checkout information:
      | firstName  | Jane        |
      | lastName   | Performance |
      | postalCode | 90210       |
    And   the user clicks the continue button
    And   the user starts a page load timer
    And   the user clicks the finish button
    Then  the order should be successfully completed
    And   the page load time for "Checkout Step 2 to Order Complete" should be recorded
    And   the page should have loaded within 3000 milliseconds

  # -- TC-PLT-007 -------------------------------------------------------------
  @TC_PLT_007 @regression
  Scenario: Inventory to product-detail page load time
    Given the user has successfully logged in
    When  the user starts a page load timer
    And   the user clicks on the first product
    Then  the product details page should be displayed
    And   the page load time for "Inventory to Product Detail" should be recorded
    And   the page should have loaded within 3000 milliseconds

  # -- TC-PLT-008 -------------------------------------------------------------
  @TC_PLT_008 @regression
  Scenario: Product-detail back to inventory page load time
    Given the user has successfully logged in
    When  the user clicks on the first product
    And   the user starts a page load timer
    And   the user navigates back to the inventory
    Then  the user should be on the inventory page
    And   the page load time for "Product Detail to Inventory" should be recorded
    And   the page should have loaded within 3000 milliseconds

  # -- TC-PLT-009 -------------------------------------------------------------
  @TC_PLT_009 @regression
  Scenario: Performance glitch user login load time (relaxed threshold)
    When  the user starts a page load timer
    And   the user logs in with username ref "performance_glitch_user" and password ref "secret_sauce"
    Then  the user should be on the inventory page
    And   the page load time for "Login to Inventory (perf-glitch user)" should be recorded
    And   the page should have loaded within 12000 milliseconds

  # -- TC-PLT-010 -------------------------------------------------------------
  @TC_PLT_010 @regression
  Scenario: Compare standard vs performance-glitch user login load times
    When  the user starts a page load timer
    And   the user logs in with username ref "standard_user" and password ref "secret_sauce"
    Then  the user should be on the inventory page
    And   the page load time for "standard_user login" should be recorded
    And   the performance recorded as "standard_user_login"
    Given the user navigates to the application home page
    When  the user starts a page load timer
    And   the user logs in with username ref "performance_glitch_user" and password ref "secret_sauce"
    Then  the user should be on the inventory page
    And   the page load time for "performance_glitch_user login" should be recorded
    And   the performance recorded as "perf_glitch_login"
    Then  "perf_glitch_login" load time should be slower than "standard_user_login"

  # -- TC-PLT-011 -------------------------------------------------------------
  @TC_PLT_011 @regression
  Scenario Outline: Page load time for all critical pages with multiple users
    When  the user starts a page load timer
    And   the user logs in with username ref "<username>" and password ref "secret_sauce"
    Then  the user should be on the inventory page
    And   the page load time for "<label>" should be recorded
    And   the page should have loaded within <threshold_ms> milliseconds

    Examples:
      | username                | label                               | threshold_ms |
      | standard_user           | Standard user login to Inventory    | 5000         |
      | performance_glitch_user | Perf-glitch user login to Inventory | 12000        |

  # -- TC-PLT-012 -------------------------------------------------------------
  @TC_PLT_012 @regression
  Scenario: Full navigation flow timings are collected and reported
    When  the user starts a page load timer
    And   the user logs in with username ref "standard_user" and password ref "secret_sauce"
    Then  the user should be on the inventory page
    When  the user navigates to the shopping cart
    Then  I am in "cart.html" page
    When  the user proceeds to checkout
    Then  the continue button should be visible
    And   the full navigation flow report should be printed



