$(function() {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#order_id").val(res.id);
        $("#order_customer_id").val(res.customer_id);
        $("#order_status").val(res.status);
        $("#order_product_id").val(res.order_items[0].product_id);
        $("#order_name").val(res.order_items[0].name);
        $("#order_quantity").val(res.order_items[0].quantity);
        $("#order_price").val(res.order_items[0].price);
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#order_id").val("");
        $("#order_customer_id").val("");
        $("#order_product_id").val("");
        $("#order_name").val("");
        $("#order_quantity").val("");
        $("#order_price").val("");
        $("#order_status").val("received");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create an order
    // ****************************************

    $("#create-btn").click(function() {
        var customer_id = $("#order_customer_id").val();
        var product_id = $("#order_product_id").val();
        var item_name = $("#order_name").val();
        var qty = $("#order_quantity").val();
        var price = $("#order_price").val();
        var order_status = $("#order_status").val();

        var data = {
            "customer_id": customer_id,
            "status": order_status,
            "order_items": [{
                "product_id": product_id,
                "name": item_name,
                "quantity": qty,
                "price": price
            }]
        };

        var ajax = $.ajax({
            type: "POST",
            url: "/orders/",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res) {
            update_form_data(res);
            flash_message("Success");
        });

        ajax.fail(function(res) {
            flash_message(res.responseJSON.message);
        });
    });


    // ****************************************
    // Update an order
    // ****************************************

    $("#update-btn").click(function() {
        var order_id = $("#order_id").val();
        if (order_id === "") {
            flash_message("Order ID is required to update!");
            return;
        }
        var customer_id = $("#order_customer_id").val();
        var product_id = $("#order_product_id").val();
        var item_name = $("#order_name").val();
        var qty = $("#order_quantity").val();
        var price = $("#order_price").val();
        var order_status = $("#order_status").val();

        var data = {
            "customer_id": customer_id,
            "status": order_status,
            "order_items": [{
                "product_id": product_id,
                "name": item_name,
                "quantity": qty,
                "price": price
            }]
        };

        var ajax = $.ajax({
            type: "PUT",
            url: "/orders/" + order_id,
            contentType: "application/json",
            data: JSON.stringify(data)
        })

        ajax.done(function(res) {
            update_form_data(res);
            flash_message("Success");
        });

        ajax.fail(function(res) {
            flash_message(res.responseJSON.message);
        });

    });

    // ****************************************
    // Retrieve an order by Order ID
    // ****************************************

    $("#retrieve-btn").click(function() {
        var order_id = $("#order_id").val();

        var ajax = $.ajax({
            type: "GET",
            url: "/orders/" + order_id,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res) {
            update_form_data(res);
            flash_message("Success");
        });

        ajax.fail(function(res) {
            clear_form_data()
            flash_message(res.responseJSON.message);
        });

    });

    // ****************************************
    // Delete an order
    // ****************************************

    $("#delete-btn").click(function() {
        var order_id = $("#order_id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/orders/" + order_id,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res) {
            clear_form_data();
            flash_message("Order Deleted!");
        });

        ajax.fail(function(res) {
            clear_form_data();
            flash_message(res.responseJSON.message);
        });
    });

    // ****************************************
    // Cancel an order
    // ****************************************

    $("#cancel-btn").click(function() {
        var order_id = $("#order_id").val();

        var ajax = $.ajax({
            type: "PUT",
            url: "/orders/" + order_id + "/cancel",
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res) {
            update_form_data(res);
            flash_message("Order Canceled!");
        });

        ajax.fail(function(res) {
            clear_form_data();
            flash_message(res.responseJSON.message);
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function() {
        clear_form_data()
    });

    // ****************************************
    // Search for orders by status
    // ****************************************


    $("#search-btn").click(function() {
        var order_status = $("#order_status").val();

        var query_params = {
            "status": order_status
        };

        var ajax = $.ajax({
            type: "GET",
            url: "/orders?" + $.param(query_params),
            contentType: "application/json",
            data: ''
        });

        ajax.done(function(res) {
            //alert(res.toSource())
            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped"> <thead><tr><th>Orders</th></tr>');
            var header = '<tr>'
            header += '<th style="width:10%">ID</th>';
            header += '<th style="width:20%">Customer ID</th>';
            header += '<th style="width:20%">Product ID</th>';
            header += '<th style="width:20%">Name</th>';
            header += '<th style="width:13%">Quantity</th>';
            header += '<th style="width:10%">Price</th>';
            header += '<th style="width:10%">Status</th></tr>';
            $("#search_results").append(header);
            for (var i = 0; i < res.length; i++) {
                var order = res[i];
                var row = "<tr><td>" +
                    order.id + "</td><td>" +
                    order.customer_id + "</td><td>" +
                    order.order_items[0].product_id + "</td><td>" +
                    order.order_items[0].name + "</td><td>" +
                    order.order_items[0].quantity + "</td><td>" +
                    order.order_items[0].price + "</td><td>" +
                    order.status + "</td></tr>";
                $("#search_results").append(row);
            }

            $("#search_results").append('</table>');

            flash_message("Success")
        });

        ajax.fail(function(res) {
            flash_message(res.responseJSON.message);
        });
    });

});
