/* Simple markdown blog for a static site.
 * Posts are markdown files in /posts, indexed by /posts/posts.json.
 * - blog.html            -> shows the list of posts
 * - blog.html?post=slug  -> renders that single post
 */

const MANIFEST_URL = "posts/posts.json";

const listView = document.getElementById("post-list-view");
const postView = document.getElementById("post-view");
const statusView = document.getElementById("status-view");
const statusMessage = document.getElementById("status-message");

function showStatus(message) {
  statusView.hidden = false;
  listView.hidden = true;
  postView.hidden = true;
  statusMessage.innerHTML = message;
}

function formatDate(dateString) {
  if (!dateString) return "";
  const date = new Date(dateString);
  if (Number.isNaN(date.getTime())) return dateString;
  return date.toLocaleDateString(undefined, {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
}

function sortByDateDesc(posts) {
  return [...posts].sort((a, b) => new Date(b.date) - new Date(a.date));
}

async function loadManifest() {
  const response = await fetch(MANIFEST_URL, { cache: "no-cache" });
  if (!response.ok) {
    throw new Error(`Could not load ${MANIFEST_URL} (${response.status})`);
  }
  return response.json();
}

function renderList(posts) {
  const list = document.getElementById("post-list");
  list.innerHTML = "";

  if (!posts.length) {
    showStatus("No thoughts published yet. Check back soon.");
    return;
  }

  for (const post of sortByDateDesc(posts)) {
    const item = document.createElement("li");
    item.className = "post-list-item";

    const link = document.createElement("a");
    link.className = "post-link";
    link.href = `blog.html?post=${encodeURIComponent(post.slug)}`;

    const title = document.createElement("span");
    title.className = "post-link-title";
    title.textContent = post.title || post.slug;
    link.appendChild(title);

    if (post.date) {
      const date = document.createElement("span");
      date.className = "post-link-date";
      date.textContent = formatDate(post.date);
      link.appendChild(date);
    }

    if (post.summary) {
      const summary = document.createElement("span");
      summary.className = "post-link-summary";
      summary.textContent = post.summary;
      link.appendChild(summary);
    }

    item.appendChild(link);
    list.appendChild(item);
  }

  statusView.hidden = true;
  postView.hidden = true;
  listView.hidden = false;
}

async function renderPost(post) {
  const fileName = post.file || `${post.slug}.md`;
  const response = await fetch(`posts/${fileName}`, { cache: "no-cache" });
  if (!response.ok) {
    throw new Error(`Could not load post "${post.slug}" (${response.status})`);
  }
  const markdown = await response.text();

  document.title = `${post.title || post.slug} | Nicholas Wells`;
  document.getElementById("post-title").textContent = post.title || post.slug;
  document.getElementById("post-date").textContent = formatDate(post.date);

  const rawHtml = marked.parse(markdown);
  document.getElementById("post-content").innerHTML = DOMPurify.sanitize(rawHtml);

  statusView.hidden = true;
  listView.hidden = true;
  postView.hidden = false;
}

async function main() {
  const params = new URLSearchParams(window.location.search);
  const slug = params.get("post");

  let posts;
  try {
    posts = await loadManifest();
  } catch (error) {
    showStatus(
      `Unable to load thoughts. ${error.message}.<br>` +
        "If you opened this file directly, serve the site over http " +
        "(for example: <code>python -m http.server</code>)."
    );
    return;
  }

  if (!slug) {
    renderList(posts);
    return;
  }

  const post = posts.find((p) => p.slug === slug);
  if (!post) {
    showStatus("That thought could not be found. " +
      '<a href="blog.html">Back to all thoughts</a>.');
    return;
  }

  try {
    await renderPost(post);
  } catch (error) {
    showStatus(`Unable to load that thought. ${error.message}.`);
  }
}

main();
