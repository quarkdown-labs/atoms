# simple-cv

A compact, single-column CV template.

## Getting started

```markdown
# John Doe

.contactinfo
    - +1 (xxx) xxx-xxxx
    - San Francisco, CA
    - [Website](https://example.com)

## Education

.edu {University of Example} degree:{Bachelor of Science in Computer Science} \
     dates:{2015 - 2019} location:{Example City, EX}
    - Graduated with honors
    - Relevant coursework: Data Structures, Algorithms, Software Engineering

## Work Experience

.work {Software Engineer} dates:{2021 - Present} company:{Example Inc.} \
     location:{Example City, EX}
    - Developed and maintained web applications using React and Node.js
    - Collaborated with cross-functional teams to deliver high-quality software solutions

## Projects

.project {Open Source Project} role:{Contributor} \
         dates:{2020 - Present}
    - Contributed to the development of an open-source library for data visualization

## Skills

- **Programming Languages:** Python, JavaScript, C++
- **Technologies:** React, Node.js, Docker, Git
```

## Functions

#### `.contactinfo`

A list of contact details, shown in a single row.

#### `.edu {institution}`

Requires `degree`, `dates` and `location`.

#### `.work {title}`

Requires `company`, `dates` and `location`.

#### `.project {name}`

Requires `dates`. `role` is optional.
