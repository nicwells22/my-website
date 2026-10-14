"""Generate a static HTML page for each post in posts/posts.json.

Each generated page (posts/<slug>.html) has Open Graph and Twitter meta
tags baked into the <head>, so link previews on Facebook, LinkedIn, etc.
show the post's title and summary. Page content is rendered client-side
with the same marked/DOMPurify setup as blog.html.

Run this after adding or editing entries in posts/posts.json:

    python generate_posts.py

Then commit the generated posts/*.html files along with the markdown.
"""

import html
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
POSTS_DIR = ROOT / "posts"
MANIFEST = POSTS_DIR / "posts.json"
SITE_URL = "https://nicholas-wells.com"
SITE_NAME = "Nicholas Wells"

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{TITLE}} | Nicholas Wells</title>
  <meta name="description" content="{{SUMMARY_ATTR}}">
  <link rel="canonical" href="{{URL}}">

  <!-- Open Graph (LinkedIn, Facebook) -->
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="Nicholas Wells">
  <meta property="og:url" content="{{URL}}">
  <meta property="og:title" content="{{TITLE_ATTR}}">
  <meta property="og:description" content="{{SUMMARY_ATTR}}">
  <meta property="og:locale" content="en_US">
  <meta property="article:published_time" content="{{DATE_ISO}}">

  <!-- Twitter/X -->
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="{{TITLE_ATTR}}">
  <meta name="twitter:description" content="{{SUMMARY_ATTR}}">

  <link rel="stylesheet" href="../styles.css">
</head>
<body>
  <nav class="site-nav" aria-label="Primary">
    <a class="nav-brand" href="../index.html">NW</a>
    <div class="nav-links">
      <a href="../index.html">Home</a>
      <a href="../blog.html" aria-current="page">Thoughts</a>
    </div>
  </nav>

  <main class="site-shell blog-shell">
    <article class="blog-panel">
      <a class="back-link" href="../blog.html">&larr; All thoughts</a>
      <header class="post-meta">
        <h1>{{TITLE}}</h1>
        <p class="post-date">{{DATE_DISPLAY}}</p>
        <div class="ridge-line" aria-hidden="true"></div>
      </header>
      <div id="post-content" class="post-content markdown-body">
        <p>Loading&hellip;</p>
      </div>
    </article>
  </main>

  <script src="https://cdn.jsdelivr.net/npm/marked@12.0.2/marked.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/marked-footnote@1.4.0/dist/index.umd.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/dompurify@3.1.6/dist/purify.min.js"></script>
  <script>
    marked.use(markedFootnote({ description: "Notes", footnoteDivider: true }));
    fetch("{{FILE}}", { cache: "no-cache" })
      .then(function (response) {
        if (!response.ok) throw new Error(response.status);
        return response.text();
      })
      .then(function (markdown) {
        document.getElementById("post-content").innerHTML =
          DOMPurify.sanitize(marked.parse(markdown));
      })
      .catch(function () {
        document.getElementById("post-content").innerHTML =
          '<p>Unable to load this thought. <a href="../blog.html">Back to all thoughts</a>.</p>';
      });
  </script>
</body>
</html>
"""


def format_date(date_string):
    try:
        parsed = datetime.strptime(date_string, "%Y-%m-%d")
    except (TypeError, ValueError):
        return date_string or ""
    return f"{parsed.strftime('%B')} {parsed.day}, {parsed.year}"


def render(template, values):
    for key, value in values.items():
        template = template.replace("{{" + key + "}}", value)
    return template


def main():
    posts = json.loads(MANIFEST.read_text(encoding="utf-8"))

    for post in posts:
        slug = post["slug"]
        title = post.get("title") or slug
        summary = post.get("summary") or ""
        file_name = post.get("file") or f"{slug}.md"
        url = f"{SITE_URL}/posts/{slug}.html"

        page = render(TEMPLATE, {
            "TITLE": html.escape(title),
            "TITLE_ATTR": html.escape(title, quote=True),
            "SUMMARY_ATTR": html.escape(summary, quote=True),
            "URL": url,
            "DATE_ISO": post.get("date") or "",
            "DATE_DISPLAY": format_date(post.get("date")),
            "FILE": file_name,
        })

        out_path = POSTS_DIR / f"{slug}.html"
        out_path.write_text(page, encoding="utf-8")
        print(f"generated {out_path.relative_to(ROOT)}")

    print(f"done ({len(posts)} post{'s' if len(posts) != 1 else ''})")


if __name__ == "__main__":
    main()
