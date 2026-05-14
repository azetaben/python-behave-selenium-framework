@miscellaneous @Accessibility @regression @all
Feature: Accessibility Check

  @TC-MC_001
  Scenario: Check accessibility basics of login page controls
    Given the user navigates to the application home page
    Then the username field should be visible
    And the password field should be visible
    And the login button should be visible

