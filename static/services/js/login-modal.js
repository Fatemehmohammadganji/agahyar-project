(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", function () {
    var modal = document.getElementById("login-modal");
    var form = document.getElementById("login-modal-form");
    var errorBox = document.getElementById("login-modal-error");
    var promptEl = document.getElementById("login-modal-prompt");
    var closeBtn = document.getElementById("login-modal-close");
    if (!modal || !form || !errorBox || !closeBtn) return;

    var onLogin = null;

    function openModal() {
      errorBox.style.display = "none";
      modal.showModal();
      var usernameEl = document.getElementById("id_username");
      if (usernameEl) {
        usernameEl.focus();
      } else {
        modal.focus();
      }
    }

    modal.addEventListener("close", function () {
      onLogin = null;
      errorBox.style.display = "none";
    });

    closeBtn.addEventListener("click", function () {
      modal.close();
    });

    modal.addEventListener("click", function (e) {
      if (e.target === modal) modal.close();
    });

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var fd = new FormData(form);
      var params = "";
      fd.forEach(function (value, key) {
        if (params) params += "&";
        params += encodeURIComponent(key) + "=" + encodeURIComponent(value);
      });
      errorBox.style.display = "none";
      var submitBtn = form.querySelector('button[type="submit"]');
      if (submitBtn) submitBtn.disabled = true;
      fetch("/login/", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          "X-Requested-With": "XMLHttpRequest",
        },
        body: params,
      })
        .then(async function (r) {
          var ct = r.headers.get("Content-Type") || "";
          if (ct.indexOf("application/json") === 0) {
            const d = await r.json();
            return { ok: r.ok, data: d };
          }
          await r.text();
          throw new Error("خطا در ارتباط با سرور");
        })
        .then(function (result) {
          if (submitBtn) submitBtn.disabled = false;
          if (result.ok && result.data.success) {
            if (result.data.csrfToken) {
              var tokens = document.querySelectorAll(
                '[name="csrfmiddlewaretoken"]',
              );
              tokens.forEach(function (el) {
                el.value = result.data.csrfToken;
              });
            }
            var cb = onLogin;
            modal.close();
            var reload = function () {
              window.location.reload();
            };
            if (cb) {
              var r = cb();
              if (r && typeof r.then === "function") {
                r.then(reload, reload);
              } else {
                reload();
              }
            } else {
              reload();
            }
          } else {
            errorBox.textContent =
              result.data && result.data.error
                ? result.data.error
                : "نام کاربری یا رمز عبور اشتباه است.";
            errorBox.style.display = "block";
          }
        })
        .catch(function (err) {
          if (submitBtn) submitBtn.disabled = false;
          errorBox.textContent =
            err.message || "خطا در ارتباط با سرور. لطفاً دوباره تلاش کنید.";
          errorBox.style.display = "block";
        });
    });

    /* --- Generic login-prompt links open the modal --- */
    document.querySelectorAll(".login-prompt-link").forEach(function (el) {
      el.addEventListener("click", function (e) {
        e.preventDefault();
        window.AgahyarLoginModal.open({
          prompt: el.getAttribute("data-prompt") || "برای ادامه وارد شوید",
        });
      });
    });

    window.AgahyarLoginModal = {
      open: function (opts) {
        opts = opts || {};
        if (promptEl && opts.prompt) promptEl.textContent = opts.prompt;
        onLogin = opts.onLogin || null;
        openModal();
      },
      close: function () {
        modal.close();
      },
    };
  });
})();
