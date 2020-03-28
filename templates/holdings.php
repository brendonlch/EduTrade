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
                    <li><a href="#settings" id="contact-link"><span class="icon solid fa-user-circle">Account</span></a>
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
                <h2>Holdings</h2><br><br>
                <table id="allHoldings">
                    <tr>
                        <th>Symbol</th>
                        <th>Name</th>
                        <th>Qty</th>
                        <th>Price Bought ($)</th>
                        <th>Current Price ($)</th>
                    </tr>
                    <script>
                        // anonymous async function
                        // - using await requires the function that calls it to be async
                        $ (async () => {
                            // Change serviceURL to your own
                            var serviceURL = "http://127.0.0.1:5000/holdings/<?php echo $username ?>";

                            try {
                                const response =
                                    await fetch(
                                        serviceURL, { method: 'GET' }
                                    );
                                const data = await response.json();
                                var holdings = data.holdings; //the arr is in data.books of the JSON data

                                // array or array.length are false
                                if (!holdings || !holdings.length) {
                                    showError('You have no holdings!')
                                } else {
                                    // for loop to setup all table rows with obtained book data
                                    var rows = "";
                                    for (const stock of holdings) {

                                        eachRow =
                                            "<td>" + stock.symbol + "</td>" +
                                            "<td>" + "NEED TO ADD NAME" + "</td>" +
                                            "<td>" + stock.qty + "</td>" +
                                            "<td>" + stock.buyprice + "</td>" +
                                            "<td>" + "NEED TO ADD CURRENT PRICE" + "</td>";
                                        rows += "<tr>" + eachRow + "</tr>";
                                    }
                                    // add all the rows to the table
                                    $('#allHoldings').append(rows);
                                }
                            } catch (error) {
                                // Errors when calling the service; such as network error,
                                // service offline, etc
                                showError
                                    ('There is a problem retrieving holdings data, please try again later.<br />' + error);

                            } // error
                        });
                    </script>
                    <tr>
                        <td>GGL</td>
                        <td>Google</td>
                        <td>200</td>
                        <td class="center">15.00</td>
                        <td class="center">20.00</td>
                    </tr>
                    <!-- <tr>
                        <td colspan="6" align="right"><a href=""><i class="fas fa-angle-double-right fa-2x"></i></a>
                        </td>
                    </tr> -->
                </table>
            </div>
        </section>

        <section id="news" class="three">
            <div class="container">
                <h2>Market</h2><br>
                
            </div>

            <!-- Footer -->
            <!-- <div id="footer"> -->

    </div>

    <script>
        // Helper function to display error message
        function showError(message) {
            // Hide the table and button in the event of error
            $('#booksTable').hide();
            $('#addBookBtn').hide();

            // Display an error under the main container
            $('#main-container')
                .append("<label>" + message + "</label>");
        }
    </script>
</body>

</html>