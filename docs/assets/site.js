/* World Newswire Press - tiny site script.
   1. World clocks: each clock carries its city's time zone (data-tz). The
      browser's own clock does the maths, so no server and no API is needed.
      Gold dot = daytime (6am-6pm local), teal dot = night.
   2. Tip form (tips.html only): turns the form into an email in the
      tipster's own mail app. Nothing is sent to or stored on our site. */
(function () {
  function tick() {
    var now = new Date();
    document.querySelectorAll('[data-tz]').forEach(function (el) {
      try {
        var t = new Intl.DateTimeFormat('en-GB', { hour: '2-digit', minute: '2-digit', hour12: false, timeZone: el.getAttribute('data-tz') }).format(now);
        var h = parseInt(t.slice(0, 2), 10);
        var out = el.querySelector('.t');
        if (out) out.textContent = t;
        var dot = el.querySelector('.dot');
        if (dot) dot.classList.toggle('day', h >= 6 && h < 18);
      } catch (e) { /* unknown zone: leave the dash */ }
    });
  }
  tick();
  setInterval(tick, 20000);

  var form = document.getElementById('tip-form');
  if (form) {
    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var f = form.elements;
      var subject = 'Confidential tip: ' + (f.topic.value || 'news tip');
      var lines = [
        'Where in the world: ' + (f.where.value || '-'),
        'Topic: ' + (f.topic.value || '-'),
        '',
        f.details.value || '',
        '',
        'How to reach me safely: ' + (f.contact.value || '-'),
        '',
        '(Sent from the World Newswire Press tip page. Nothing was stored on the website.)'
      ];
      window.location.href = 'mailto:info@worldnewswirepress.com?subject=' +
        encodeURIComponent(subject) + '&body=' + encodeURIComponent(lines.join('\n'));
    });
  }
})();
