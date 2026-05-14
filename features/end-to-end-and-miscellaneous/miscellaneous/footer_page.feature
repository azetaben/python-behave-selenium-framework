@miscellaneous @regression @all
Feature: Footer Section Verification

  @TC-MC_006
  Scenario: Verify inventory page is reachable and cart link works
    Given the user navigates to the application home page
    When the user logs in with username ref "standard_user" and password ref "secret_sauce"
    Then the user should be on the inventory page
    And the product inventory should be displayed
    When the user clicks on the cart badge
    Then I am in "cart.html" page
