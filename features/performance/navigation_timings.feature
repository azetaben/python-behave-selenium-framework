@performance
Feature: Navigation timing metrics

  Scenario: Collect navigation flow checkpoints
    Given the user navigates to the application home page
    When the user logs in with username ref "standard_user" and password ref "secret_sauce"
    Then the user should be on the inventory page
    When the user navigates to the shopping cart
    Then I am in "cart.html" page

