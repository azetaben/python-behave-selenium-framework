@miscellaneous
@Accessibility
@login_logout
@login_logout
@all
Feature: Web Page Accessibility

  Background: navigates to login page
    Given the user navigates to the application home page

  @TC-MC_008
  Scenario: Check accessibility basics of the Sauce Demo login page
    Then the username field should be visible
    And the password field should be visible
    And the login button should be visible

  @TC-MC_009
  Scenario: Check accessibility basics of the Sauce Demo inventory page after login
    When the user logs in with username ref "standard_user" and password ref "secret_sauce"
    Then the user should be on the inventory page
    And the product inventory should be displayed
