@performance @all
Feature: Performance Testing for SauceDemo

  @TC-MC_013 @PageLoad @Thresholds
  Scenario: Homepage and login controls are available
    Given the user navigates to the application home page
    Then the username field should be visible
    And the password field should be visible
    And the login button should be visible

  @TC-MC_014 @PageLoad @Interaction @Thresholds
  Scenario: Login interaction flow reaches inventory page
    Given the user navigates to the application home page
    When the user logs in with username ref "performance_glitch_user" and password ref "secret_sauce"
    Then the user should be on the inventory page
    And the product inventory should be displayed

  @TC-MC_015 @PageLoad @Thresholds
  Scenario: Glitch user can navigate to cart and checkout information page
    Given the user navigates to the application home page
    When the user logs in with username ref "performance_glitch_user" and password ref "secret_sauce"
    And the user adds the first product to the cart
    And the user navigates to the shopping cart
    And the user proceeds to checkout
    Then the continue button should be visible
