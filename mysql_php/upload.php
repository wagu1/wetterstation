<?php

if ( isset($_GET["m"])) { $m = $_GET["m"]; } else { exit(); }
if ( isset($_GET["t"])) { $t = $_GET["t"]; } else { exit(); }
if ( isset($_GET["p"])) { $p = $_GET["p"]; } else { exit(); }
if ( isset($_GET["f"])) { $f = $_GET["f"]; } else { exit(); }

$link = mysqli_connect("localhost", "xxxxxxx", "xxxxxxx", "$m");
if (mysqli_connect_errno()) {
	exit();
}

/* Prepare an insert statement */
$ins = "INSERT INTO $m (time, temperature, pressure, humidity) VALUES (now(),?,?,?);";
$stmt = mysqli_prepare($link, $ins);

mysqli_stmt_bind_param($stmt, "ddd", $t, $p, $f);

/* Execute tne statement */
mysqli_stmt_execute($stmt);

/* close statement */
mysqli_stmt_close($stmt);

/* close connection */
mysqli_close($link);  //  close connection 

?>
