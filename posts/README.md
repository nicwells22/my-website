# How to post a new thought

Your blog ("Thoughts") is powered by plain markdown files in this `posts/`
folder plus an index file, `posts.json`. Follow these steps to publish a new
post.

## 1. Write the post

Create a new markdown file in this `posts/` folder. Name it with a short,
lowercase, hyphenated slug, for example:

```
posts/my-new-idea.md
```

Write your post in normal markdown. You can use headings, **bold**, _italics_,
lists, links, images, blockquotes, and code blocks.

> Tip: The big page title comes from `posts.json` (below), so you don't have to
> repeat the title inside the markdown file if you don't want to.

## 2. Add an entry to `posts.json`

Open `posts.json` and add a new object to the list. Each post needs these
fields:

| Field     | What it is                                                        |
| --------- | ----------------------------------------------------------------- |
| `slug`    | The post's URL id. Use the same name as the file (without `.md`). |
| `title`   | The title shown on the post and in the list.                      |
| `date`    | Publish date in `YYYY-MM-DD` format. Used for sorting.            |
| `file`    | The markdown file name, e.g. `my-new-idea.md`.                    |
| `summary` | A one-line description shown in the list of posts.                |

Example — adding a post to the existing list:

```json
[
  {
    "slug": "welcome",
    "title": "Welcome to my thoughts",
    "date": "2026-06-29",
    "file": "welcome.md",
    "summary": "A first note on why this space exists and what to expect here."
  },
  {
    "slug": "my-new-idea",
    "title": "My New Idea",
    "date": "2026-08-04",
    "file": "my-new-idea.md",
    "summary": "A short sentence describing what this post is about."
  }
]
```

Notes:

- The list is JSON, so keep the commas between entries and wrap every value in
  double quotes.
- Order doesn't matter — posts are automatically sorted newest-first by `date`.

## 3. Generate the shareable post page

Each post also gets a static HTML page (`posts/<slug>.html`) with the post's
title and summary baked into `<meta>` tags. This is what makes link previews
(Facebook, LinkedIn, etc.) show the post title — the `blog.html?post=...` URL
can't do that because those platforms don't run JavaScript.

From the project root run:

```
.venv/Scripts/python.exe generate_posts.py
```

This creates one `posts/<slug>.html` file per entry in `posts.json`. Re-run it
whenever you add a post or change a title, summary, or date. Commit the
generated HTML files along with the markdown — the site has no build step, so
they must be in the repo.

## 4. Preview locally (optional)

Because the site loads posts with `fetch`, you need to view it over http, not by
double-clicking the file. From the project root run:

```
python -m http.server 8000
```

Then open <http://localhost:8000/blog.html> and confirm your post appears in the
list and opens correctly.

## 5. Publish

Commit and push your changes:

```
git add posts/ generate_posts.py
git commit -m "Add post: My New Idea"
git push
```

Your new thought is now live. When sharing a post on social media, use the
`posts/<slug>.html` URL — that's the link whose preview shows the post title.

## Quick checklist

- [ ] Created `posts/<slug>.md`
- [ ] Added a matching entry in `posts.json` (`slug`, `title`, `date`, `file`, `summary`)
- [ ] `posts.json` is still valid JSON (commas + double quotes)
- [ ] Ran `generate_posts.py` and the new `posts/<slug>.html` exists
- [ ] Previewed at `/blog.html`
- [ ] Committed and pushed
