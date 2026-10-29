# kanban

A Quarkdown atom for easily creating kanban boards.

![A kanban board with three columns](https://github.com/quarkdown-labs/atoms/blob/main/kanban/1.0.0/__images/preview.png?raw=true)

## Getting started

- `.kanban` holds the board
- `.kbcolumn` adds a column to the board.
- `.kbitem` adds a card to a column.

```
.kanban fontsize:{small}
    .kbcolumn {To do}
        .kbitem {Authentication} labels:{- High}
        .kbitem {Update documentation}
        .kbitem {Implement search} labels:{- Medium}

    .kbcolumn {In progress}
        .kbitem {Dashboard} labels:{- Low}
        .kbitem {Fix login bug} labels:{- High} color:{red}
        .kbitem {Write unit tests}

    .kbcolumn {Done} color:{green}
        .kbitem {Set up project}
        .kbitem {Create landing page} labels:{- Medium}
```

## Optional configuration

#### `.kanban`

- `fontsize`: font size of the whole board.
- `rowgap`: space between columns.
- `labels`: a dictionary mapping label names to colors. Defaults to `high: red`, `medium: yellow` and `low: green`.

#### `.kbcolumn`

- `width`: column width.
- `color`: color of the line under the column title.

#### `.kbitem`

- `color`: card border color.
- `labels`: a list of labels shown under the card text.

## Custom labels

```
.var {labels}
    - bug: red
    - feature: blue

.kanban labels:{.labels}
    .kbcolumn {To do}
        .kbitem {Fix login} labels:{- Bug}
        .kbitem {Add search} labels:{- Feature}
```
