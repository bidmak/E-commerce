document.addEventListener("DOMContentLoaded", function () {
  const category = document.querySelector("#find-category");
  const search = document.querySelector("#search");
  const arrow = document.querySelector("#arrow");

  category.addEventListener("mouseenter", function () {
    document.querySelector("#arrow").classList.add("fa-chevron-up");
    search.classList.remove("hidden");
  });

  category.addEventListener("mouseleave", function () {
    document.querySelector("#arrow").classList.add("fa-chevron-down");
    search.classList.add("hidden");
  });

  search.addEventListener("mouseenter", function () {
    search.classList.remove("hidden");
    document.querySelector("#arrow").classList.add("fa-chevron-up");
  });
  search.addEventListener("mouseleave", function () {
    search.classList.add("hidden");
    document.querySelector("#arrow").classList.add("fa-chevron-down");
  });

  document.querySelector("#message-close").addEventListener("click", () => {
    document.querySelector("#message").style.display = "none";
  });
});
