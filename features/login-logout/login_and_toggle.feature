@login_logout @filter @regression @all
Feature: Login and navigation checks

  Background:
    Given the user has successfully logged in
    And the user should be on the "inventory.html" page

  @TC_L_LF_014 @filter @regression
  Scenario: inventory page remains active
    Then the user should be on the "inventory.html" page

  @TC_L_LF_015 @filter @regression
  Scenario: cart link is clickable
    When the user clicks on the cart badge
    Then I am in "cart.html" page

  @TC_L_LF_016 @filter @regression
  Scenario: back navigation to inventory works
    When the user navigates to the shopping cart
    And the user navigates back to the inventory
    Then the user should be on the "inventory.html" page

  @TC_L_LF_017 @filter @regression
  Scenario: cart badge updates after adding one product
    When the user adds the first product to the cart
    Then the cart badge should display "1"





