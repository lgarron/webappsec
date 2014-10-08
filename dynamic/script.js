{% autoescape true %}
// TODO: Using Python, change this

"use strict";

var protocol = "{{ protocol }}";

// This should always be satisfied, but let's not open ourselves up to injection.
if (["http", "https"].indexOf(protocol) == -1) {
  throw "Invalid protocol"
}

document.getElementById("messages").innerHTML += "<br><span class='" + protocol + "'>Script has loaded and run. [Protocol: " + protocol + "]</span>";

if (protocol == "http") {
  // document.getElementById("messages").style.borderColor = "#F00";
  // document.getElementById("messages").classList.add("http");
}
{% endautoescape %}
