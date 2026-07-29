(function () {
  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".blog-image-widget").forEach(function (widget) {
      var dropzone = widget.querySelector(".blog-image-dropzone");
      var fileInput = widget.querySelector(".blog-image-file-input");
      var preview = widget.querySelector(".blog-image-preview");
      var previewImg = widget.querySelector(".blog-image-preview-img");
      var previewRemove = widget.querySelector(".blog-image-preview-remove");
      var clearCheckbox = widget.querySelector(
        ".blog-image-clear-label input[type=checkbox]",
      );

      function handleFiles(files) {
        if (files.length === 0) return;
        var file = files[0];
        if (!file.type.startsWith("image/")) return;

        try {
          var dt = new DataTransfer();
          dt.items.add(file);
          fileInput.files = dt.files;
        } catch (_) {}

        var reader = new FileReader();
        reader.onload = function (e) {
          previewImg.src = e.target.result;
          preview.style.display = "";
          dropzone.style.display = "none";
          if (clearCheckbox) clearCheckbox.checked = false;
        };
        reader.readAsDataURL(file);
      }

      dropzone.addEventListener("click", function () {
        fileInput.click();
      });

      fileInput.addEventListener("change", function () {
        handleFiles(this.files);
      });

      dropzone.addEventListener("dragover", function (e) {
        e.preventDefault();
        e.stopPropagation();
        dropzone.classList.add("blog-image-dropzone--dragover");
      });

      dropzone.addEventListener("dragenter", function (e) {
        e.preventDefault();
        e.stopPropagation();
        dropzone.classList.add("blog-image-dropzone--dragover");
      });

      dropzone.addEventListener("dragleave", function (e) {
        e.preventDefault();
        e.stopPropagation();
        dropzone.classList.remove("blog-image-dropzone--dragover");
      });

      dropzone.addEventListener("drop", function (e) {
        e.preventDefault();
        e.stopPropagation();
        dropzone.classList.remove("blog-image-dropzone--dragover");
        handleFiles(e.dataTransfer.files);
      });

      if (previewRemove) {
        previewRemove.addEventListener("click", function () {
          preview.style.display = "none";
          previewImg.src = "";
          dropzone.style.display = "";
          fileInput.value = "";
          if (clearCheckbox) clearCheckbox.checked = false;
        });
      }
    });
  });
})();
