Feature: The order store service back-end
  As an Order Store Owner
  I need a RESTful catalog service
  So that I can keep track of all my orders

  Background:
    Given the following orders
      | customer_id | product_id | name         | quantity | price | status   |
      | 1           | 1          | protein bars | 2        | 18.25 | received |
      | 2           | 2          | airpods      | 1        | 199   | received |
      | 3           | 3          | notebook     | 1        | 5.49  | shipped  |
      | 3           | 4          | shirt        | 1        | 23.50 | received |

  Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Order RESTful Service" in the title
    And I should not see "404 Not Found"

  Scenario: Create an order
    When I visit the "Home Page"
    And I set the "customer_id" to "1"
    And I set the "product_id" to "1"
    And I set the "name" to "protein bars"
    And I set the "quantity" to "2"
    And I set the "price" to "18.25"
    And I set the "status" to "received"
    And I press the "Create" order button
    Then I should see the message "Success"

#Scenario: List all orders


#Scenario: List certain orders


#Scenario: Update an order


  Scenario: Read an order
    When I visit the "Home Page"
    And I set the "ID" to "1"
    And I press the "retrieve" order button
    Then I should see "1" in the "customer_id" field
    Then I should see "1" in the "product_id" field
    Then I should see "protein bars" in the "name" field
    Then I should see "2" in the "quantity" field
    Then I should see "18.25" in the "price" field
    Then I should see "received" in the "status" field
    Then I should see the message "Success"

  Scenario: Delete an Order
    When I visit the "Home Page"
    And I set the "ID" to "4"
    And I press the "delete" order button
    Then I should see the message "Order Deleted!"


  Scenario: Cancel an Order
    When I visit the "Home Page"
    And I set the "ID" to "1"
    And I press the "cancel" order button
    Then I should see the message "Order Canceled!"
    Then I should see "canceled" in the "Status" field
