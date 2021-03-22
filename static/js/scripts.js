// Empty JS for your own code to be here

(function () {


    var myVar = setInterval(myTimer, 2000);
    var lastEpoch=""
    var myChart;
    

    function myTimer() {
        var d = new Date();
        var xhttp = new XMLHttpRequest();
        var sensorshttp = new XMLHttpRequest();
        var metricshttp = new XMLHttpRequest();
        

        xhttp.open("GET", '/getresult', true);
        xhttp.send();
            
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
             document.getElementById("XXXXX").innerHTML = this.responseText;
            } };
    
        

        sensorshttp.open("GET", '/getsensors', true);
        sensorshttp.send();
            
        sensorshttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
             document.getElementById("sensors").innerHTML = this.responseText;
            } };
    
        metricshttp.open("GET", '/getmetrics', true);
        metricshttp.send();
                
        metricshttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                document.getElementById("metrics").innerHTML = this.responseText;
            } };

    };
       
}());


function startTask(filename) {  
    var xhttp = new XMLHttpRequest();

    xhttp.open("GET", '/startTask/'+filename, true);
    xhttp.send();
};