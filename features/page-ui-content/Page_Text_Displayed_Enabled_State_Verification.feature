@verification_helper @display_state @all
Feature: Element displayed and enabled state verification

  Background:
    Given the user navigates to the application home page

  @DisplayState @Smoke @regression @login
  Scenario: Verify login form elements are displayed
    Then the username field should be visible
    And the password field should be visible
    And the login button should be visible

  @DisplayState @Smoke @regression @login
  Scenario: Verify login can proceed to inventory
    When the user logs in with username ref "standard_user" and password ref "secret_sauce"
    Then the user should be on the inventory page

  @DisplayState @regression @inventory
  Scenario: Verify product list is displayed on inventory page
    Given the user has successfully logged in
    Then the product inventory should be displayed

  @DisplayState @regression @inventory
  Scenario: Verify remove button appears after add to cart
    Given the user has successfully logged in
    When the user add a product item "Sauce Labs Backpack" to the cart
    Then the user can see remove button for "Sauce Labs Backpack"

  @EnabledState @regression @inventory
  Scenario: Verify cart badge updates
    Given the user has successfully logged in
    When the user adds the first product to the cart
    Then the cart badge should display "1"

  @DisplayedAndEnabled @Smoke @regression @checkout
  Scenario: Verify checkout fields are displayed and enabled
    Given the user has successfully logged in
    When the user adds the first product to the cart
    And the user navigates to the shopping cart
    And the user proceeds to checkout
    Then the first name field should be visible
    And the last name field should be visible
    And the continue button should be visible


  @DisplayState @regression @cart
  Scenario: Verify cart page is displayed after navigation
    Given the user has successfully logged in
    When the user navigates to the shopping cart
    Then I am in "cart.html" page

