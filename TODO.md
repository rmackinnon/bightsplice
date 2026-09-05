# TODO

Future enhancements that are intentionally outside the initial `bightsplice`
release scope.

- [ ] Add an optional external-dependency inspection flag. It may inspect
  project dependency metadata such as `requirements.txt`, `pyproject.toml`,
  or other supported formats, but must remain informational and must not block
  validation or publish.
- [ ] Add richer interactive validation repair helpers, such as tab completion
  for module names, symbols, and import targets.
- [ ] Consider a pluggable linter interface. Version 1 uses Flake8 directly.
- [ ] Consider consulting the XDG `text/plain` MIME association when selecting
  an editor if neither explicit `bightsplice` configuration nor `$EDITOR` is
  available.
- [ ] Add additional completed-run compression backends such as zstd, 7zip,
  and lzma. Version 1 implements gzip only.
- [ ] Consider optional Git-native ignore matching in a future release. Do not
  implement a custom `.gitignore` parser.
- [ ] Add additional `LanguageHandler` implementations if future releases need
  language-aware reconciliation beyond Python.
