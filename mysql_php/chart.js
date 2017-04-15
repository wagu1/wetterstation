// ***********************************************************
// 
// Globale Einstellungen
// gültig für alle Diagramme
//
// ***********************************************************

// Parse the date / time
var parseDate = d3.time.format("%Y-%m-%d %H:%M:%S").parse;

// Einstellung auf deutsche Formate
var de_DE = d3.locale({
  "decimal": ",",
  "thousands": ".",
  "grouping": [3],
  "currency": ["", "€"],
  "dateTime": "%a %b %e %X %Y",
  "date": "%d.%m.%Y",
  "time": "%H:%M:%S",
  "periods": ["AM", "PM"],
  "days": ["Sonntag", "Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag"],
  "shortDays": ["So", "Mo", "Di", "Mi", "Do", "Fr", "Sa"],
  "months": ["Januar", "Februar", "März", "April", "Mai", "Juni", "July", "August", "September", "Oktober", "November", "Dezember"],
  "shortMonths": ["Jan", "Feb", "Mrz", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"]
});

// Zeit auf deutsches Format einstellen
d3.time.format = de_DE.timeFormat;

// Benutzerdefiniertes Zeitformat
var customTimeFormat = d3.time.format.multi([
  [".%L", function(d) { return d.getMilliseconds(); }],
  [":%S", function(d) { return d.getSeconds(); }],
  ["%H:%M", function(d) { return d.getMinutes(); }],
  ["%H:%M", function(d) { return d.getHours(); }],
  ["%a %d", function(d) { return d.getDay() && d.getDate() != 1; }],
  ["%b %d", function(d) { return d.getDate() != 1; }],
  ["%B", function(d) { return d.getMonth(); }],
  ["%Y", function() { return true; }]
]);

// Zeitformat für Tooltipps
var formatTimeTooltipp = d3.time.format("%e %B %H:%M");

// ************************************
// define grid line functions
// ************************************
function make_x_axis1(x) {		
    return d3.svg.axis()
            .scale(x)
            .orient("bottom")
            .ticks(15)
}

function make_y_axis1(yy,dir) {		
    return d3.svg.axis()
            .scale(yy)
            .orient(dir)
            .ticks(5)
}


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

function showDiagram1Line(titel, sql, textX, textY, breite, hoehe, data, scaleY, units, id) {

    var margin = {top: 30, right: 55, bottom: 30, left: 60},
        width = breite - margin.left - margin.right,
        height = hoehe - margin.top - margin.bottom;
    
    document.write ("<div class='title'>" + titel + "</div>");
    
    // specify the scales for each set of data
    var x = d3.time.scale().range([0, width]);
    var y = d3.scale.linear().range([height, 0]);
    
    // dynamische Werte anzeigen
    var div = d3.select("body").append("div")   
        .attr("class", "tooltip tooltippfarbe")               
        .style("opacity", 0);

    
    // axis formatting
    var xAxis = d3.svg.axis().scale(x)
        	.orient("bottom").ticks(6).tickFormat(customTimeFormat);;
    var yAxis = d3.svg.axis().scale(y)
    		.tickFormat(d3.format(".1f"))
        	.orient("left").ticks(5);
    
    // line functions
    var valueLine = d3.svg.line()
        .x(function(d) { return x(d.zeit); })
        .y(function(d) { return y(d.value); });


    // setup the svg area
    var svg = d3.select(id)
        .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
        .append("g")
            .attr("transform", 
                "translate(" + margin.left + "," + margin.top + ")");

    // wrangle the data into the correct formats and units
    data.forEach(function(d) {
        d.zeit = parseDate(d.zeit);
        d.value = +d.value;
    });

    // Scale the range of the data
    x.domain(d3.extent(data, function(d) { return d.zeit; }));
    if ( scaleY == 0 ) {
        y.domain([
            d3.min(data, function(d) {return Math.min(d.value); })-.25, 
            d3.max(data, function(d) {return Math.max(d.value); })+.25]); 
        } 
        else {
            y.domain([ 0,100 ]);
        }

    svg.append("path")      // Add the value line.
        .attr("class", "linecolor")
        .attr("d", valueLine(data));

    svg.append("g")         // Add the X Axis
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    svg.append("g")         // Add the value axis 
        .attr("class", "y axis")
        //.style("fill", "steelblue")
        .call(yAxis);	

    svg.append("text")      // Add the text label for the value axis
        .attr("class", "y")
        .attr("transform", "rotate(-90)")
        .attr("x", 0)
        .attr("y", -40)
        //.style("fill", "steelblue")
        .style("text-anchor", "end")
        .text(textY);


    svg.append("g")			
            .attr("class", "grid")
            .attr("transform", "translate(0," + height + ")")
            .call(make_x_axis1(x)
                .tickSize(-height, 0, 0)
                .tickFormat("")
            );
    
    svg.append("g")         
        .attr("class", "grid")
        .call(make_y_axis1(y,"left")
            .tickSize(-width, 0, 0)
            .tickFormat("")
        )
        

    // dynamische Wertanzeige
    svg.selectAll("dot")    
            .data(data)         
        .enter().append("circle")                               
            .attr("r", 2)       
            .attr("cx", function(d) { return x(d.zeit); })       
            .attr("cy", function(d) { return y(d.value); })     
            .on("mouseover", function(d) {      
                div.transition()        
                    .duration(100)      
                    .style("opacity", .9);      
                div .html(formatTimeTooltipp(d.zeit) + "<br/>"  + d.value + units)  
                    .style("left", (d3.event.pageX) + "px")     
                    .style("top", (d3.event.pageY - 28) + "px");    
                })                  
            .on("mouseout", function(d) {       
                div.transition()        
                    .duration(500)      
                    .style("opacity", 0);   
            });

    return true;
}




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

function showDiagram2Lines(titel, data, textX, textY1, textY2, breite, hoehe, scaleY1, scaleY2, units1, units2, id) {

    var margin = {top: 30, right: 65, bottom: 30, left: 60},
        width = breite - margin.left - margin.right,
        height = hoehe - margin.top - margin.bottom;
    
    document.write ("<div class='title'>" + titel + "</div>");
    
    // specify the scales for each set of data
    var x = d3.time.scale().range([0, width]);
    var y = d3.scale.linear().range([height, 0]);
    var y2 = d3.scale.linear().range([height, 0]);

    // dynamische Werte anzeigen
    var div = d3.select("body").append("div")   
        .attr("class", "tooltip tooltippfarbe")               
        .style("opacity", 0);

    
    // axis formatting
    var xAxis = d3.svg.axis().scale(x)
        	.orient("bottom").ticks(6).tickFormat(customTimeFormat);;
    var yAxis = d3.svg.axis().scale(y)
    		.tickFormat(d3.format(".1f"))
        	.orient("left").ticks(5);
    var y2Axis = d3.svg.axis().scale(y2)
    		.tickFormat(d3.format(".1f"))
        	.orient("right").ticks(5);
    
    // line functions ^
    var valueLine1 = d3.svg.line()
        .x(function(d) { return x(d.zeit); })
        .y(function(d) { return y(d.value1); });
    // line functions 1
    var valueLine2 = d3.svg.line()
        .x(function(d) { return x(d.zeit); })
        .y(function(d) { return y2(d.value2); });


    // setup the svg area
    var svg = d3.select(id)
        .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
        .append("g")
            .attr("transform", 
                "translate(" + margin.left + "," + margin.top + ")");

    // wrangle the data into the correct formats and units
    data.forEach(function(d) {
        d.zeit = parseDate(d.zeit);
        d.value1 = +d.value1;
        d.value2 = +d.value2;
    });

    // Scale the range of the data
    x.domain(d3.extent(data, function(d) { return d.zeit; }));
    if ( scaleY1 == 0 ) {
        y.domain([
            d3.min(data, function(d) {return Math.min(d.value1); })-.25, 
            d3.max(data, function(d) {return Math.max(d.value1); })+.25]); 
    } 
    else {
        y.domain([ 0,100 ]);
    }
    
    if ( scaleY2 == 0 ) {
        y2.domain([
            d3.min(data, function(d) {return Math.min(d.value2); })-.25, 
            d3.max(data, function(d) {return Math.max(d.value2); })+.25]); 
    } 
    else {
        y2.domain([ 0,100 ]);
    }
    

    svg.append("path")      // Add the value line.1
        .attr("class", "linecolor1")
        .attr("d", valueLine1(data));

    svg.append("path")      // Add the value line 2
        .attr("class", "linecolor2")
        .attr("d", valueLine2(data));

    svg.append("g")         // Add the X Axis
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    svg.append("g")         // Add the value axis 
        .attr("class", "y1 axis")
        .call(yAxis);
    svg.append("g")         // Add the value axis 
        .attr("class", "y2 axis")
        .attr("transform", "translate(" + width + " ,0)")	
        .call(y2Axis);

    // Y-Achsen-Beschriftung
    svg.append("text")      // Add the text label for the value1 axis
        .attr("class", "y1")
        //.attr("transform", "rotate(-90)")
        .attr("x", 10)
        .attr("y", 0)
        //.style("fill", "steelblue")
        .style("text-anchor", "begin")
        .text(textY1);

    svg.append("text")      // Add the text label for value 2
        .attr("class", "y2")
        //.attr("transform", "rotate(-90)")
        .attr("x", width-10)
        .attr("y", 0)
        //.style("fill", "red")
        .style("text-anchor", "end")
        .text(textY2);


    svg.append("g")			
            .attr("class", "grid")
            .attr("transform", "translate(0," + height + ")")
            .call(make_x_axis1(x)
                .tickSize(-height, 0, 0)
                .tickFormat("")
            );
    
    svg.append("g")         
        .attr("class", "grid")
        .call(make_y_axis1(y,"left")
            .tickSize(-width, 0, 0)
            .tickFormat("")
        )
    // NEU
    svg.append("g")         
        .attr("class", "grid")
        .call(make_y_axis1(y,"right")
            .tickSize(-width, 0, 0)
            .tickFormat("")
        )    

    // dynamische Wertanzeige
    svg.selectAll("dot")    
            .data(data)         
        .enter().append("circle")                               
            .attr("r", 2)       
            .attr("cx", function(d) { return x(d.zeit); })       
            .attr("cy", function(d) { return y(d.value1); })     
            .on("mouseover", function(d) {      
                div.transition()        
                    .duration(100)      
                    .style("opacity", .9);      
                div .html(formatTimeTooltipp(d.zeit) + "<br/>"  + d.value1 + units1 + "<br/>" + d.value2 + units2)  
                    .style("left", (d3.event.pageX) + "px")     
                    .style("top", (d3.event.pageY - 28) + "px");    
                })                  
            .on("mouseout", function(d) {       
                div.transition()        
                    .duration(500)      
                    .style("opacity", 0);   
            });

    return true;
}

