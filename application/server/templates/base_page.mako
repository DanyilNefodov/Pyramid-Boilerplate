<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <title>
        <%block name="title">
        </%block>
    </title>
    <meta content="width=device-width, initial-scale=1.0" name="viewport">
    <meta content="" name="keywords">
    <meta content="" name="description">

    <!-- Favicons -->
    <link href="img/favicon.png" rel="icon">
    <link href="img/apple-touch-icon.png" rel="apple-touch-icon">

    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css?family=Inconsolata:400,700|Raleway:400,700&display=swap"
        rel="stylesheet">

    <!-- Bootstrap CSS File -->
    <link rel="stylesheet" href="${request.static_url('server:static/vendor/bootstrap/css/bootstrap.min.css')}"/>

    <!-- Template Main CSS File -->
    <link rel="stylesheet" href="${request.static_url('server:static/css/style.css')}"/>
    <%block name="css">
    </%block>
</head>

<body>
    <main id="main">
        <%block name="main">
        </%block>
    </main>

    <!-- jQuery -->
    <script src="${request.static_url('server:static/js/jquery.min.js')}"></script>

    <%block name="js">
    </%block>
</body>
</html>
