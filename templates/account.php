<!DOCTYPE HTML>
<html>

<head>
    <title>EduTrade</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
    <link rel="stylesheet" href="../css/dashboard/assets/css/main.css" />
    <!--===============================================================================================-->
    <link rel="icon" type="image/png" href="../images/icons/icon.png" />
    <!--===============================================================================================-->
    <!-- Scripts -->
    <script src="../css/dashboard/assets/js/jquery.min.js"></script>
    <script src="../css/dashboard/assets/js/jquery.scrolly.min.js"></script>
    <script src="../css/dashboard/assets/js/jquery.scrollex.min.js"></script>
    <script src="../css/dashboard/assets/js/browser.min.js"></script>
    <script src="../css/dashboard/assets/js/breakpoints.min.js"></script>

</head>

<body class="is-preload">

    <?php
    // $username = $_POST["username"];
    $username = "brydonmemelord123";
    ?>

    <!-- Header -->
    <div id="header">
        <div class="top">
            <!-- Logo -->
            <div id="logo">
                <h1 id="usernametop">Username</h1>
                <p id="credits">Balance</p>
            </div>

            <!-- Nav -->
            <nav id="nav">
                <ul>
                    <li><a href="index.html" id="index-link"><span class="icon solid fa-home">My dashboard</span></a></li>
                    <li><a href="holdings.php" id="holdings-link"><span class="icon solid fa-book-open">Holdings</span></a></li>
                    <li><a href="trading.html" id="trading-link"><span class="icon solid fa-search-dollar">Market</span></a></li>
                    <li><a href="#account" id="account-link"><span class="icon solid fa-user-circle">Account</span></a></li>
                </ul>
            </nav>

        </div>
    </div>

    <!-- Main -->
    <div id="main">

        <!-- Intro -->
        <section id="top" class="one cover dark">
            <div class="container">
                <h2>Here is your account details!</h2>
            </div>
        </section>

        <!-- Portfolio -->
        <section id="account" class="four">
            <div class="container">
                <h2>Edit Profile</h2>
                <hr>
                <h1 id="error">
                    <h1>


                        <!-- edit form column -->
                        <form id="accountform" class="form-horizontal" role="form">
                            <div class="form-group">
                                <label class="col-lg-3 control-label">Username:</label>
                                <div class="col-lg-8">
                                    <input id="username" class="form-control" type="text" value="">
                                </div>
                            </div>
                            <div class="
                            ">
                                <label class="col-lg-3 control-label">Name:</label>
                                <div class="col-lg-8">
                                    <input id="name" class="form-control" type="text" value="">
                                </div>
                            </div>
                            <div class="form-group">
                                <label class="col-lg-3 control-label">Age:</label>
                                <div class="col-lg-8">
                                    <input id="age" class="form-control" type="text" value="">
                                </div>
                            </div>
                            <div class="form-group">
                                <label class="col-lg-3 control-label">Email:</label>
                                <div class="col-lg-8">
                                    <input id="email" class="form-control" type="text" value="">
                                </div>
                            </div>
                            <div class="form-group">
                                <label class="col-lg-3 control-label">Institution:</label>
                                <div class="col-lg-8">
                                    <div class="ui-select">
                                        <input id="institution" class="form-control" type="text" value="">
                                    </div>
                                </div>
                            </div>
                            <div class="form-group">
                                <label class="col-md-3 control-label">Password:</label>
                                <div class="col-md-8">
                                    <input id="password" class="form-control" type="password" value="">
                                </div>
                            </div>
                            <div class="form-group">
                                <label class="col-md-3 control-label">Confirm password:</label>
                                <div class="col-md-8">
                                    <input id="confirmpassword" class="form-control" type="password">
                                </div>
                            </div>
                            <div class="form-group">
                                <label class="col-md-3 control-label"></label>
                                <div class="col-md-8">
                                    <input type="submit" class="btn btn-primary" value="Save Changes">
                                    <span></span>
                                    <input type="reset" id="reset" class="btn btn-default" value="Cancel">
                                </div>
                            </div>
                        </form>
            </div>
    </div>
    </section>

    <script type="text/javascript">
        async function getData(serviceURL) {
            let requestParam = {
                headers: {
                    "content-type": "charset=UTF-8"
                },
                mode: "cors",
                method: "GET",
            }

            try {
                const response = await fetch(serviceURL, requestParam);
                data = await response.json();
                // console.log(data);
            } catch (error) {
                console.error(error);
                "Currently unable to display your holdings";
                $("form").hide();
                document.getElementById("error").textContent = "Unable to display user account details.";
            }
            username = data.username;
            document.getElementById("username").value = username;
            document.getElementById("usernametop").textContent = username;
            name = data.name;
            document.getElementById("name").value = name;
            age = data.age;
            document.getElementById("age").value = age;
            email = data.email;
            document.getElementById("email").value = email;
            institution = data.institution;
            document.getElementById("institution").value = institution;
            password = data.password;
            document.getElementById("password").value = password;
            credits = data.credit;
            document.getElementById("credits").textContent = "Credits =" + credits;
        }

        $(function() {
            var serviceURL = "http://localhost:5010/user/" + "<?php echo $username ?>";
            user = getData(serviceURL);
        });

        async function postData(serviceURL, requestBody) {
            var requestParam = {
                headers: {
                    "content-type": "charset=UTF-8; application/json;"
                },
                mode: 'cors', // other options: no-cors, etc.
                method: 'POST',
                body: JSON.stringify(requestBody)
            }
            try {
                const response = await fetch(serviceURL, requestParam);
                data = await response.json();
                console.log(data);
            } catch (error) {
                console.error(error);
            }
        }
        $("#accountform").submit(function() {
            //     var username = $('#username').val();
            // console.log(username)
            var serviceURL = "http://localhost:5000/update_user/" + <?php echo $username ?>;
            var requestBody = {
                username: data.username,
                name: data.name,
                age: data.age,
                email: data.email,
                institution: data.institution,
                password: data.password
            };
            postData(serviceURL, requestBody);
        });
    </script>

    <script src="../css/dashboard/assets/js/util.js"></script>
    <script src="../css/dashboard/assets/js/main.js"></script>
    <script src="https://canvasjs.com/assets/script/canvasjs.min.js"></script>

</body>

</html>