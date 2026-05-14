@login_logout @edgeUrlOuterHtml @all
Feature: Login edge coverage

  Background:
    Given the user navigates to the application home page

  @TC_EDGE_URL_HTML_001
  Scenario: Successful login shows inventory page
    When the user logs in with username ref "standard_user" and password ref "secret_sauce"
    Then the user should be on the inventory page

  @TC_EDGE_URL_HTML_002
  Scenario: Invalid login shows generic authentication error
    When the user logs in with username ref "standard_user" and password ref "wrong_password"
    Then an error message should be displayed
    And the error message should contain "do not match any user"

  @TC_EDGE_URL_HTML_003
  Scenario: Locked-out user error is shown
    When the user logs in with username ref "locked_out_user" and password ref "secret_sauce"
    Then an error message should be displayed
    And the error message should contain "locked out"

  @TC_EDGE_URL_HTML_004
  Scenario: Post-login cart navigation remains available
    Given the user has successfully logged in
    When the user clicks on the cart badge
    Then I am in "cart.html" page
