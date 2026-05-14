@ui-test @toggle-menu
Feature: Hamburger Menu (Toggle Sidebar) Navigation

  As a user
  I want to interact with the hamburger menu sidebar
  In order to navigate between application pages and perform actions

  Background:
    Given the user has successfully logged in
    And the hamburger menu should be visible

  Scenario: All menu items are visible
    Then all menu items should be visible
    And the menu should contain 4 items
    And the close menu button should be visible

  Scenario: Navigate to All Items from menu
    When I click "All Items" in the menu
    Then the user should be on the inventory page
    And I wait for the hamburger menu to disappear

  Scenario: Menu items can be clicked by text
    When I click the "logout" menu item
    Then I wait for the hamburger menu to disappear

  Scenario: Close button closes the menu
    When I close the hamburger menu
    Then the hamburger menu should not be visible
    And I wait for the hamburger menu to disappear

  Scenario: Verify each menu item individually
    Then the "All Items" menu item should be visible
    And the "About" menu item should be visible
    And the "Logout" menu item should be visible
    And the "Reset App State" menu item should be visible

  Scenario: Menu contains expected items
    Then the menu should contain the following items:
      | item            |
      | All Items       |
      | About           |
      | Logout          |
      | Reset App State |


  Scenario: Logged in user can still access cart and logout from menu
    Then the user should be on the "inventory.html" page
    And the user tap on the toggle menu button
    And I close the hamburger menu
    And the user tap on the toggle menu button
    And the user clicks on the "Logout" menu link
    Then the user should be on the login page
    Then I am in "/" page

Scenario: Logged in user can still access cart and About from menu
    Then the user should be on the "inventory.html" page
    And the user tap on the toggle menu button
    And I close the hamburger menu
    And the user tap on the toggle menu button
    And the user clicks on the "About" menu link

Scenario: Logged in user can still access cart and All items from menu
    Then the user should be on the "inventory.html" page
    And the user tap on the toggle menu button
    And I close the hamburger menu
    And the user tap on the toggle menu button
    And the user clicks on the "All Items" menu link
    Then the user should be on the "inventory.html" page

Scenario: Logged in user can still access cart and Reset App State from menu
    Then the user should be on the "inventory.html" page
    And the user tap on the toggle menu button
    And I close the hamburger menu
    And the user tap on the toggle menu button
    And the user clicks on the "Reset App State" menu link
    Then the user should be on the "inventory.html" page

