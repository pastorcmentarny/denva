function displayGreetings() {
    "use strict";
  let date = new Date();
  let hour = date.getHours();
  if (hour > 19) {
        display("Good Evening to You");
    } else if (hour > 16) {
        display("Good afernoon to You");
    } else if (hour === 12) {
        display("Good noon to You");
    } else if (hour > 10) {
        display("Good day to You");
    } else if (hour > 6) {
        display("Good  Morning to You");
    } else {
        display("Good Very Early Morning to You");
    }
}

function display(greetings) {
    const who = ",Dominik!";
    document.write(greetings + who);
}
