## Edge Case Chosen

When creating a student via `POST /students`, the `mark` field is optional.

## Handling

If `mark` is missing, the backend defaults it to `0`.

## Why

The specification says `mark` is optional for create, but does not define a default.
Using `0` keeps behavior deterministic, keeps `/stats` calculation simple, and avoids storing null marks in the database.
# Document your edge case here
- To get marks for this section you will need to explain to your tutor:
1) The edge case you identified
2) How you have accounted for this in your implementation