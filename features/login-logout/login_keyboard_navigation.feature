@regression @auth @login @keyboard @accessibility
Feature: Login keyboard navigation
  As a keyboard user
  I want to navigate the login form with the Tab key
  So that the login controls are reachable without using a mouse

  Background:
    Given the user navigates to the application home page
    Then the username field should be visible
    And the password field should be visible
    And the login button should be visible

  Scenario: standard user can login successfully
    When the user logs in with username ref "standard_user" and password ref "secret_sauce"
    Then the user should be on the inventory page

  Scenario Outline: accepted users can login successfully
    When the user logs in with username ref "<username_ref>" and password ref "<password_ref>"
    Then the user should be on the inventory page

    Examples:
      | username_ref            | password_ref |
      | standard_user           | secret_sauce |
      | problem_user            | secret_sauce |
      | performance_glitch_user | secret_sauce |
