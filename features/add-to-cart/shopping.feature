Feature: Shopping Cart Functionality
  As a user
  I want to manage my shopping cart
  So that I can organize my purchases

  Background:
    Given the user has successfully logged in

  @smoke @e2e
  Scenario: Add single product to cart
    When the user adds the first product to the cart
    Then the cart should contain 1 item
    And the cart badge should display "1"

  @smoke @e2e
  Scenario: Add single product to cart by product name
    And the user should be on the "inventory.html" page
    When the user add a product item "Sauce Labs Backpack" to the cart
    And the user can see remove button for "Sauce Labs Backpack"
    Then the cart should contain 1 item
    And the cart badge should display "1"

  @smoke @e2e
  Scenario Outline: Add multiple product to cart by product names
    And the user should be on the "inventory.html" page
    When the user add "<productName>" to the cart:
    And the user can see remove button for "<productName>"
    Then the cart should contain 1 item
    Examples:
      | productName             |
      | Sauce Labs Backpack     |
      | Sauce Labs Bike Light   |
      | Sauce Labs Bolt T-Shirt |

  @smoke @e2e
  Scenario: Add multiple products to cart by product names
    And the user should be on the "inventory.html" page
    When the user adds the following products to the cart:
      | product_name            |
      | Sauce Labs Backpack     |
      | Sauce Labs Bike Light   |
      | Sauce Labs Bolt T-Shirt |
    Then the cart should contain 3 items


  @functional
  Scenario: Add multiple products to cart
    When the user adds the first product to the cart
    And the user adds the second product to the cart
    And the user adds the third product to the cart
    Then the cart should contain 3 items
    And the cart badge should display "3"

  @functional
  Scenario: Remove item from cart
    When the user adds the first product to the cart
    And the user navigates to the shopping cart
    When the user removes the first item from the cart
    Then the cart should be empty

  @functional
  Scenario: View product details
    When the user clicks on the first product
    Then the product details page should be displayed


  @functional
  Scenario: Click on a product by name, view details, add to cart and navigate to cart
    And the user should be on the "inventory.html" page
    When the user clicks on the product named "Sauce Labs Backpack"
    And the user should be on the "inventory-item.html" page
    And the user add the product "Sauce Labs Backpack" to the cart
    And the user add verify that the cart badge shows 1
    And the user can see remove button for "Sauce Labs Backpack"
    And the user can see "Back to products" button
    And the user clicks on the cart badge
    And I am in "cart.html" page
    Then the cart should contain 1 item

  @functional
  Scenario: Click on a product by name,view details and click on "Back to products" button
    And the user should be on the "inventory.html" page
    When the user clicks on the product named "Sauce Labs Backpack"
    And the user should be on the "inventory-item.html" page
    And the user should see product details for "Sauce Labs Backpack"
    And the user verify that the product name is "Sauce Labs Backpack"
    And the user add the product "Sauce Labs Backpack" to the cart
    And the user add verify that the cart badge shows "1"
    And the user can see remove button for "Sauce Labs Backpack"
    And the user can see "Back to products" button
    And the user clicks on the "Back to products" button
    And I am in "inventory.html" page

  @functional
  Scenario: Click on a product by name,view product details and remove from cart
    And the user should be on the "inventory.html" page
    When the user clicks on the product named "Sauce Labs Backpack"
    And the user should be on the "inventory-item.html" page
    And the user should see product details for "Sauce Labs Backpack"
    And the user verify that the product name is "Sauce Labs Backpack"
    And the user add the product "Sauce Labs Backpack" to the cart
    And the user add verify that the cart badge shows "1"
    And the user can see remove button for "Sauce Labs Backpack"
    And the user clicks on the remove button for "Sauce Labs Backpack"
    And the user clicks on the cart badge
    And I am in "cart.html" page
    Then the cart should be empty

  @regression
  Scenario: Cart persists after navigation
    When the user adds the first product to the cart
    And the user navigates to the shopping cart
    And the user navigates back to the inventory
    Then the cart badge should still show 1 item
