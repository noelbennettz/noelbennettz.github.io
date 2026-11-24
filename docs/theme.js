/* theme.js — the one theme bootstrap and toggle for every page on this domain.

   Loaded synchronously in <head> before the stylesheet so the first paint
   already has data-theme; the same localStorage key is shared by the index and
   the three project sites, so switching on one page switches all of them. */
(function () {
  var root = document.documentElement;
  var KEY = "theme";
  var zh = root.lang.indexOf("zh") === 0;
  var labels = {
    light: zh ? "日間" : "Light",
    dark: zh ? "夜間" : "Dark"
  };
  var aria = {
    toLight: zh ? "切換日間模式" : "Switch to light mode",
    toDark: zh ? "切換夜間模式" : "Switch to dark mode"
  };

  function prefersDark() {
    try {
      return window.matchMedia("(prefers-color-scheme: dark)").matches;
    } catch (e) {
      return false;
    }
  }

  function stored() {
    try {
      return localStorage.getItem(KEY);
    } catch (e) {
      return null;
    }
  }

  function current() {
    return root.dataset.theme === "dark" ? "dark" : "light";
  }

  /* The button shows the mode it switches to, so its label is always the
     destination and aria-pressed describes the present state. */
  function render() {
    var dark = current() === "dark";
    var buttons = document.querySelectorAll(".theme-toggle");
    for (var i = 0; i < buttons.length; i++) {
      var btn = buttons[i];
      btn.textContent = dark ? labels.light : labels.dark;
      btn.setAttribute("aria-label", dark ? aria.toLight : aria.toDark);
      btn.setAttribute("aria-pressed", dark ? "true" : "false");
    }
  }

  function set(theme) {
    root.dataset.theme = theme;
    render();
  }

  /* Boot: a stored choice beats the system setting; the system setting is the
     fallback when storage is unavailable. */
  set(stored() || (prefersDark() ? "dark" : "light"));

  document.addEventListener("DOMContentLoaded", function () {
    var buttons = document.querySelectorAll(".theme-toggle");
    for (var i = 0; i < buttons.length; i++) {
      buttons[i].addEventListener("click", function () {
        var next = current() === "dark" ? "light" : "dark";
        try {
          localStorage.setItem(KEY, next);
        } catch (e) {}
        set(next);
      });
    }
    render();
  });

  window.addEventListener("storage", function (event) {
    if (event.key === KEY && (event.newValue === "dark" || event.newValue === "light")) {
      set(event.newValue);
    }
  });
})();
