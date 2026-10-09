document.addEventListener("DOMContentLoaded", function () {
  loadLinks();
});

/* ---------- Load links from links.json ---------- */
function loadLinks() {
  fetch("links.json")
    .then(function (response) { return response.json(); })
    .then(function (data) {
      var container = document.getElementById("link-container");
      if (!container) {
        console.error("link-container not found in HTML");
        return;
      }
      data.forEach(function (link) {
        var card = document.createElement("div");
        card.className = "link-card";

        var a = document.createElement("a");
        a.href = link.url;
        a.target = "_blank";
        a.rel = "noopener noreferrer";
        a.textContent = link.title || link.url;

        var p = document.createElement("p");
        p.textContent = link.description || "";

        card.appendChild(a);
        card.appendChild(p);
        container.appendChild(card);
      });
    })
    .catch(function (err) {
      console.error("Error loading links.json:", err);
    });
}

/* ---------- Cookie consent modal handling ---------- */
function handleCookieConsent() {
  var overlay = document.getElementById("cookie-overlay");
  var acceptBtn = document.getElementById("accept-cookies");
  var manageBtn = document.getElementById("manage-cookies");
  var saveBtn = document.getElementById("save-settings");
  var settingsPanel = document.getElementById("cookie-settings");
  var analyticsCheckbox = document.getElementById("analytics-checkbox");

  if (!overlay) {
    console.error("Cookie overlay not found in HTML");
    return;
  }

  var raw = localStorage.getItem("cookieConsent");
  var consent = null;
  try {
    consent = raw ? JSON.parse(raw) : null;
  } catch (e) {
    localStorage.removeItem("cookieConsent");
    consent = null;
  }

  if (!consent) {
    overlay.classList.remove("hidden");
  } else if (consent.analytics) {
    loadGoogleAnalytics();
  }

  if (acceptBtn) {
    acceptBtn.addEventListener("click", function () {
      var data = { analytics: true };
      localStorage.setItem("cookieConsent", JSON.stringify(data));
      overlay.classList.add("hidden");
      loadGoogleAnalytics();
    });
  }

  if (manageBtn) {
    manageBtn.addEventListener("click", function () {
      if (settingsPanel) {
        settingsPanel.classList.remove("hidden");
      }
    });
  }

  if (saveBtn) {
    saveBtn.addEventListener("click", function () {
      var data = { analytics: !!(analyticsCheckbox && analyticsCheckbox.checked) };
      localStorage.setItem("cookieConsent", JSON.stringify(data));
      overlay.classList.add("hidden");
      if (data.analytics) {
        loadGoogleAnalytics();
      }
    });
  }
}

/* ---------- Load Google Analytics only after consent ---------- */
function loadGoogleAnalytics() {
  if (window.gaLoaded) return;
  window.gaLoaded = true;

  var measurementId = 'G-5H07SV662K'; // Replace with your GA4 ID

  var script1 = document.createElement('script');
  script1.async = true;
  script1.setAttribute('src', 'https://www.googletagmanager.com/gtag/js?id=' + measurementId);
  document.head.appendChild(script1);

  var script2 = document.createElement('script');
  var code = [
    "window.dataLayer = window.dataLayer || [];",
    "function gtag(){dataLayer.push(arguments);}",
    "gtag('js', new Date());",
    "gtag('config', '" + measurementId + "');"
  ].join("\n");
  script2.textContent = code;
  document.head.appendChild(script2);
}
