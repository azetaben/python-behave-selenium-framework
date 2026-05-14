@login_general_examples
Feature: Login examples using general page contracts and helper utilities

  Background:
    Given the user navigates to the application home page

  @login_general_form_validation
  Scenario: Validate the login page elements are visible
    Then the username field should be visible
    And the password field should be visible
    And the login button should be visible

  @login_general_typed_input
  Scenario: Login succeeds with standard user
    When the user logs in with username ref "standard_user" and password ref "secret_sauce"
    Then the user should be on the inventory page
    And the product inventory should be displayed

  @login_general_field_data
  Scenario: Invalid user shows error
    When the user logs in with username ref "invalid_user" and password ref "wrong_password"
    Then an error message should be displayed



