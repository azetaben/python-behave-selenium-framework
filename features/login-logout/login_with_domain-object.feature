@login_logout @all
Feature: Login Functionality
  As a user,
  I want to login into the application
  inorder to make online purchase.

  Background:
    Given the user navigates to the application home page

  Scenario: login with accepted credentials for all users
    When the user logs in with username ref "standard_user" and password ref "secret_sauce"
    Then the user should be on the inventory page
    And the product inventory should be displayed

