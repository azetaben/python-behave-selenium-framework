@verification_helper @page_verification @all
Feature: Page URL, title and header verification

  Background:
    Given the user navigates to the application home page
    Then the username field should be visible

  @TC_VP_001 @Smoke @regression @page_title
  Scenario: Login page controls are available
    Then the password field should be visible
    And the login button should be visible

  @TC_VP_002 @Smoke @regression @page_url
  Scenario: Inventory URL fragment is present after login
    When the user logs in with username ref "standard_user" and password ref "secret_sauce"
    Then the user should be on the inventory page

  @TC_VP_003 @regression @page_header
  Scenario Outline: Accepted users land on inventory page
    Given the user navigates to the application home page
    When the user logs in with username ref "<username_ref>" and password ref "secret_sauce"
    Then the user should be on the inventory page

    Examples:
      | username_ref            |
      | standard_user           |
      | problem_user            |
      | performance_glitch_user |

  @TC_VP_004 @Smoke @E2E @regression
  Scenario: Login then cart navigation verifies route transition
    Given the user has successfully logged in
    When the user clicks on the cart badge
    Then I am in "cart.html" page
