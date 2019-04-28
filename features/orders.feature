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


#Scenario: Create an order


#Scenario: List all orders


#Scenario: List certain orders


#Scenario: Update an order


#Scenario: Read an order


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
