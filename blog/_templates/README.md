# Blog posts and GitHub comments

The blog uses giscus (https://giscus.app/ko), backed by GitHub Discussions.

## One-time activation

Install https://github.com/apps/giscus on **only** `seominseok0429.github.io`.
Discussions is already enabled. The loader uses the verified repository ID and
Announcements category ID. The app installation must be completed before
publishing a post with comments. No secret or access token belongs in the site.

## Publish a post

1. Copy `post.html` into a new stable path, for example `blog/posts/my-post/index.html`.
2. Replace the title and publication date, then add the post content.
3. Keep the comments section and `/blog/comments.js` include at the end.
4. Add a link to the post on the corresponding category page and update its empty state.
5. Check the published post: comments should load and offer GitHub sign-in.

Only individual posts include the widget. The homepage and empty category pages
have no comment threads. This `_templates` folder is excluded by Jekyll, so the
starter file is not a public fake post.

Each pathname maps to its own discussion. Keep published URLs stable to retain
that mapping. The first real comment or reaction creates the discussion; do not
post a test comment on behalf of the owner. Manage comments in the repository's
Discussions tab.
