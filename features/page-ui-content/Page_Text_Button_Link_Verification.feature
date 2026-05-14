@verification_helper @generic_elements @all
Feature: Generic text, button and link verification

  Background:
    Given the user navigates to the application home page

  @TC_GPE_001 @Smoke @regression @text
  Scenario: Login page text and controls are visible
    Then the username field should be visible
    And the password field should be visible
    And the login button should be visible

  @TC_GPE_002 @Smoke @regression @button
  Scenario: Inventory actions are visible after login
    When the user logs in with username ref "standard_user" and password ref "secret_sauce"
    Then the user should be on the inventory page
    And the product inventory should be displayed

  @TC_GPE_003 @Smoke @regression @link
  Scenario: Cart link is navigable from inventory page
    Given the user has successfully logged in
    When the user clicks on the cart badge
    Then I am in "cart.html" page

  @TC_GPE_004 @E2E @regression
  Scenario: Combined login and checkout button visibility
    Given the user has successfully logged in
    When the user adds the first product to the cart
    And the user navigates to the shopping cart
    And the user proceeds to checkout
    Then the first name field should be visible
    And the continue button should be visible


#    Then the "Login" button is not visible on the page
#    Then the "Finish" button is not visible on the page
#    Then the "Remove" button is not visible on the page
#
#    Then a button with label "Login" is not visible on the page
#    Then a button with label "Add to cart" is not visible on the page
#    Then a button with label "Finish" is not visible on the page
#    Then a button with label "Remove" is not visible on the page