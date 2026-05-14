@login_helper_utilities_manifest
Feature: Login helper utilities manifest coverage

  Background:
    Given the user navigates to the application home page

  @login_helper_utilities_path_check
  Scenario: Login and validate inventory reachability
    When the user logs in with username ref "standard_user" and password ref "secret_sauce"
    Then the user should be on the inventory page
    And the product inventory should be displayed

