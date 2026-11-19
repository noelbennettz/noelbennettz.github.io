// Latest-release lookup. The page works without JavaScript: every link
// already points at /releases/latest, and this only upgrades them to the
// exact asset of the newest release.
(() => {
  const REPO = "noelbennettz/Hy2droid";
  const API = `https://api.github.com/repos/${REPO}/releases/latest`;

  const assetMatchers = {
    arm64: (name) => name.includes("arm64-v8a"),
    armeabi: (name) => name.includes("armeabi-v7a"),
    x86_64: (name) => name.includes("x86_64"),
    x86: (name) => /-x86-release\.apk$/.test(name),
    universal: (name) => name.includes("universal"),
  };

  function setText(id, text) {
    const node = document.getElementById(id);
    if (node) node.textContent = text;
  }

  function formatDate(iso, locale) {
    const date = new Date(iso);
    if (Number.isNaN(date.getTime())) return "";
    return date.toLocaleDateString(locale, {
      year: "numeric",
      month: "short",
      day: "numeric",
    });
  }

  function apply(release) {
    const tag = release.tag_name || "";
    const locale = document.documentElement.lang || "en";
    const date = release.published_at ? formatDate(release.published_at, locale) : "";

    setText("release-version", tag);
    setText("release-version-2", tag);
    setText("release-version-3", tag);
    if (date) setText("release-date", date);

    document.querySelectorAll("[data-release-link]").forEach((link) => {
      link.href = release.html_url;
    });

    const assets = Array.isArray(release.assets) ? release.assets : [];
    document.querySelectorAll("[data-asset]").forEach((link) => {
      const match = assetMatchers[link.dataset.asset];
      const asset = match && assets.find((a) => match(a.name));
      if (asset && asset.browser_download_url) {
        link.href = asset.browser_download_url;
        if (asset.size) {
          link.title = `${(asset.size / 1024 / 1024).toFixed(1)} MB`;
        }
      }
    });
  }

  fetch(API, { headers: { Accept: "application/vnd.github+json" } })
    .then((response) => (response.ok ? response.json() : null))
    .then((release) => {
      if (release && !release.draft && !release.prerelease) apply(release);
    })
    .catch(() => {
      // Offline, rate limited, or GitHub is down: keep the static links.
    });
})();
