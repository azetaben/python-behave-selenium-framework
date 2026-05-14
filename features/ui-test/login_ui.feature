@login_logout @all
Feature: Login Functionality
  As a user,
  I want to login into the application
  inorder to make online purchase.

  Scenario: Login page UI controls are visible
    Given the user navigates to the application home page
    Then the username field should be visible
    And the password field should be visible
    And the login button should be visible

  Scenario: Successful login reaches inventory UI
    Given the user navigates to the application home page
    When the user logs in with username ref "standard_user" and password ref "secret_sauce"
    Then the user should be on the inventory page
    And the product inventory should be displayed
