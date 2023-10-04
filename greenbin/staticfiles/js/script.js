function getCookie(c_name) {
  if (document.cookie.length > 0) {
    c_start = document.cookie.indexOf(c_name + "=");
    if (c_start != -1) {
      c_start = c_start + c_name.length + 1;
      c_end = document.cookie.indexOf(";", c_start);
      if (c_end == -1) c_end = document.cookie.length;
      return unescape(document.cookie.substring(c_start, c_end));
    }
  }
  return "";
}

$(function () {
  $.ajaxSetup({
    headers: { "X-CSRFToken": getCookie("csrftoken") },
  });
});

// CURRENT YEAR
const currentYear = new Date().getFullYear();
const year = document.querySelector(".year");
year.textContent = currentYear;

// MAKE MOBILE NAVIGATION WORK
const btnNavEl = document.querySelector(".btn-mobile-nav");
const headerEl = document.querySelector(".header");
const heroImgs = document.querySelector(".hero-container");

btnNavEl.addEventListener("click", function () {
  headerEl.classList.toggle("nav-open");
});
///////////////////////////////////////////////////////////
// Smooth scrolling animation
const allLinks = document.querySelectorAll("a:link");

allLinks.forEach(function (link) {
  link.addEventListener("click", function (e) {
    e.preventDefault();
    const href = link.getAttribute("href");

    // Scroll back to top
    if (href === "#")
      window.scrollTo({
        top: 0,
        behavior: "smooth",
      });

    // Scroll to other links
    if (href !== "#" && href.startsWith("#")) {
      const sectionEl = document.querySelector(href);
      sectionEl.scrollIntoView({ behavior: "smooth" });
    }

    // Close mobile naviagtion
    if (link.classList.contains("main-nav-link"))
      headerEl.classList.toggle("nav-open");
  });
});

///////////////////////////////////////////////////////////
//STICKY ANIMATION
// const sectionHeroEl = document.querySelector(".section-hero");

// const obs = new IntersectionObserver(
//   function (entries) {
//     const ent = entries[0];
//     if (!ent.isIntersecting) document.body.classList.add("sticky");
//     if (ent.isIntersecting) document.body.classList.remove("sticky");
//   },
//   {
//     // In the viewport
//     root: null,
//     threshold: 0,
//     rootMargin: "-300px ",
//   }
// );
// obs.observe(sectionHeroEl);

window.addEventListener("scroll", () => {
  const currentScroll = window.pageYOffset;
  if (currentScroll > 150) {
    document.body.classList.add("sticky");
  } else {
    document.body.classList.remove("sticky");
  }
});
///////////////////////////////////////////////////////////
// Fixing flexbox gap property missing in some Safari versions
function checkFlexGap() {
  var flex = document.createElement("div");
  flex.style.display = "flex";
  flex.style.flexDirection = "column";
  flex.style.rowGap = "1px";

  flex.appendChild(document.createElement("div"));
  flex.appendChild(document.createElement("div"));

  document.body.appendChild(flex);
  var isSupported = flex.scrollHeight === 1;
  flex.parentNode.removeChild(flex);
  console.log(isSupported);

  if (!isSupported) document.body.classList.add("no-flexbox-gap");
}
checkFlexGap();

///////////////////////////////////////////////////////////
//SLIDER ANIMATION

const container = document.querySelector(".hero-container");
document.querySelector(".slider").addEventListener("input", (e) => {
  container.style.setProperty("--position", `${e.target.value}%`);
});

///////////////////////////////////////////////////////////
//Dropdown
let dropdown = document.querySelector(".dropdown");
dropdown.addEventListener("click", function () {
  console.log("click");
  dropdown.classList.toggle("active");
});

// Toggle for delete
function toggle() {
  var blur = document.getElementById("blur");
  blur.classList.toggle("active");
}

//////////////////////////////////////////////////////////////
//Timer for Process

function timeDiff(size, date) {
  Date.prototype.addHours = function (h) {
    this.setHours(this.getHours() + h);
    return this;
  };

  if (size === "S") {
    addHours = 6;
  }
  if (size === "M") {
    addHours = 8;
  }
  if (size === "L") {
    addHours = 10;
  }
  let nowTime = new Date().getTime();
  let dateTimeHours = new Date(date).addHours(addHours).getTime();

  // DATE FORMAT
  // let hours = Math.floor((sub % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  // let minutes = Math.floor((sub % (1000 * 60 * 60)) / (1000 * 60));
  // let seconds = Math.floor((sub % (1000 * 60)) / 1000);
  let sub = dateTimeHours - nowTime;
  let remainingTime = (dateTimeHours - nowTime + 1000) / 1000;
  let seconds = ("0" + Math.floor(remainingTime % 60)).slice(-2);
  let minutes = ("0" + Math.floor((remainingTime / 60) % 60)).slice(-2);
  let hours = ("0" + Math.floor((remainingTime / 3600) % 24)).slice(-2);

  return [hours, minutes, seconds, remainingTime];
}

function sendEmail(id, startdate) {
  Email.send({
    Host: "smtp.elasticemail.com",
    Username: "wadgymarandoni@gmail.com",
    Password: "BE8EB64DDEB11A485CB6A220FB41ED50DFB0",
    To: "andowii@hotmail.com",
    From: "wadgymarandoni@gmail.com",
    Subject: `Process Complete TP${id}`,
    Body: `<!DOCTYPE html> <html xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office" lang="en"> <head> <title></title> <meta http-equiv="Content-Type" content="text/html; charset=utf-8"> <meta name="viewport" content="width=device-width, initial-scale=1.0"> <link href="https://fonts.googleapis.com/css?family=Cabin" rel="stylesheet" type="text/css"> <style> * { box-sizing: border-box; } body { margin: 0; padding: 0; } a[x-apple-data-detectors] { color: inherit !important; text-decoration: inherit !important; } #MessageViewBody a { color: inherit; text-decoration: none; } p { line-height: inherit } .desktop_hide, .desktop_hide table { mso-hide: all; display: none; max-height: 0px; overflow: hidden; } .image_block img+div { display: none; } @media (max-width:670px) { .desktop_hide table.icons-inner { display: inline-block !important; } .icons-inner { text-align: center; } .icons-inner td { margin: 0 auto; } .image_block img.fullWidth { max-width: 100% !important; } .mobile_hide { display: none; } .row-content { width: 100% !important; } .stack .column { width: 100%; display: block; } .mobile_hide { min-height: 0; max-height: 0; max-width: 0; overflow: hidden; font-size: 0px; } .desktop_hide, .desktop_hide table { display: table !important; max-height: none !important; } } </style> </head> <body style="background-color: #000; margin: 0; padding: 0; -webkit-text-size-adjust: none; text-size-adjust: none;"> <table class="nl-container" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #000;"> <tbody> <tr> <td> <table class="row row-1" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #f2f9f1;"> <tbody> <tr> <td> <table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; color: #000; width: 650px; margin: 0 auto;" width="650"> <tbody> <tr> <td class="column column-1" width="100%" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; padding-bottom: 5px; padding-top: 5px; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;"> <table class="image_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"> <tr> <td class="pad" style="padding-bottom:15px;padding-top:15px;width:100%;padding-right:0px;padding-left:0px;"> <div class="alignment" align="center" style="line-height:10px"></div> </td> </tr> </table> </td> </tr> </tbody> </table> </td> </tr> </tbody> </table> <table class="row row-2" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #fff; background-size: auto;"> <tbody> <tr> <td> <table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-size: auto; background-color: #fff;background-position: top center; background-repeat: no-repeat; color: #000; width: 650px; margin: 0 auto;" width="650"> <tbody> <tr> <td class="column column-1" width="100%" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; padding-top: 45px; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;"> <table class="heading_block block-3" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"> <tr> <td class="pad" style="padding-top:35px;text-align:center;width:100%;"> <h1 style="margin: 0; color: #333; direction: ltr; font-family: 'Cabin', Arial, 'Helvetica Neue', Helvetica, sans-serif; font-size: 28px; font-weight: 400; letter-spacing: normal; line-height: 120%; text-align: center; margin-top: 0; margin-bottom: 0;"><strong>Your trash is READY!</strong></h1> </td> </tr> </table> <table class="paragraph_block block-4" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"> <tr> <td class="pad" style="padding-left:45px;padding-right:45px;padding-top:10px;"> <div style="color:#333333;font-family:'Cabin',Arial,'Helvetica Neue',Helvetica,sans-serif;font-size:18px;line-height:150%;text-align:center;mso-line-height-alt:27px;"> <p style="margin: 0;">The trash process that started in: ${startdate} is al done, its recommended to wait for the bin to cooldown. If you are interested in ways to use your new processed trash you can check out the "Whats next" section on your app!</p> </div> </td> </tr> </table> <table class="divider_block block-5" width="100%" border="0" cellpadding="20" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"> <tr> <td class="pad"> <div class="alignment" align="center"> <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="80%" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"> <tr> <td class="divider_inner" style="font-size: 1px; line-height: 1px; border-top: 1px solid #333333;"><span> </span></td> </tr> </table> </div> </td> </tr> </table> <table class="button_block block-6" width="100%" border="0" cellpadding="10" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"> <tr> <td class="pad"> <div class="alignment" align="center"><a href="http://127.0.0.1:8000/trash/${id}/" target="_blank" style="text-decoration:none;display:inline-block;color:#ffffff;background-color:#536655;border-radius:0px;width:auto;border-top:1px solid transparent;font-weight:400;border-right:1px solid transparent;border-bottom:1px solid transparent;border-left:1px solid transparent;padding-top:10px;padding-bottom:10px;font-family:'Cabin', Arial, 'Helvetica Neue', Helvetica, sans-serif;font-size:14px;text-align:center;mso-border-alt:none;word-break:keep-all;"><span style="padding-left:40px;padding-right:40px;font-size:14px;display:inline-block;letter-spacing:normal;"><span style="word-break:break-word;"><span style="line-height: 28px;" data-mce-style>See Details</span></span></span></a></div> </td> </tr> </table> <table class="paragraph_block block-7" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"> <tr> <td class="pad" style="padding-bottom:15px;padding-left:10px;padding-right:10px;padding-top:10px;"> <div style="color:#393d47;font-family:'Cabin',Arial,'Helvetica Neue',Helvetica,sans-serif;font-size:10px;line-height:120%;text-align:center;mso-line-height-alt:12px;"> <p style="margin: 0; word-break: break-word;"><span style="color: #000000;">Thanks for helping the planet change, we hope you are satisfied with our service.</span></p> </div> </td> </tr> </table> <table class="paragraph_block block-8" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"> <tr> <td class="pad" style="padding-bottom:20px;padding-left:10px;padding-right:10px;padding-top:10px;"> <div style="color:#8412c0;font-family:Arial, Helvetica Neue, Helvetica, sans-serif;font-size:14px;line-height:120%;text-align:center;mso-line-height-alt:16.8px;"> <p style="margin: 0; word-break: break-word;"><span style="color: #000000;">Greenbin © </span></p> </div> </td> </tr> </table> </td> </tr> </tbody> </table> </td> </tr> </tbody> </table> <table class="row row-3" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #f2f9f1;"> <tbody> <tr> <td> <table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; color: #000; width: 650px; margin: 0 auto;" width="650"> <tbody> <tr> <td class="column column-1" width="100%" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; padding-bottom: 10px; padding-top: 5px; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;"> <table class="divider_block block-1" width="100%" border="0" cellpadding="5" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"> <tr> <td class="pad"> <div class="alignment" align="center"> <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"> <tr> <td class="divider_inner" style="font-size: 1px; line-height: 1px; border-top: 0px solid #BBBBBB;"><span> </span></td> </tr> </table> </div> </td> </tr> </table> <table class="paragraph_block block-2" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"> <tr> <td class="pad"> <div style="color:#333;font-family:Arial, Helvetica Neue, Helvetica, sans-serif;font-size:11px;line-height:120%;text-align:center;mso-line-height-alt:13.2px;"> <p style="margin: 0; word-break: break-word;"><span style="color: #000000;">Duis euismod neque at lacus rutrum, nec suscipit eros tincidunt nterdum et malesuada.</span></p> <p style="margin: 0; word-break: break-word;"><span style="color: #000000;">Fames ac ante ipsum vestibulum.</span></p> </div> </td> </tr> </table> <table class="paragraph_block block-3" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"> <tr> <td class="pad"> <div style="color:#8412c0;font-family:Arial, Helvetica Neue, Helvetica, sans-serif;font-size:12px;line-height:120%;text-align:center;mso-line-height-alt:14.399999999999999px;"> <p style="margin: 0; word-break: break-word;"> </p> </div> </td> </tr> </table> <table class="paragraph_block block-4" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"> <tr> <td class="pad"> <div style="color:#8412c0;font-family:Arial, Helvetica Neue, Helvetica, sans-serif;font-size:11px;line-height:120%;text-align:center;mso-line-height-alt:13.2px;"> <p style="margin: 0; word-break: break-word;"><span><span style="color: #000000;">Your Street 12, 34567 AB City  /  info@example.com / (+1) 123 456 789</span><a href="http://www.example.com" style="color: #8412c0;"></a></span></p> </div> </td> </tr> </table> <table class="paragraph_block block-5" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;"> <tr> <td class="pad"> <div style="color:#8412c0;font-family:Arial, Helvetica Neue, Helvetica, sans-serif;font-size:12px;line-height:120%;text-align:center;mso-line-height-alt:14.399999999999999px;"> <p style="margin: 0; word-break: break-word;"> </p> </div> </td> </tr> </table> </td> </tr> </tbody> </table> </td> </tr> </tbody> </table> <table class="row row-4" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #ffffff;"> <tbody> <tr> <td> <table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; color: #000; background-color: #fff; width: 650px; margin: 0 auto;" width="650"> <tbody> <tr> <td class="column column-1" width="100%" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; padding-bottom: 5px; padding-top: 5px; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;"> <table class="icons_block block-1" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"> <tr> <td class="pad" style="vertical-align: middle; color: #1e0e4b; font-family: 'Inter', sans-serif; font-size: 15px; padding-bottom: 5px; padding-top: 5px; text-align: center;"> <table width="100%" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;"> <tr> <td class="alignment" style="vertical-align: middle; text-align: center;"></td> </tr> </table> </td> </tr> </table> </td> </tr> </tbody> </table> </td> </tr> </tbody> </table> </td> </tr> </tbody> </table> </body> </html>`,
  }).then(function (message) {
    alert("Trash Process Completed, mail notification sended");
    $.ajax({
      type: "POST",
      url: "completed/",
      dataType: "text/json",
      data: {
        id: id,
      },
      success: function () {
        console.log("Success");
      },
      error: function (error) {
        console.log("error:", error);
      },
    });
    // datos mandados con la solicutud POST
    // let _data = {
    //   id: id,
    // };
    // console.log(id);
    // fetch("completed/", {
    //   method: "POST",
    //   body: JSON.stringify(_data),
    //   headers: { "Content-type": "application/json; charset=UTF-8" },
    // }).catch((err) => console.log(err));
  });
}

function timer(id, size, startdate, mail, on_process) {
  let txtSeconds = document.getElementById("seconds");
  let txtMinutes = document.getElementById("minutes");
  let txtHours = document.getElementById("hours");

  const timerUpdate = setInterval(() => {
    let times = timeDiff(size, startdate);
    let hours = times[0];
    let minutes = times[1];
    let seconds = times[2];
    let remainingTime = times[3];
    txtHours.innerHTML = hours;
    txtMinutes.innerHTML = minutes;
    txtSeconds.innerHTML = seconds;
    if (remainingTime <= 1) {
      if (on_process == "True") {
        sendEmail(id, startdate, mail);
      }
      clearInterval(timerUpdate);
      txtHours.innerHTML = "--";
      txtMinutes.innerHTML = "--";
      txtSeconds.innerHTML = "--";
    }
  }, 1000);
}

// var timeObj = JSON.parse(localStorage.getItem("timeObj"));
// if (timeObj) {
//   hours = timeObj["hr"];
//   minutes = timeObj["min"];
//   seconds = timeObj["sec"];
// } else {

// Define and execute seconds
// function timer(size, startdate) {
//   let times = timeDiff(size, startdate);
//   // let hours = times[0];
//   // let minutes = times[1];
//   // let seconds = times[2];
//   let hours = 0;
//   let minutes = 0;
//   let seconds = 5;

//   loadSeconds();

//   function loadSeconds() {
//     let txtSeconds;

//     if (seconds < 0) {
//       seconds = 59;
//     }
//     // Show seconds in view
//     if (seconds < 10) {
//       txtSeconds = `0${seconds}`;
//     } else {
//       txtSeconds = seconds;
//     }
//     document.getElementById("seconds").innerHTML = txtSeconds;
//     seconds--;

//     loadMinutes(seconds);
//   }

//   function loadMinutes(seconds) {
//     let txtMinutes;

//     if (seconds == -1 && minutes !== 0) {
//       setTimeout(() => {
//         minutes--;
//       }, 500);
//     } else if (seconds == -1 && minutes == 0) {
//       setTimeout(() => {
//         minutes = 59;
//       }, 500);
//     }

//     // Show minutes in view
//     if (minutes < 10) {
//       txtMinutes = `0${minutes}`;
//     } else {
//       txtMinutes = minutes;
//     }
//     document.getElementById("minutes").innerHTML = txtMinutes;
//     loadHours(seconds, minutes);
//   }

//   function loadHours(seconds, minutes) {
//     let txtHours;

//     if (seconds == -1 && minutes == 0 && hours !== 0) {
//       setTimeout(() => {
//         hours--;
//       }, 500);
//     } else if (seconds == -1 && minutes == 0 && hours == 0) {
//       setTimeout(() => {
//         hours = 2;
//       }, 500);
//     }

//     // Show minutes in view
//     if (hours < 10) {
//       txtHours = `0${hours}`;
//     } else {
//       txtHours = hours;
//     }
//     document.getElementById("hours").innerHTML = txtHours;
//   }

//   setInterval(loadSeconds, 1000);
// }

// SAVE TIMER WHEN PAGE IS UNLOAD
function SaveTime() {
  seconds = document.getElementById("seconds").innerHTML;
  minutes = document.getElementById("minutes").innerHTML;
  hours = document.getElementById("hours").innerHTML;

  var timeObj = {
    sec: seconds,
    min: minutes,
    hr: hours,
  };
  localStorage.setItem("timeObj", JSON.stringify(timeObj));
}

// Function to make slides work
let slideIndex = 1;
showSlides(slideIndex);

// Next/previous controls
function plusSlides(n) {
  showSlides((slideIndex += n));
}

// Thumbnail image controls
function currentSlide(n) {
  showSlides((slideIndex = n));
}

function showSlides(n) {
  let i;
  let slides = document.getElementsByClassName("mySlides");
  let dots = document.getElementsByClassName("dot");
  if (n > slides.length) {
    slideIndex = 1;
  }
  if (n < 1) {
    slideIndex = slides.length;
  }
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex - 1].style.display = "block";
  dots[slideIndex - 1].className += " active";
}
