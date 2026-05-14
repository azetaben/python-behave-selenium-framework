@ui-test @inventory_item @all
Feature: Inventory item page interactions and validations
  As a user
  I want to validate inventory item page elements and actions
  So that product detail behavior is reliable end-to-end

  Background:
    Given the user has successfully logged in
    When the user clicks on the first product
    Then I am in "inventory-item.html" page

  @smoke @regression @TC_IIP_001
  Scenario: Verify inventory item core containers and element visibility
    Then the inventory item page core elements should be visible
    And the inventory item page core elements should be present
    And the inventory item element "secondary header" should be visible
    And the inventory item element "inventory item" should be present
    And the inventory item element "item image" should be visible
    And the inventory item element "item description" should be present
    And the inventory item description should contain "carry.allTheThings()"
    And the inventory item element "item price" should be visible
    And the inventory item element "add to cart button" should be present
    And the inventory item element "back to products button" should be visible
    And the user clicks "back to products" on the inventory item page
    Then I am in "inventory.html" page

  @smoke @regression @TC_IIP_002
  Scenario: Verify inventory item text values
    Then the inventory item name should be "Sauce Labs Backpack"
    And the inventory item description should contain "carry.allTheThings()"
    And the inventory item price should be "$29.99"

  @regression @TC_IIP_003
  Scenario: Click remove using dedicated remove step
    And the inventory item element "add to cart button" should be present
    And the user clicks "add to cart" button
    And the inventory item element "remove button" should be present
    When the user clicks "remove" on the inventory item page
    And the user clicks "back to products" on the inventory item page
    Then I am in "inventory.html" page

  @regression @TC_IIP_004
  Scenario: Click back to products using dedicated back step
    And the user clicks "back to products" on the inventory item page
    Then I am in "inventory.html" page

  @regression @TC_IIP_005
  Scenario: Click controls using text-based inventory item step
    And the inventory item element "remove button" should be present
    When the user clicks "remove" on the inventory item page
    And the user clicks "back to products" on the inventory item page
    Then I am in "inventory.html" page

