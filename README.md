# Photo Club Hub

[🇳🇱  Nederlands](README_nl.md)

## What does it do?

Photo Club Hub shows the work of photo club members to audiences outside their club.
It serves as a permanent online exhibition, showing a selection of each photographer's best work.
Unlike most photo sites, it is built around **clubs** rather than individual photographers:
clubs are where photographers already meet, discuss each other's work and exhibit together.
You can look up photographers directly, but you always see them as members of their clubs.
The clubs supply the data, and stay in full control of it.

Photo Club Hub aims to draw more visitors than club websites, which few people visit nowadays.
It also aims to provide a better viewing experience than social media, with its never-ending distractions.

Photo Club Hub comes as an app for iPhone and iPad, and as a web version that works in any browser,
on an Android phone or on a Windows or Mac computer.

## Where are we today?

- The [app](https://apps.apple.com/nl/app/photo-club-hub/id1178324330?l=en) for iPhone and iPad is available in Apple's App Store,
  and gets improvements and fixes about once a month.
- A club can add the [web version](https://www.fcdegender.nl/hub/en/clubs/) to its own website with one link: on
  [Fotogroep De Gender's website](https://www.fcdegender.nl/), the "Ledenlijst" menu item leads to
  [the club's members in the web version](https://www.fcdegender.nl/hub/nl/clubs/fgDeGender/).
- A handful of clubs show their members and portfolios. Many more are visible on the map, ready for the next step.
- Several clubs have integrated their data themselves, using a written guide (although we plan to make this easier).

## Where is this going?

Readers typically judge by what is already visible today, but today's version is part of a larger goal. So here are both side by
side.

| | Today | Goal |
| --- | --- | --- |
| Clubs | A handful show members and photos; many more are on the map. | Most photo clubs in the Netherlands showcase the work of their members. Gradually more countries join in. |
| Supplying data | Clubs edit a structured file, following a written guide; some manage on their own, some need additional help. | A club can get a largely pre-filled form for their data. It is largely prefilled using website data. Club only needs to "check-and-correct". |
| Keeping it current | Only when someone notices something is incorrect, and gets the data fixed. | Photo Club Hub checks for outdated data using the club's website, and asks for confirmation. |
| Exhibitions | Photo Club Hub doesn't show exhibitions yet. Clubs announce them on their own website, but people mostly hear about them by e-mail: a club's secretary tells nearby clubs, who may pass it on to their members. | Each club's upcoming and past exhibitions in one place, visible in the app and on the web, so people can discover exhibitions near them without being on anyone's mailing list. Optionally, the app can remind you of upcoming exhibitions by nearby clubs or clubs you follow. |
| Software maintenance | One enthousiast volunteered to design and build the current software, mostly before AI coding assistants were available. | A few volunteers, each looking after the features they made or care about (supported by readily available AI assistance). |

## Strategy to get the ball rolling

- There is a chicken-and-egg problem. As long as there are few clubs onboard, there is limited content. Limited content mean limited usage.
Limited usage means litle motivation for a club to come onboard. We want to break this cycle by not waiting for the clubs
  to arrive: clubs are put on the in-app map in advance, and a club can then step up and, helped by smart software, take it from there.  
- **Taking part is done in small steps.** Each level adds value. Level 1: the club is visible on the map.
  Level 2: current club members and their interests are listed. Level 3: member portfolios are available for viewing.
- **Software can handle most of the data entry for clubs.** Software has become far better at reading what a club
  already publishes. Instead of editing a file and fixing its errors, a club will get its data mostly filled in,
  and only has to check-and-correct it. We are not there yet, but this is where supplying the data is heading.
- **Coding assistants lower the barrier for developers to help out.** Joining an existing software project used to mean first investing
  days to find your way around the code. A modern AI assistant now explains in seconds where a value comes from,
  what caused a bug, or why the software tool chain says there are errors. So a volunteer can
  contribute to the code by investing a few hours of time per improvement.

## Principles

Photo Club Hub rests on a few principles:

- **Non-commercial.** Both apps are fully free, and will remain so. It is volunteer powered.
- **Open source.** The software code is in public repositories on GitHub and falls under an MIT open source license.
- **Clubs own their data.** A club owns its data and can host it itself. Alternatively, the project can host
  it on the club's behalf.
- **Photos stay with the clubs.** They are shown from the club's own website, and are *not* centrally hosted.
- **No login.** End-users don't sign up or have passwords: anyone can view the results, no big central database that needs maintenance. 
  The data is protected against accidental/malicious change via Git version control mechanisms: essentially submit-and-approve.
- **Priorities.** Without any data to show, the software has no value. So getting clubs on board has the highest priority.
  New features or improvements that can contribute to that are thus also very relevant. Example: simpler data entry using AI techniques.
  Simplifications are encouraged (because they simplify maintenance). Fancy technology that adds complexity needs clear justification. 
- **Target end users who are not technical.** Many club members are "a bit older" and joined their club for photography rather than to wrestle with software.
  So an intuitive user experience is key: external simplicity, sometimes at the cost of internal complexity.
- **Not limited to any organization or any specific country.** Although the current clubs are all in the Netherlands, the target audience is international.
Participating clubs do not have to belong to any particular national or international organization.
Having said that, we do strive for alignment with organizations such as the Dutch Fotobond.
- **Other apps are welcome.** There is an internal "Data" library that can be used to create additional applications (experimental or otherwise).
Please align with us before using the Photo Club Hub name. If you use the project's data, please credit Photo Club Hub.
The actual photos themselves are copyrighted and owned by the photographers.

## What we ask of you

| You are | We would ask you to | What you get back |
| --- | --- | --- |
| A supporter | try it, spread the word within your club, tell us what's missing | a say in what gets built next |
| A developer | pick up a ticket, and keep the part you built in good shape | a real project with real users, in Swift. Serious use of agentic AI. |
| A club's webmaster | publish your club's member list, and fix it when someone finds an error | your club's work visible outside the club, website improvement options |
| A club's officers | agree to take part, and enlist a member to supply the data | a showcase for the club and its exhibitons, all free |

## Hard questions

These are the questions people ask, or think without asking. Answers are being written. Some of the
[FAQ's Policy section](https://github.com/vdhamer/Photo-Club-Hub/blob/main/Photo%20Club%20Hub/Documentation/FAQ_en.md#policy) covers related ground: costs, privacy, control over photos, and whether it will still work in a few years.

1. The idea is great, but I see only a small number of photographers in the app, and it isn't growing. Why?
2. Maintaining JSON files is far too high a barrier for clubs. Why can't AI simply fill the app from the
   clubs' own websites?
3. How will clubs keep this up to date, when they struggle to keep even their own websites current?
4. I believe it can take off, but how do you break the chicken-and-egg problem: few users, so little value, so few users?
5. You built something only you can maintain. We can't afford to hire a company to take your place. What
   happens when you stop?
6. What does this add over the website a club already has?
7. What drives you to do this?

## Who owns what

<!-- Draft diagram, to be redrawn. The technical version (package, databases, data flow) lives in the Data README. -->
![Who owns what: a central club list points to each club's member list, which points to each member's portfolio. The member lists and portfolios are the club's own, and the photos stay on the club's website. The app and the web version show all of it, without copying photos.](images/who-owns-what.svg)

## Following along, and taking part

- **[The dashboard](https://github.com/vdhamer/Photo-Club-Hub-Project/discussions/14)** in this repository's Discussions
  shows what is being worked on, what comes next, and how that is decided. You can comment on it.
- **To get notified**, click Watch at the top of this page, or subscribe to the dashboard only.
- **No git or code needed** to comment on a ticket or a discussion: sign up to a free GitHub account, a browser will do.
- **`Good first issue`** marks tickets a newcomer can pick up.
- **Everything here is public.** Please don't write the names of club members in tickets or comments.
- **Ticket numbers** are written as `iOS#123`, `HTML#123`, `Data#123` or `Project#123`, after the four repositories:
  - [Photo-Club-Hub](https://github.com/vdhamer/Photo-Club-Hub): the app for iPhone and iPad
  - [Photo-Club-Hub-HTML](https://github.com/vdhamer/Photo-Club-Hub-HTML): the Mac app that generates the web version
  - [Photo-Club-Hub-Data](https://github.com/vdhamer/Photo-Club-Hub-Data): the part both apps share, and the master copy of central data
  - Photo-Club-Hub-Project (this one): overal planning, and cross-repository resources. In principle code-free.
- **Developers** find the code, how it is built and how to contribute in the READMEs of the first three.

## Further information

- [FAQ](https://github.com/vdhamer/Photo-Club-Hub/blob/main/Photo%20Club%20Hub/Documentation/FAQ_en.md), for users and clubs
- [How a club supplies its member list](https://tinyurl.com/Level2creation) (Level 2 guide)
- [The iOS app's README](https://github.com/vdhamer/Photo-Club-Hub/blob/main/.github/README.md): Levels, the data model, installation
- [Where the data lives, and current plans](https://github.com/vdhamer/Photo-Club-Hub-Data/issues/56) (a one-screen overview)
- [Glossary](https://github.com/vdhamer/Photo-Club-Hub-Data/issues/48) of terms the data model does not hold (being written)
