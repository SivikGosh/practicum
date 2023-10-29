SELECT
    "posts_post"."id",
    "posts_post"."text",
    "posts_post"."pub_date",
    "posts_post"."author_id",
    "posts_post"."group_id"
FROM "posts_post"
WHERE (
  "posts_post"."text" LIKE Утромъ% ESCAPE '\'
  AND NOT ("posts_post"."author_id" = 1)
  AND "posts_post"."pub_date" >= 1895-01-30 00:00:00
)
ORDER BY "posts_post"."pub_date" DESC