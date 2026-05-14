@login_logout @edge @all
Feature: Login and logout edge cases

  Background:
    Given the user navigates to the application home page
    Then the username field should be visible
    And the password field should be visible
    And the login button should be visible

  @TC_EDGE_001
  Scenario: Wrong credentials are rejected
    When the user logs in with username ref "invalid_user" and password ref "wrong_password"
    Then an error message should be displayed
    And the error message should contain "do not match any user"

  @TC_EDGE_002
  Scenario: Locked-out user is rejected
    When the user logs in with username ref "locked_out_user" and password ref "secret_sauce"
    Then an error message should be displayed
    And the error message should contain "locked out"

  @TC_EDGE_003
  Scenario Outline: injection-like payloads are rejected
    When the user logs in with username ref "<username_ref>" and password ref "<password_ref>"
    Then an error message should be displayed
    And the error message should contain "Epic sadface"

    Examples:
      | username_ref              | password_ref              |
      | ' OR '1'='1               | secret_sauce              |
      | standard_user             | ' OR '1'='1               |
      | <script>alert('x')</script> | secret_sauce            |

  @TC_EDGE_004
  Scenario: accepted users can login
    When the user logs in with username ref "standard_user" and password ref "secret_sauce"
    Then the user should be on the inventory page

  @TC_EDGE_005
  Scenario: cart badge persists after navigation round-trip
    Given the user has successfully logged in
    When the user adds the first product to the cart
    And the user navigates to the shopping cart
    And the user navigates back to the inventory
    Then the cart badge should still show 1 item
