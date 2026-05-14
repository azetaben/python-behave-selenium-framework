@login_logout @all
Feature: Login and session navigation functionality

  @TC_L_LF_012
  Scenario: navigate from login to inventory and cart pages
    Given the user navigates to the application home page
    When the user logs in with username ref "standard_user" and password ref "secret_sauce"
    Then the user should be on the inventory page
    When the user clicks on the cart badge
    Then I am in "cart.html" page
