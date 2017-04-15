<!DOCTYPE html>
<head>
<meta charset="utf-8">
<link rel="stylesheet" type="text/css" href="wetter.css">
</head>
<body>


<script src="https://d3js.org/d3.v3.min.js"></script> 
<script src="chart.js"></script>

<br />


<?php
  /*
   * Anzeige der Messdaten unter Verwendung der Bibliothek d3js.org
   * Die Daten werden aus einer Datenbank gelesen
   * Tabelle:   wetter (temperatur, luftdruck, lueftfeuchtigkeit, zeit)
   *
   * Die Ausgabe der Daten am oberen Rand dient nur der Kontrolle
   * und kann durch auskommentieren der Zeile (direkt unterhalb von body) 
   * entfernt werden.
   * 
   * Folgende Dateien werden benötigt:
   *   o Bibliothek d3.v3.min.js (wird automatisch geladen)
   *   o Diese Datei (Hauptseite)
   *   o dbutil (Datenbankzugriffsfunktionen)
   *   o wetter.css
   *   o chart.js
   *
   * Oktober 2016
   */
   
    include_once("./dbutil.php");
    
    $anzahl = 72;
    if (isset($_GET["dauer"])) $anzahl = $_GET["dauer"]; 
    $dauer = $anzahl;
    
    $aktuelleWerte = getAktuelleWerte($dauer);
    $server = "https://xxxxxxx";
    $tab = "outdoor";
    $webpage = "http://$server/wetter.php";


    /*** The SQL SELECT statement ***/
    if ($anzahl == 0) $a =""; else $a = " limit $anzahl";
    $sqlTP = "select time as zeit, temperature as value1, pressure as value2 from (select * from i$tab order by time desc $a) as tab order by zeit";
    $sqlT = "select time as zeit, temperature as value from (select * from $tab order by time desc $a) as tab order by zeit";
    $sqlP = "select time as zeit, pressure as value    from (select * from $tab order by time desc $a) as tab order by zeit";
    $sqlH = "select time as zeit, humidity as value    from (select * from $tab order by time desc $a) as tab order by zeit";
    $sql  = "select * from $tab order by time DESC $a";
    
?>

<div style="float:left;padding-left:10px;padding-right:10px; padding-top:10px;">

<b style="font-size:1.8em; color:#57ABFD">Wetterstation HOME</b> 
<!--
<p>
letzte Messung um <b><?php echo getLastTime(); ?> </b>
</p>
-->

<br /> <br /> &nbsp;

Zeitraum: 
  <select name="dauer"  onchange="window.open(this.options[this.selectedIndex].value,'_top')">
    <option VALUE="<?php echo $webpage; ?>?dauer=72"  <?php if ($anzahl==72)   echo "selected"; ?> >1 Tag</option>
    <option VALUE="<?php echo $webpage; ?>?dauer=144" <?php if ($anzahl==144)  echo "selected"; ?> >2 Tage</option>
    <option VALUE="<?php echo $webpage; ?>?dauer=216" <?php if ($anzahl==216)  echo "selected"; ?> >3 Tage</option>
    <option VALUE="<?php echo $webpage; ?>?dauer=288" <?php if ($anzahl==288)  echo "selected"; ?> >4 Tage</option>
    <option VALUE="<?php echo $webpage; ?>?dauer=360" <?php if ($anzahl==360)  echo "selected"; ?> >5 Tage</option>
    <option VALUE="<?php echo $webpage; ?>?dauer=432" <?php if ($anzahl==432)  echo "selected"; ?> >6 Tage</option>
    <option VALUE="<?php echo $webpage; ?>?dauer=504" <?php if ($anzahl==504)  echo "selected"; ?> >1 Woche</option>
    <option VALUE="<?php echo $webpage; ?>?dauer=1008"<?php if ($anzahl==1008) echo "selected"; ?> >2 Wochen</option>
    <option VALUE="<?php echo $webpage; ?>?dauer=0"   <?php if ($anzahl==  0)  echo "selected"; ?> >alle Werte</option>
  </select>
</div>

<div style="float:left;padding-left:10px;">

<p>
letzte Messung um<br />
<b><?php echo getLastTime(); ?> </b>
<br />
<br />
Sensorstandort:
<br />
<b>außerhalb</b>
</p>
</div>

<div style="float:left;padding-left:20px;">
<?php  echo $aktuelleWerte; ?>
</div>

<br clear="all">
<br />

<div id="graphTemperaturePressure">
<script>
    <?php 
        $json_data = getJSON_Data1($sqlTP);
        echo "data=".$json_data.";" 
    ?>
    showDiagram2Lines("Temperatur und Luftdruck", data, "textX", "Temperatur (°C)", "Luftdruck (hPa)", 1200, 400, 0, 0, "°C", "hPa", "#graphTemperaturePressure");
</script>
</div>

<br /> 
    

<div style="float:left;">
<div id="graphTemperature">
<script>
    <?php 
        $json_data = getJSON_Data1($sqlT);
        echo "data=".$json_data.";" 
    ?>
    showDiagram1Line("Temperatur (in °C)","","Zeit", "", 600, 300, data, 0, "°C", "#graphTemperature");
</script>
</div>
</div>

<div style="float:left;margin-left:10px;">
<div id="graphPressure">
<script>
    <?php 
        $json_data = getJSON_Data1($sqlP);
        echo "data=".$json_data.";" 
    ?>
    showDiagram1Line("Luftdruck (in hPa)","","Zeit", "", 600, 300, data, 0, "hPa", "#graphPressure");
</script>
</div>
</div>

<br clear="all" />

<br />
<div style="float:left;">
<div id="graphHumidity">
<script>
    <?php 
        $json_data = getJSON_Data1($sqlH);
        echo "data=".$json_data.";" 
    ?>
    showDiagram1Line("Luftfeuchtigkeit (in %)","","Zeit", "", 600, 300, data, 1, "%", "#graphHumidity");
</script>
</div>
</div>

<br clear="all">

<p><b>Gemessene Werte:</b></p>
<?php
    echo getDaten();
?>

</body>
</html>
