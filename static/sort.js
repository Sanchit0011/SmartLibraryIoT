$(document).ready(function () {
    $('#sort').DataTable();
});

var docStyle = document.documentElement.style;
var aElem = document.querySelector('a');
var boundingClientRect = aElem.getBoundingClientRect();

aElem.onmousemove = function (e) {

    var x = e.clientX - boundingClientRect.left;
    var y = e.clientY - boundingClientRect.top;

    var xc = boundingClientRect.width / 2;
    var yc = boundingClientRect.height / 2;

    var dx = x - xc;
    var dy = y - yc;

    docStyle.setProperty('--rx', dy / -1 + 'deg');
    docStyle.setProperty('--ry', dx / 10 + 'deg');

};

aElem.onmouseleave = function (e) {

    docStyle.setProperty('--ty', '0');
    docStyle.setProperty('--rx', '0');
    docStyle.setProperty('--ry', '0');

};

aElem.onmousedown = function (e) {

    docStyle.setProperty('--tz', '-25px');

};

document.body.onmouseup = function (e) {

    docStyle.setProperty('--tz', '-12px');

};


var openModal = function (name) {
    if (name != "") {
        document.getElementById(name).id = "{{"+name+"}}";
    }
}

window.onload = function () {
    if (document.getElementById("myModaladd")) {
        document.getElementById("openadd").click()
    } else if (document.getElementById("myModaldel")) {
        document.getElementById("opendel").click()
    } else if (document.getElementById("myModallog")) {
        document.getElementById("openlog").click()
    } else if (document.getElementById("myModalcantdel")) {
        document.getElementById("openmyModalcantdel").click()
    }
};