@miscellaneous @regression @performance @all
Feature: Performance Smoke Audit

  @TC-MC_007
  Scenario: Login page and inventory load smoke check
    Given the user navigates to the application home page
    Then the username field should be visible
    When the user logs in with username ref "standard_user" and password ref "secret_sauce"
    Then the user should be on the inventory page

  @TC-MC_007_1
  Scenario: Performance-glitch user checkout flow smoke check
    Given the user navigates to the application home page
    When the user logs in with username ref "performance_glitch_user" and password ref "secret_sauce"
    And the user adds the first product to the cart
    And the user navigates to the shopping cart
    And the user proceeds to checkout
    Then the first name field should be visible
