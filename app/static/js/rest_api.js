$(function() {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#order_id").val(res.id);
        $("#customer_id").val(res.customer_id);
        $("#order_date").val(res.order_date);
        $("#order_status").val(res.status);
        $("item_name").val(res.order_items['name']);
        $("product_id").val(res.order_items['product_id']);
        $("item_qty").val(res.order_items['quantity']);
        $("item_price").val(res.order_items['price']);
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#order_id").val("");
        $("#customer_id").val("");
        $("#item_name").val("");
        $("#product_id").val("");
        $("#item_qty").val("");
        $("#item_price").val("");
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

        var customer_id = $("#customer_id").val();
        var order_status = $("#order_status").val();
        var item_name = $("#item_name").val();
        var qty = $("#item_qty").val();
        var price = $("#item_price").val();
        var product_id = $("#product_id").val();

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
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res) {
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update order status
    // ****************************************

    $("#update-btn").click(function() {

        var order_id = $("#order_id").val();
        var status = $("#order_status").val();

        var data = {
            "status": status,
            "order_id": order_id
        };

        var ajax = $.ajax({
            type: "PUT",
            url: "/orders/" + order_id,
            contentType: "application/json",
            data: JSON.stringify(data)
        })

        ajax.done(function(res) {
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res) {
            flash_message(res.responseJSON.message)
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
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res) {
            clear_form_data()
            flash_message(res.responseJSON.message)
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
            clear_form_data()
            flash_message("Order ID [" + res.order_id + "] has been deleted!")
        });

        ajax.fail(function(res) {
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function() {
        $("#order_id").val("");
        $("#customer_id").val("");
        $("#order_date").val("");
        $("#item_name").val("");
        $("#product_id").val("");
        $("#item_qty").val("");
        $("#item_price").val("");
        clear_form_data()
    });

    // ****************************************
    // Search for an order
    // ****************************************

    $("#search-btn").click(function() {

        var order_id = $("#order_id").val();
        var customer_id = $("#customer_id").val();

        var queryString = ""

        if (status) {
            queryString += 'status=' + status
        }
        if (category) {
            if (queryString.length > 0) {
                queryString += '&category=' + category
            } else {
                queryString += 'category=' + category
            }
        }
        if (available) {
            if (queryString.length > 0) {
                queryString += '&available=' + available
            } else {
                queryString += 'available=' + available
            }
        }

        var ajax = $.ajax({
            type: "GET",
            url: "/orders?" + queryString,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res) {
            //alert(res.toSource())
            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped">');
            var header = '<tr>'
            header += '<th style="width:10%">Order ID</th>'
            header += '<th style="width:40%">Customer ID</th>'
            header += '<th style="width:40%">Status</th>'
            $("#search_results").append(header);
            for (var i = 0; i < res.length; i++) {
                var order = res[i];
                var row = "<tr><td>" + order.order_id + "</td><td>" + order.customer_id + "</td><td>" + order.status + "</td>";
                $("#search_results").append(row);
            }

            $("#search_results").append('</table>');

            flash_message("Success")
        });

        ajax.fail(function(res) {
            flash_message(res.responseJSON.message)
        });

    });

})
