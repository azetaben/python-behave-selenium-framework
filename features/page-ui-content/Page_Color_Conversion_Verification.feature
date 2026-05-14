@verification_helper @color_conversion @all
Feature: Page color-related UI smoke verification

  @ColorConversion @Smoke @regression
  Scenario: Login controls are visible
    Given the user navigates to the application home page
    Then the username field should be visible
    And the password field should be visible
    And the login button should be visible

  @ColorConversion @regression
  Scenario: Inventory page is reachable after login
    Given the user navigates to the application home page
    When the user logs in with username ref "standard_user" and password ref "secret_sauce"
    Then the user should be on the inventory page
    And the product inventory should be displayed

  @ColorConversion @framework @regression
  Scenario: Cart badge updates after add-to-cart action
    Given the user has successfully logged in
    When the user adds the first product to the cart
    Then the cart badge should display "1"

