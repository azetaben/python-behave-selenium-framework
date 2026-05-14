@login_logout @all
Feature: Logout Functionality

  Background:
    Given the user has successfully logged in

  @TC_L_LF_022
  Scenario: Logged in user can still access cart and return
    When the user adds the first product to the cart
    And the user clicks on the cart badge
    Then I am in "cart.html" page
    When the user navigates back to the inventory
    Then the user should be on the "inventory.html" page

