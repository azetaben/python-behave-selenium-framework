@login_logout @all
Feature: Login Functionality

  Background:
    Given the user navigates to the application home page
    Then the username field should be visible
    And the password field should be visible
    And the login button should be visible

  @TC_LF_018
  Scenario: Valid login
    When the user logs in with username ref "standard_user" and password ref "secret_sauce"
    Then the user should be on the inventory page
    And the product inventory should be displayed

  @TC_L_LF_019
  Scenario: Invalid login
    When the user logs in with username ref "invalid_user" and password ref "wrong_password"
    Then an error message should be displayed
    And the error message should contain "do not match any user"

  @TC_L_LF_020
  Scenario: Locked-out user
    When the user logs in with username ref "locked_out_user" and password ref "secret_sauce"
    Then an error message should be displayed
    And the error message should contain "locked out"

  @TC_L_LF_021
  Scenario: Login page UI elements
    Then the username field should be visible
    And the password field should be visible
    And the login button should be visible
