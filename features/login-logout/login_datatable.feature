@login_logout @dataDriven @all
Feature: Login Data-Driven Tests
  As a user
  I want to verify login behaviour across all user types and credential combinations
  In order to ensure the authentication system works correctly

  Background:
    Given the user navigates to the application home page

  @TC_LDD_001 @TC_LDD_003 @TC_LDD_004 @TC_LDD_005 @TC_LDD_006
  @validLogin @regression
  Scenario Outline: <testCaseId> - Successful login with valid credentials for <username_ref>
    When the user logs in with username ref "<username_ref>" and password ref "<password_ref>"
    Then the user should be on the inventory page

    Examples:
      | testCaseId | username_ref            | password_ref |
      | TC_LDD_001 | standard_user           | secret_sauce |
      | TC_LDD_003 | problem_user            | secret_sauce |
      | TC_LDD_004 | performance_glitch_user | secret_sauce |

  @TC_LDD_002 @invalidLogin @regression @ErrorValidation
  Scenario: TC_LDD_002 - Failed login for locked_out_user with valid credentials
    When the user logs in with username ref "locked_out_user" and password ref "secret_sauce"
    Then an error message should be displayed
    And the error message should contain "locked out"

  @TC_LDD_007 @TC_LDD_008 @TC_LDD_009 @TC_LDD_010 @TC_LDD_011 @TC_LDD_012
  @invalidLogin @regression @ErrorValidation
  Scenario Outline: <testCaseId> - Failed login with invalid credentials
    When the user logs in with username ref "<username_ref>" and password ref "<password_ref>"
    Then an error message should be displayed
    And the error message should contain "<expectedMessageContains>"

    Examples:
      | testCaseId | username_ref    | password_ref   | expectedMessageContains |
      | TC_LDD_007 | invalid_user    | wrong_password | do not match            |
      | TC_LDD_008 | standard_user   | wrong_password | do not match            |
      | TC_LDD_012 | locked_out_user | wrong_password | do not match            |


