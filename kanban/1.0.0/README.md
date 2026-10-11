# kanban

A Quarkdown atom for easily creating kanban boards.

### Example

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