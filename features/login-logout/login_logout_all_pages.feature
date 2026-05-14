@login_logout @regression @all
Feature: Login and logout from all pages except login page
  As a logged-in user
  I want to be able to log out from each application page
  So that session termination works consistently across the app

  @inventory @TC_LP_001
  Scenario: Logout from inventory page
    Given the user has successfully logged in
    Then I am in "inventory.html" page
    And the user tap on the toggle menu button
    And the user clicks on the "Logout" menu link
    Then the user should be on the login page
    And I am in "/" page

  @product_detail @TC_LP_002
  Scenario: Logout from product detail page
    Given the user has successfully logged in
    When the user clicks on the first product
    Then I am in "inventory-item.html" page
    And the user tap on the toggle menu button
    And the user clicks on the "Logout" menu link
    Then the user should be on the login page
    And I am in "/" page

  @cart @TC_LP_003
  Scenario: Logout from cart page
    Given the user has successfully logged in
    When the user adds the first product to the cart
    And the user clicks on the cart badge
    Then I am in "cart.html" page
    And the user tap on the toggle menu button
    And the user clicks on the "Logout" menu link
    Then the user should be on the login page
    And I am in "/" page

  @checkout_step_one @TC_LP_004
  Scenario: Logout from checkout step one page
    Given the user has successfully logged in
    When the user adds the first product to the cart
    And the user clicks on the cart badge
    And the user proceeds to checkout
    Then I am in "checkout-step-one.html" page
    And the user tap on the toggle menu button
    And the user clicks on the "Logout" menu link
    Then the user should be on the login page
    And I am in "/" page

  @checkout_step_two @TC_LP_005
  Scenario: Logout from checkout step two page
    Given the user has successfully logged in
    When the user adds the first product to the cart
    And the user clicks on the cart badge
    And the user proceeds to checkout
    And the user fills in checkout information:
      | firstName  | John  |
      | lastName   | Doe   |
      | postalCode | 12345 |
    And the user clicks the continue button
    Then I am in "checkout-step-two.html" page
    And the user tap on the toggle menu button
    And the user clicks on the "Logout" menu link
    Then the user should be on the login page
    And I am in "/" page

  @checkout_complete @TC_LP_006
  Scenario: Logout from checkout complete page
    Given the user has successfully logged in
    When the user adds the first product to the cart
    And the user clicks on the cart badge
    And the user proceeds to checkout
    And the user fills in checkout information:
      | firstName  | John  |
      | lastName   | Doe   |
      | postalCode | 12345 |
    And the user clicks the continue button
    And the user clicks the finish button
    Then I am in "checkout-complete.html" page
    And the user tap on the toggle menu button
    And the user clicks on the "Logout" menu link
    Then the user should be on the login page
    And I am in "/" page

