Feature: The order store service back-end
  As an Order Store Owner
  I need a RESTful catalog service
  So that I can keep track of all my orders

  Background:
    Given the following orders
      | customer_id | product_id | name         | quantity | price | status   |
      | 1           | 1          | protein bars | 2        | 18.25 | received |
      | 2           | 2          | airpods      | 1        | 199   | received |
      | 3           | 3          | notebook     | 1        | 5.49  | shipped |

  Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "" in the title
    # TODO update to below line once UI is implemented
    # Then I should see "Orders REST API Service" in the title
    And I should not see "404 Not Found"


#Scenario: Create an order


#Scenario: List all orders


#Scenario: List certain orders


#Scenario: Update an order


#Scenario: Read an order


#Scenario: Delete an Order


#Scenario: Cancel an order
