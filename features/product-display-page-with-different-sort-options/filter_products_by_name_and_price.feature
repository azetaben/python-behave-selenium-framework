@ProductsDisplayedPage @ParallelRun @all @error_validation_tests
Feature: Product Sorting

  Background:
    Given the user navigates to the application home page

  @TC_PDP_001
  Scenario Outline: Inventory is shown for accepted users
    When the user logs in with username ref "<username_ref>" and password ref "<password_ref>"
    Then the user should be on the inventory page
    And the product inventory should be displayed
    Examples:
      | username_ref            | password_ref |
      | standard_user           | secret_sauce |
      | problem_user            | secret_sauce |
      | performance_glitch_user | secret_sauce |

  @TC_PDP_002 @error_validation_tests
  Scenario Outline: User can add product and see remove button
    When the user logs in with username ref "<username_ref>" and password ref "<password_ref>"
    And the user add a product item "Sauce Labs Backpack" to the cart
    Then the user can see remove button for "Sauce Labs Backpack"
    Examples:
      | username_ref            | password_ref |
      | standard_user           | secret_sauce |
      | performance_glitch_user | secret_sauce |

  @TC_PDP_002_1 @error_validation_tests
  Scenario: Problem user can still access inventory page
    When the user logs in with username ref "problem_user" and password ref "secret_sauce"
    Then the user should be on the inventory page

  @TC_PDP_003
  Scenario Outline: Cart badge updates after add for accepted users
    When the user logs in with username ref "<username_ref>" and password ref "<password_ref>"
    And the user adds the first product to the cart
    Then the cart badge should display "1"
    Examples:
      | username_ref            | password_ref |
      | standard_user           | secret_sauce |
      | performance_glitch_user | secret_sauce |

  @TC_PDP_004
  Scenario: Problem user locked-out check remains negative for invalid credentials
    When the user logs in with username ref "problem_user" and password ref "wrong_password"
    Then an error message should be displayed

