@verification_helper @text_and_lists @all
Feature: Page text and lists verification

  Background:
    Given the user navigates to the "login" page
    And the user should be on the "/" page
    And the user can see the page title "Swag Labs"
    And the logo should present and visible
    And the user can see the following input fields:
      | field_name |
      | username   |
      | password   |
    And the user can see the "Login" button is enabled and visible

    And the login page should contain "Accepted usernames are":
      | Accepted usernames|
      | standard_user           |
      | locked_out_user         |
      | problem_user            |
      | performance_glitch_user |
      | error_user              |
      | visual_user             |

    And the login page should contain "Password for all users":
      | Password for all users |
      | secret_sauce            |


  Scenario: Verify login page text and logged in as standard_user
    When the user logged in as standard_user
    And the user should be on the "inventory" page
    And the user can see the page title "Swag Labs"


  Scenario: Verify login page text and logged in as problem_user
    When the user logged in as problem_user
    And the user should be on the "inventory" page
    And the user can see the page title "Swag Labs"

  Scenario: Verify login page text and logged in as performance_glitch_user
    When the user logged in as performance_glitch_user
    Then the user should be on the "inventory" page
    And the user can see the page title "Swag Labs"

  Scenario: Verify login page text and logged in as error_user
    When the user logged in as error_user
    Then the user should be on the "inventory" page
    And the user can see the page title "Swag Labs"

  Scenario: Verify login page text and logged in as visual_user
    When the user logged in as visual_user
    Then the user should be on the "inventory" page
    And the user can see the page title "Swag Labs"

  Scenario: Verify locked out user cannot login
    When the user logged in as locked_out_user
    Then an error message should be displayed
    And the error message should contain "Epic sadface: Sorry, this user has been locked out."
    And the user can see the "Login" button is enabled and visible


  Scenario Outline: Verify login page text and logged in as accepted inventory user
    When the user logged in as <username>
    Then the user should be on the "inventory" page
    And the user can see the page title "Swag Labs"

    Examples:
      | username                |
      | standard_user           |
      | problem_user            |
      | performance_glitch_user |
      | error_user              |
      | visual_user             |

  Scenario: Verify locked out user cannot login 01
    When the user logged in as locked_out_user
    Then an error message should be displayed
    And the error message should contain "Sorry, this user has been locked out."

