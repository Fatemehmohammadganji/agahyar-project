(function () {
  "use strict";

  function toFa(n) {
    return String(n).replace(/\d/g, function (d) {
      return "۰۱۲۳۴۵۶۷۸۹"[d];
    });
  }

  function getCSRF() {
    var el = document.querySelector('[name="csrfmiddlewaretoken"]');
    return el ? el.value : "";
  }

  document.addEventListener("DOMContentLoaded", function () {
    var rating = document.getElementById("center-star-rating");
    if (!rating) return;
    var centerId = rating.getAttribute("data-center-id");
    var isAuth = rating.getAttribute("data-user-auth") === "true";
    var avgEl = document.getElementById("center-rating-average");
    var countEl = document.getElementById("center-rating-count");
    var pendingScore = null;

    function submitRating(id, score) {
      return new Promise(function (resolve) {
        var token = getCSRF();
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/api/rate-center/" + id + "/");
        xhr.setRequestHeader(
          "Content-Type",
          "application/x-www-form-urlencoded",
        );
        xhr.onload = function () {
          if (xhr.status === 401) {
            window.location.reload();
            return;
          }
          if (xhr.status !== 200) {
            alert("ثبت امتیاز با خطا مواجه شد: کد " + xhr.status);
            var radios = rating.querySelectorAll('input[type="radio"]');
            for (var i = 0; i < radios.length; i++) radios[i].checked = false;
            return resolve();
          }
          try {
            var d = JSON.parse(xhr.responseText);
          } catch (e) {
            return resolve();
          }
          if (d.error) {
            alert(d.error);
            return resolve();
          }
          if (avgEl) {
            avgEl.textContent = d.average != null ? toFa(d.average) : "\u2014";
          }
          if (countEl) {
            countEl.textContent = "(" + toFa(d.count) + " نظر)";
          }
          resolve();
        };
        xhr.onerror = function () {
          alert("ثبت امتیاز با خطا مواجه شد: خطای شبکه");
          resolve();
        };
        xhr.send(
          "score=" +
            score +
            "&csrfmiddlewaretoken=" +
            encodeURIComponent(token),
        );
      });
    }

    rating.addEventListener("click", function (e) {
      var label = e.target.closest("label");
      if (!label) return;
      var input = document.getElementById(label.getAttribute("for"));
      if (!input || !input.matches('input[type="radio"]')) return;
      var score = parseInt(input.value);
      if (!isAuth) {
        e.preventDefault();
        pendingScore = score;
        input.checked = false;
        if (window.AgahyarLoginModal) {
          window.AgahyarLoginModal.open({
            prompt: "برای ثبت امتیاز وارد شوید",
            onLogin: function () {
              return submitRating(centerId, pendingScore);
            },
          });
        }
        return;
      }
      submitRating(centerId, score);
    });
  });
})();
