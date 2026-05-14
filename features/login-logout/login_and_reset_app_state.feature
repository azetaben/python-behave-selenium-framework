@login_logout @all
Feature: Login and cart state flow

  Background:
    Given the user has successfully logged in

  @TC_L_LF_013
  Scenario: add products and verify cart count
    When the user adds the first product to the cart
    And the user adds the second product to the cart
    Then the cart should contain 2 items
    And the cart badge should display "2"

  @TC_L_LF_013A
  Scenario: cart navigation remains available after login
    When the user clicks on the cart badge
    Then I am in "cart.html" page


  @TC_L_LF_013B
  Scenario: return to inventory from cart
    When the user navigates to the shopping cart
    And the user navigates back to the inventory
    Then the user should be on the "inventory.html" page



