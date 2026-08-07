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
    /* --- Table of Contents --- */
    var bodyEl = document.getElementById("blog-detail-body");
    var tocList = document.getElementById("blog-toc-list");
    var tocSection = document.getElementById("blog-toc");
    if (bodyEl && tocList) {
      var headings = bodyEl.querySelectorAll("h2, h3");
      if (headings.length > 1) {
        headings.forEach(function (h, i) {
          var id = "section-" + i;
          h.setAttribute("id", id);
          var li = document.createElement("li");
          if (h.tagName === "H3") li.style.paddingRight = "1rem";
          var a = document.createElement("a");
          a.href = "#" + id;
          a.textContent = h.textContent;
          li.appendChild(a);
          tocList.appendChild(li);
        });
        tocSection.style.display = "";
      }
    }

    /* --- Image lightbox --- */
    var mainImage = document.getElementById("blog-detail-main-image");
    var lightbox = document.getElementById("blog-lightbox");
    if (mainImage && lightbox) {
      mainImage.addEventListener("click", function () {
        lightbox.classList.add("open");
      });
    }

    /* --- Scroll progress bar (based on article body) --- */
    var progressBar = document.getElementById("blog-progress-bar");
    var bodyEl = document.getElementById("blog-detail-body");
    if (progressBar && bodyEl) {
      window.addEventListener("scroll", function () {
        var bodyTop = bodyEl.getBoundingClientRect().top + window.scrollY;
        var bodyHeight = bodyEl.offsetHeight;
        var scrollY = window.scrollY;

        /* 0% when body top aligns with viewport top, 100% when body bottom aligns with viewport top */
        var startPos = bodyTop;
        var endPos = bodyTop + bodyHeight - window.innerHeight;

        var progress = Math.min(
          1,
          Math.max(0, (scrollY - startPos) / (endPos - startPos)),
        );
        progressBar.style.width = progress * 100 + "%";
      });
    }

    /* --- Fade-in scroll animations --- */
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("fade-in--visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.1 },
    );
    document
      .querySelectorAll(
        ".blog-detail-author-box, .blog-related-posts, .comments-section",
      )
      .forEach(function (el) {
        el.classList.add("fade-in");
        observer.observe(el);
      });

    /* --- Star rating --- */
    var blogRating = document.getElementById("blog-star-rating");
    if (blogRating) {
      var postId = blogRating.getAttribute("data-post-id");
      var isAuth = blogRating.getAttribute("data-user-auth") === "true";
      var ratingAvg = document.getElementById("rating-average");
      var ratingCnt = document.getElementById("rating-count");
      var pendingScore = null;

      function submitRating(id, score) {
        return new Promise(function (resolve) {
          var token = getCSRF();
          var xhr = new XMLHttpRequest();
          xhr.open("POST", "/api/rate-blog-post/" + id + "/");
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
              var radios = blogRating.querySelectorAll('input[type="radio"]');
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
            ratingAvg.textContent =
              d.average != null ? toFa(d.average) : "\u2014";
            ratingCnt.textContent = "(" + toFa(d.count) + " امتیاز)";
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

      blogRating.addEventListener("click", function (e) {
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
                return submitRating(postId, pendingScore);
              },
            });
          }
          return;
        }
        submitRating(postId, score);
      });
    }
  });
})();
