(function () {
  document.addEventListener("DOMContentLoaded", function () {
    var input = document.getElementById("id_keywords");
    var existingEl = document.getElementById("existing-keywords-data");
    if (!input || !existingEl) return;

    var existingKeywords = [];
    try {
      existingKeywords = JSON.parse(existingEl.textContent);
    } catch (_) {}
    existingKeywords = existingKeywords.filter(function (k) {
      return k.trim() !== "";
    });

    var container = document.createElement("div");
    container.className = "tag-input-container";

    var tagList = document.createElement("div");
    tagList.className = "tag-input-tags";

    var textInput = document.createElement("input");
    textInput.type = "text";
    textInput.className = "tag-input-field";
    textInput.placeholder = "تگ جدید را تایپ کنید و Enter بزنید...";

    var dropdown = document.createElement("div");
    dropdown.className = "tag-input-dropdown";
    dropdown.style.display = "none";

    container.appendChild(tagList);
    container.appendChild(textInput);
    container.appendChild(dropdown);

    input.parentNode.insertBefore(container, input);
    input.style.display = "none";

    function getTags() {
      var val = input.value.trim();
      if (!val) return [];
      return val
        .split(",")
        .map(function (t) {
          return t.trim();
        })
        .filter(function (t) {
          return t !== "";
        });
    }

    function setTags(tags) {
      input.value = tags.join(",");
    }

    function renderTags() {
      var tags = getTags();
      tagList.innerHTML = "";
      tags.forEach(function (tag) {
        var chip = document.createElement("span");
        chip.className = "tag-input-chip";
        chip.textContent = tag;
        var remove = document.createElement("button");
        remove.type = "button";
        remove.className = "tag-input-chip-remove";
        remove.innerHTML = "&times;";
        remove.setAttribute("aria-label", "حذف " + tag);
        remove.addEventListener("click", function () {
          var current = getTags();
          var idx = current.indexOf(tag);
          if (idx !== -1) {
            current.splice(idx, 1);
            setTags(current);
            renderTags();
            updateSuggestions();
          }
        });
        chip.appendChild(remove);
        tagList.appendChild(chip);
      });
    }

    function extractWordsFromText(text) {
      if (!text) return [];
      var words = text
        .replace(/[،,.;:!؟?\-_(){}[\]"'«»@#$%^&*\/\\<>~\s]+/g, " ")
        .split(/\s+/)
        .map(function (w) {
          return w.trim();
        })
        .filter(function (w) {
          return w.length >= 2;
        });
      return Array.from(new Set(words));
    }

    function getSuggestions() {
      var currentTags = getTags();
      var titleWords = extractWordsFromText(
        document.getElementById("id_title")
          ? document.getElementById("id_title").value
          : "",
      );
      var bodyWords = extractWordsFromText(
        document.querySelector("textarea.ckeditor-textarea")
          ? document.querySelector("textarea.ckeditor-textarea").value
          : "",
      );

      var all = existingKeywords.concat(titleWords).concat(bodyWords);
      return Array.from(new Set(all)).filter(function (s) {
        return currentTags.indexOf(s) === -1;
      });
    }

    function updateSuggestions() {
      var query = textInput.value.trim();
      var allSuggestions = getSuggestions();
      var filtered = query
        ? allSuggestions.filter(function (s) {
            return s.indexOf(query) !== -1 || s.indexOf(query) === 0;
          })
        : [];
      filtered.sort(function (a, b) {
        var aStarts = a.indexOf(query) === 0 ? 0 : 1;
        var bStarts = b.indexOf(query) === 0 ? 0 : 1;
        if (aStarts !== bStarts) return aStarts - bStarts;
        return a.length - b.length;
      });
      filtered = filtered.slice(0, 10);

      if (filtered.length > 0 && query.length > 0) {
        dropdown.innerHTML = "";
        filtered.forEach(function (s) {
          var item = document.createElement("div");
          item.className = "tag-input-dropdown-item";
          item.textContent = s;
          item.addEventListener("mousedown", function (e) {
            e.preventDefault();
            addTag(s);
          });
          dropdown.appendChild(item);
        });
        dropdown.style.display = "block";
      } else {
        dropdown.style.display = "none";
      }
    }

    function addTag(tag) {
      tag = tag.trim();
      if (!tag) return;
      var current = getTags();
      if (current.indexOf(tag) !== -1) return;
      current.push(tag);
      setTags(current);
      renderTags();
      textInput.value = "";
      dropdown.style.display = "none";
      textInput.focus();
      updateSuggestions();
    }

    textInput.addEventListener("input", updateSuggestions);

    textInput.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === ",") {
        e.preventDefault();
        var val = textInput.value.trim();
        if (val) {
          addTag(val);
        }
      } else if (e.key === "Backspace" && textInput.value === "") {
        var current = getTags();
        if (current.length > 0) {
          current.pop();
          setTags(current);
          renderTags();
          updateSuggestions();
        }
      } else if (e.key === "Escape") {
        dropdown.style.display = "none";
      }
    });

    document.addEventListener("click", function (e) {
      if (!container.contains(e.target)) {
        dropdown.style.display = "none";
      }
    });

    var titleInput = document.getElementById("id_title");
    var bodyTextarea = document.querySelector("textarea.ckeditor-textarea");
    if (titleInput) {
      titleInput.addEventListener("input", function () {
        if (textInput === document.activeElement) updateSuggestions();
      });
    }

    function pollBody() {
      if (bodyTextarea && textInput === document.activeElement) {
        updateSuggestions();
      }
    }

    if (bodyTextarea) {
      var bodyObserver = new MutationObserver(pollBody);
      bodyObserver.observe(bodyTextarea, {
        attributes: true,
        subtree: true,
        childList: true,
      });
    }

    textInput.addEventListener("focus", function () {
      if (textInput.value.trim()) {
        updateSuggestions();
      }
    });

    renderTags();
  });
})();
