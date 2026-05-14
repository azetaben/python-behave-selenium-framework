@verification_helper @text_and_lists @all
Feature: Page text and lists verification

  Background:
    Given the user navigates to the application home page

  @TextVerification @Smoke @regression @login
  Scenario: Login page fields are visible
    Then the username field should be visible
    And the password field should be visible
    And the login button should be visible

  @TextVerification @regression @login
  Scenario: Failed login shows error text
    When the user logs in with username ref "locked_out_user" and password ref "secret_sauce"
    Then an error message should be displayed
    And the error message should contain "locked out"

  @ListOperations @Smoke @regression @inventory
  Scenario: Inventory list is shown after login
    When the user logs in with username ref "standard_user" and password ref "secret_sauce"
    Then the user should be on the inventory page
    And the product inventory should be displayed

  @ListOperations @regression @cart
  Scenario: Cart contains expected count after adding products
    Given the user has successfully logged in
    When the user adds the first product to the cart
    And the user adds the second product to the cart
    Then the cart should contain 2 items

  @ElementPresence @Smoke @regression @checkout
  Scenario: Checkout fields are present
    Given the user has successfully logged in
    When the user adds the first product to the cart
    And the user navigates to the shopping cart
    And the user proceeds to checkout
    Then the first name field should be visible
    And the last name field should be visible
    And the postal code field should be visible

