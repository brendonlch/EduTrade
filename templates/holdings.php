<!DOCTYPE HTML>

<html>

<head>

    <title>EduTrade</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
    <link rel="stylesheet" href="../css/dashboard/assets/css/main.css" />

    <!--===============================================================================================-->
    <link rel="icon" type="image/png" href="../css/dashboard/images/icon.png" />
    <!-- Scripts -->
    <script src="../css/dashboard/assets/js/jquery.min.js"></script>
    <script src="../css/dashboard/assets/js/jquery.scrolly.min.js"></script>
    <script src="../css/dashboard/assets/js/jquery.scrollex.min.js"></script>
    <script src="../css/dashboard/assets/js/browser.min.js"></script>
    <script src="../css/dashboard/assets/js/breakpoints.min.js"></script>
    <script src="../css/dashboard/assets/js/util.js"></script>
    <script src="../css/dashboard/assets/js/main.js"></script>
    <script src="https://canvasjs.com/assets/script/canvasjs.min.js"></script>
</head>

<body class="is-preload">
    <?php
    // $username = $_POST['username'];
    $username = "lol";
    ?>
    <!-- Header -->
    <div id="header">

        <div class="top">

            <!-- Logo -->
            <div id="logo">
                <span class="image avatar48"><img src="../css/dashboard/images/earn.png" alt="" /></span>
                <h1 id="title">BrydonMemeLord</h1>
                <p>Balance &nbsp; $e-dollar</p>
            </div>

            <!-- Nav -->
            <nav id="nav">
                <ul>
                    <li><a href="#top" id="top-link"><span class="icon solid fa-home">My dashboard</span></a></li>
                    <li><a id="holdings-link"><span class="icon solid fa-book-open">Holdings</span></a></li>
                    <li><a href="stocks.html" id="about-link"><span class="icon solid fa-search-dollar">Market</span></a>
                    </li>
                    <li><a href="account.php" id="contact-link"><span class="icon solid fa-user-circle">Account</span></a>
                    </li>
                </ul>
            </nav>

        </div>
    </div>

    <!-- Main -->
    <div id="main">

        <!-- Intro -->
        <section id="top" class="one cover dark">
            <div class="container">
                <h2>These are the stocks you currently own! </h2>
            </div>
        </section>

        <!-- Portfolio -->
        <section id="holdings" class="two">
            <div class="container">
                <h2>Holdings</h2><br>
                <table id="allHoldings">
                    <tr>
                        <th>Symbol</th>
                        <th>Name</th>
                        <th>Qty</th>
                        <th>Price Bought ($)</th>
                        <th>Current Price ($)</th>
                        <th>Unrealised P/L</th>
                    </tr>
                    <script>
                        // anonymous async function
                        // - using await requires the function that calls it to be async

                        $(async () => {

                            let requestParam = {
                                headers: {
                                    "content-type": "charset=UTF-8"
                                },
                                mode: 'cors', // allow cross-origin resource sharing
                                method: 'GET',
                            }
                            // Change serviceURL to your own
                            var serviceURL = "http://127.0.0.1:5010/holdings/<?php echo $username ?>";

                            try {
                                const response =
                                    await fetch(serviceURL, requestParam);
                                const data = await response.json();
                                var holdings = data.holdings; //the arr is in data.books of the JSON data

                                // array or array.length are false
                                if (!holdings || !holdings.length) {
                                    showError('You have no holdings!')
                                } else {
                                    // for loop to setup all table rows with obtained book data
                                    var rows = "";
                                    for (const stock of holdings) {
                                        let stockDetails = await getLatestStock(stock.symbol);
                                        var unrealised = (stockDetails.price - stock.buyprice) * stock.qty;

                                        var eachRow = "<td>" + stock.symbol + "</td>" +
                                            "<td>" + stockDetails.stockname + "</td>" +
                                            "<td>" + String(stock.qty) + "</td>" +
                                            "<td>" + String(stock.buyprice) + "</td>" +
                                            "<td>" + String(stockDetails.price) + "</td>";

                                        if (unrealised < 0) {
                                            eachRow = eachRow + "<td style='color:#e63e32'>" + unrealised.toFixed(2) + "</td>";
                                        } else {
                                            eachRow = eachRow + "<td style='color:#4caf50'>" + unrealised.toFixed(2) + "</td>";
                                        }
                                        rows += "<tr>" + eachRow + "</tr>";
                                    }
                                    // add all the rows to the table
                                    $('#allHoldings').append(rows);
                                }
                            } catch (error) {
                                var rows = "<tr><td colspan='6'>Currently unable to display your holdings.</td></tr>";
                                $('#allHoldings').append(rows);
                                // Errors when calling the service; such as network error,
                                // service offline, etc
                                showError
                                    ('There is a problem retrieving holdings data, please try again later.<br />' + error);

                            } // error

                        });
                    </script>
                </table>


            </div>
            <a href="#alerts" id="newAlert">Set an alert so you know when you buy / sell!<br><i class="fas fa-angle-double-down fa-2x"></i></a>
            <!--
                    Alerts requires user to add symbol, price and alert type (< / >)
                 -->
            <div>
            </div>
        </section>

        <section id="alerts" class="three">
            <div class="container">
            <script>
                    async function getStockSymbols() {
                        let requestParam = {
                            headers: {
                                "content-type": "charset=UTF-8"
                            },
                            mode: 'cors', // allow cross-origin resource sharing
                            method: 'GET',
                        }
                        // Change serviceURL to your own
                        var serviceURL = "http://127.0.0.1:6010/stock/symbol";

                        try {
                            const response =
                                await fetch(serviceURL, requestParam);
                            const data = await response.json();
                            var holdings = data.holdings; //the arr is in data.books of the JSON data

                            // array or array.length are false
                            if (!holdings || !holdings.length) {
                                showError('You have no holdings!')
                            } else {
                                // for loop to setup all table rows with obtained book data
                                var options = "";
                                for (const stock of holdings) {
                                    options = options + `<option value="${stock.symbol}">< "${stock.symbol}"</option>`;
                                    console.log(options);
                                }
                                // add all the rows to the table
                                console.log(options);
                                document.getElementById('symbol').innerHTML = rows;
                            }
                        } catch (error) {
                            // Errors when calling the service; such as network error,
                            // service offline, etc
                            showError
                                ('There is a problem retrieving stock symbols from the database. Please try again later.<br />' + error);

                        } // error

                    }
                </script>  
                <h2>Alerts</h2><br>
                <form class="form-horizontal" role="form">
                    <label class="col-lg-3 control-label">Symbol:</label><select id="symbol" name="symbol">
                        <script>
                            let symbols = await getStockSymbols();
                        </script>
                    </select>
                    <label class="col-lg-3 control-label">Price:</label><input type="text" id="quantity" name="quantity" />
                    <label class="col-lg-3 control-label">Alert Type:</label><select id="type" name="type">
                        <option value="less">
                            < "less than" </option> <option value="more">> "more than"</i>
                        </option>
                    </select>
                </form>

            </div>
        </section>

        <!-- <section id="another" class="two">
            <div class="container">
                <h2>Another Section</h2><br>
            </div>
        </section> -->

        <!-- Footer -->
        <!-- <div id="footer"> -->

    </div>

    <script>
        // $(function () {
        //     $("#alerts").hide();
        // })

        // Helper function to display error message
        function showError(message) {
            // Hide the table and button in the event of error
            $('#booksTable').hide();
            $('#addBookBtn').hide();

            // Display an error under the main container
            $('#main-container')
                .append("<label>" + message + "</label>");
        }

        async function getLatestStock(symbol) {
            let requestParam = {
                headers: {
                    "content-type": "charset=UTF-8"
                },
                mode: 'cors', // allow cross-origin resource sharing
                method: 'GET',
            }
            var serviceURL = "http://127.0.0.1:6010/stock/" + symbol;

            try {
                const response =
                    await fetch(serviceURL, requestParam);
                const data = await response.json();
                // array or array.length are false
                if (data) {
                    return data;
                } else {
                    showError('No such stock!')
                }
            } catch (error) {
                // Errors when calling the service; such as network error,
                // service offline, etc
                showError
                    ('There is a problem retrieving holdings data, please try again later.<br />' + error);

            } // error
        }

        $("#newAlert").click(function() {
            $("#alerts").show();
        })
    </script>


</body>

</html>