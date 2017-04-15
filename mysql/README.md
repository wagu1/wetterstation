# Web- und Datenbankserver

Voraussetzung: Es steht ein Webserver und ein Datenbankserver zur Verfügung.
Getestet wurde die Konfiguration mit 

- MYSQL
- APACHE2

## Dateien

```
 info.txt ..... diese Datei
 chart.js ..... Javascriptdatei für Grafiken
 dbutil.php ... Datenbankverbindung
 upload.php ... php-Datei zum Eintragen eines neuen Messwertes
 wetter.css ... CSS-Formatdatei
 wetter.php ... Anzeigeseite
 wetter.sql ... Befehle zum Anlegen der Tabellen
```

# Datenbank anlegen:

Die Datenbank 'wetter' enthält für jeden Sensor eine Tabelle, deren Aufbau
identisch ist:

```
CREATE TABLE `indoor` (
	`id`          int(11)    NOT NULL AUTO_INCREMENT,
	`time`        timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	`temperature` float(4,2) NOT NULL,
	`pressure`    float(6,2) NOT NULL,
	`humidity`    float(3,1) NOT NULL,
	PRIMARY KEY (`id`)
	) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8
```


# Neue Messwerte eintragen

Das Python-Programm ruft die URL mit Parametern auf:
```
<server>/upload.php?m=table&t=temp&p=pres&h=hum
     table = indoor oder outdoor (String
     temp  = Temperatur          (double)
     pres  = Luftdruck           (double)
     hum   = Luftfeuchtigkeit    (double)
```
Auf dem Server fügt die Auswertung dieser URL die Daten in die Datenbank ein.

Auf diese Art werden die Daten nur lokal auf dem Server verarbeitet. Ein
externer Zugriff auf die Datenbank (direkt vom Raspberry Pi) würde ein
Sicherheitsrisiko für die Datenbank darstellen.

# Messwerte abrufen

Die grafische Anzeige basiert auf https://d3js.org/d3.v3.min.js.
In der Datei **chart.js** werden dazu zwei Funktionen definiert,
die für die Anzeige aufgerufen werden.

```
  // ************************************************************
  // Funktion zur Erzeugung einer Grafik (Linie)
  // Die Daten müssen zwei Spalten enthalten: (zeit | value)
  //
  // Parameter:
  //  o titel    Diagrammtitel oben
  //  o sql      wird z.Zt. nicht genutzt
  //  o textX    Beschrfitung der x-Achse
  //  o textY    Beschriftung der y-Achse  
  //  o breite   Breite des Diagramms
  //  o hoehe    Höhe des Diagramms
  //  o data     Daten im JSON-Format
  //  o scaleY   0=automatisch skalieren, 1=Prozent 0..100
  //  o units    Einheiten für die Tooltipps
  //  o id       id in css-Klasse
  //             #id  ............ Breite, Rand/farbe)
  //             #id .title ...... Farbe, Größe des Titels
  //             #id .y .......... Farbe der y-Beschriftung
  //             #id .linecolor .. Linienfarbe
  //             #id .tooltip .... Frarbe Tooltipps
  // ***********************************************************

  function showDiagram1Line(titel, sql, textX, textY, breite, hoehe, 
                            data, scaleY, units, id) 

  // ************************************************************
  // Funktion zur Erzeugung einer Grafik (2 Linien)
  // Die Daten müssen drei Spalten enthalten: (zeit | value1 | value2 )
  //
  // Parameter:
  //  o titel    Diagrammtitel oben
  //  o data     Daten im JSON-Format
  //  o textX    Beschrfitung der x-Achse
  //  o textY1   Beschriftung der y1Achse (links)
  //  o textY2   Beschriftung der y1-Achse (rechts)
  //  o breite   Breite des Diagramms
  //  o hoehe    Höhe des Diagramms
  //  o scaleY1  0=automatisch skalieren, 1=Prozent 0..100 value1
  //  o scaleY2  0=automatisch skalieren, 1=Prozent 0..100 value2
  //  o units1   Einheiten für die Tooltipps value1
  //  o units2   Einheiten für die Tooltipps value2
  //  o id       id in css-Klasse
  //             #id  ............ Breite, Rand/farbe)
  //             #id .title ...... Farbe, Größe des Titels
  //             #id .y1 ......... Farbe der y-Beschriftung value1
  //             #id .y2 ......... Farbe der y-Beschriftung value2
  //             #id .linecolor1 . Linienfarbe value1
  //             #id .linecolor2 . Linienfarbe value2
  //             #id .tooltip .... Farbe Tooltipps
  // ***********************************************************

  function showDiagram2Lines(titel, data, textX, textY1, textY2, breite,
                             hoehe, scaleY1, scaleY2, units1, units2, id)
```

Die Anzeige soll exemplarisch an der Temperatur (1 Linie) beschrieben werden.
Die Box um den Graphen mit farbigem Titel kann über css realisiert werden.

<div id="graphTemperature"> ... </div>

FÜr das Auslesen der Daten wird die Funktion **getJSON_Data1($sqlT)** verwendet,
die in **dbutil.php** definiert ist. Das Ergebnis wird in 'data' gespeichert.

```
<script>
    <?php
        $json_data = getJSON_Data1($sqlT);
        echo "data=".$json_data.";"
    ?>
    showDiagram1Line("Temperatur (in °C)","","Zeit",
                   "", 600, 300, data, 0, "°C",
                   "#graphTemperature");
</script>
```

Der SQL-Befehl zur Abfrage:

```
$sqlT = "SELECT   time AS Zeit, 
                  temperature AS value 
         FROM     (SELECT * FROM outdoor ORDER BY time DESC) AS tab 
         ORDER BY Zeit";
```     

