# frontmatter

A package for compactly displaying a frontmatter for publications, with authors and affiliations.

## Getting started

In `.docauthors`, add the authors and their affiliation IDs.
This code is conventionally put at the top of your document, before imports and other content.

```markdown
.docauthors
    - Jane Doe
      - ids: quarkdown, usfca
    - John Smith
    - Alice Johnson
      - ids: quarkdown
```

Call `.frontmatter` where your frontmatter should appear, with the affiliation IDs associated with their full names.

```
.frontmatter
    - quarkdown: Quarkdown Labs
    - usfca: University of San Francisco
```

## Configuration

The `.frontmatter` function takes the following optional parameters:

#### `layout` (`inline`, `stack`, `auto`)

The layout of the affiliations. Defaults to `auto`.

- `inline`: affiliations are displayed in a single row, separated by commas.
- `stack`: affiliations are displayed in a vertical stack, one per line.
- `auto`: `inline` for 5 or fewer affiliations, `stack` otherwise.

#### `fontsize`

The font size for the authors row.

#### `fontweight`

The font weight for the authors row.