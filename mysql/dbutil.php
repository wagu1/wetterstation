<?php

  /*
   * Testprogramm zur Erzeugung einer Grafik 
   * mit der Bibliothek d3js.org
   * Die Daten werden aus einer Datenbank gelesen
   * DB:        wetter
   * Tabelle:   outdoor (id, time, temperature, pressure, humidity)
   *
   * Die Ausgabe der Daten am oberen Rand dient nur der Kontrolle
   * und kann durch auskommentieren der Zeile (direkt unterhalb von body) 
   * entfernt werden.
   *
   * Oktober2016
   */

$hostname = 'localhost';
$username = 'xxxxxxx';
$password = 'xxxxxxx';
$table    = 'outdoor';
$dbname   = "wetter";

$anzahl = 48;
if (isset($_GET["dauer"])) $anzahl = $_GET["dauer"]; 

// Verwendete SQL-Abfragen
// aktuelle Werte
$sql1 = "SELECT * from $table ORDER BY time DESC LIMIT 1";

if ($anzahl == 0) $a =""; else $a = " limit $anzahl";
$sql = "select * from (select * from $table order by time desc $a) as tab order by time";

// Daten für tabellarische Anzeige
$sql2 = "select * from $table order by time DESC $a";

// Mittelwert für den ausgewählten Zeitraum 
$sql2a = "select avg(t.temperature) as avgT, avg(t.pressure) as avgP, avg(t.humidity) as avgH from (SELECT * FROM $table ORDER BY time DESC $a) AS t";

// Zeit der letzten Messung
$sqlTime = "SELECT time FROM $table ORDER BY time DESC LIMIT 1";


function getJSON_Data() {
    global $hostname;
    global $username;
    global $password;
    global $dbname;
    global $sql;
    try {
        $dbh = new PDO("mysql:host=$hostname;dbname=$dbname", $username, $password);

        // *** The SQL SELECT statement *** /
        $sth = $dbh->prepare($sql);
        $sth->execute();

        // Fetch all of the remaining rows in the result set * /
        $result = $sth->fetchAll(PDO::FETCH_ASSOC);

        // ** close the database connection *** /
        $dbh = null;
    }
    catch(PDOException $e) {
        echo $e->getMessage();
    }

    $json_data = json_encode($result);
    return  $json_data;
}


function getJSON_Data1($sq) {
    global $hostname;
    global $username;
    global $password;
    global $dbname;
    global $sql;
    try {
        $dbh = new PDO("mysql:host=$hostname;dbname=$dbname", $username, $password);

        // *** The SQL SELECT statement *** /
        $sth = $dbh->prepare($sq);
        //$sth = $dbh->prepare("SELECT `temperatur`, `luftdruck`,`luftfeuchtigkeit`, `zeit` FROM `wetter` order by `zeit`");
        $sth->execute();

        // Fetch all of the remaining rows in the result set * /
        $result = $sth->fetchAll(PDO::FETCH_ASSOC);

        // ** close the database connection *** /
        $dbh = null;
    }
    catch(PDOException $e) {
        echo $e->getMessage();
    }

    $json_data = json_encode($result);
    return  $json_data;
}


function doQuery($sql) {
    global $hostname;
    global $username;
    global $password;
    global $dbname;
    $link = mysqli_connect($hostname, $username, $password, $dbname);
    if (mysqli_connect_errno()) {
	    printf("Connect failed: %s\n", mysqli_connect_error());
	    exit();
    }
    if ($result = mysqli_query($link, $sql)) {
	    return $result;
	}
    else return null;
}

function getLastTime() {
	global $sqlTime;
	$zeit = "";
	$result = doQuery($sqlTime);
	if ($result != null) {
		$obj = mysqli_fetch_object($result);
		$zeit = $obj->time;
	}
	mysqli_free_result($result);  // free result set
	return $zeit; 
}

function getAktuelleWerte($dauer) {
    global $sql1;
    global $sql2;
    global $sql2a;
    $html = "";
    $zeit = ""; // aktuelle Zeit
    $tA = "";   // aktuelle Temperatur
    $pA = "";
    $hA = "";
    // result hat max. 1 Wert
    $result = doQuery($sql1);
    $dauer = $dauer / 72;
    if ($dauer == 1) $dauer .= " Tag"; else  $dauer .= " Tage";

    if ($result != null) {
	    //while ($obj = mysqli_fetch_object($result)) {
	    $obj = mysqli_fetch_object($result);
	    $zeit = $obj->time;
	    $tA = $obj->temperature;
	    $pA = $obj->pressure;
	    $hA = $obj->humidity;
    }
    mysqli_free_result($result);  // free result set
    

    // Mittelwerte -- max. 1 Ergebniszeile
    $result1 = doQuery($sql2a);
    if ($result1 != null) {
	    $obj = mysqli_fetch_object($result1);
	    $avgT = $obj->avgT;
	    $avgP = $obj->avgP;
	    $avgH = $obj->avgH;
    }
    mysqli_free_result($result);  // free result set
    

    // jetzt min-max-Werte
    $tmin = 100; $tmax = -100;  // Temperatur
    $pmin = 2000; $pmax = 0;    // Luftdruck
    $lmin = 100; $lmax = 0;     // Luftfeuchtigkeit
    $result = doQuery($sql2);
    if ($result != null) {
	    while ($obj = mysqli_fetch_object($result)) {
		    if ($obj->temperature < $tmin)  $tmin = $obj->temperature;
		    if ($obj->temperature > $tmax)  $tmax = $obj->temperature;
		    if ($obj->pressure    < $pmin)  $pmin = $obj->pressure;
		    if ($obj->pressure    > $pmax)  $pmax = $obj->pressure;
		    if ($obj->humidity    < $lmin)  $lmin = $obj->humidity;
		    if ($obj->humidity    > $lmax)  $lmax = $obj->humidity;
	    }
	    mysqli_free_result($result);  // free result set
    }

    $html = "<p>letzter Messwert um &nbsp; <b>$zeit</b>";
    $html .= "&nbsp; &middot; &nbsp; Zeitraum: <b>$dauer</b></p>";
    $html = "<div class='messwert'> <div class='text'>°C</div> <div class='value'>";
    $html .= sprintf("<div class='aktuell'>T = %6.2f °C </div>",$tA);
    $html .= sprintf("<div class='min'>min = %6.2f °C </div>",$tmin);
    $html .= sprintf("<div class='max'>max = %6.2f °C </div>",$tmax);
    $html .= sprintf("<div class='avg'>avg = %6.2f °C </div>",$avgT);
    $html .= "</div> </div>";

    $html .= "<div class='messwert'> <div class='text'>Pa</div> <div class='value'>";
    $html .= sprintf("<div class='aktuell'>p = %6.2f hPa </div>",$pA);
    $html .= sprintf("<div class='min'>min = %6.2f hPa </div>",$pmin);
    $html .= sprintf("<div class='max'>max = %6.2f hPa </div>",$pmax);
    $html .= sprintf("<div class='avg'>avg = %6.2f hPa </div>",$avgP);
    $html .= "</div> </div>";

    $html .= "<div class='messwert'> <div class='text'>%</div> <div class='value'>";
    $html .= sprintf("<div class='aktuell'>h = %6.2f &#37; </div>",$hA);
    $html .= sprintf("<div class='min'>min = %6.1f &#37; </div>",$lmin);
    $html .= sprintf("<div class='max'>max = %6.1f &#37; </div>",$lmax);
    $html .= sprintf("<div class='avg'>avg = %6.1f &#37; </div>",$avgH);
    $html .= "</div> </div>";
    $html .= "<br clear='all' />";

    mysqli_close($link);  //  close connection 
    return $html;
}


function getDaten() {
    global $sql2;
    $html = "";
    $result = doQuery($sql2);

    $html .= "<pre>";
    $html .= sprintf ("%-20s   %-8s  %-10s      %-5s (&#037;) \n", "Zeit", "Temperatur","Luftdruck","Luftfeuchtigkeit");
    $html .=  "-----------------------------------------------------------------------\n";
    if ($result != null) {
        while ($obj = mysqli_fetch_object($result)) {
            $html .= sprintf ("%s   %6.2f °C   %8.2f hPa  %5d &#037; \n", $obj->time, $obj->temperature, $obj->pressure, $obj->humidity);
        }
        mysqli_free_result($result);  // free result set
    } else { $html .=  "NO - error bei query";}
    $html .=  "</pre>";
    mysqli_close($link);  //  close connection 
    return $html;
}


?>
