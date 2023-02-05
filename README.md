![logo](http://reasonabledeviations.com/assets/images/secondbrain1/logo_big.png)

This repository contains my Obsidian implementation of **Molecular Notes** – a Second Brain system that I use to organise my thinking. You can read about the philosophy of Molecular Notes [here](https://reasonabledeviations.com/2022/04/18/molecular-notes-part-1/) and more about the Obsidian implementation [here](https://reasonabledeviations.com/2022/06/12/molecular-notes-part-2/)).

**Note:** I am not accepting PRs as this repo represents my personal workflow. *However*, if you have a use case that the current iteration of MolecularNotes doesn't address, it would be awesome if you could [create an issue](https://github.com/robertmartin8/MolecularNotes/issues) and share the modification you made so that others can get some inspiration!


## Basic setup instructions

1. Install [Obsidian](https://obsidian.md/) and create an Obsidian Vault (a folder to store all your notes). Mine is named `ObsidianVault` and I put it in my home folder.
2. Clone this repository into your vault (on GitHub click the green `Code` button, then `Download ZIP`, and copy-paste the contents into your vault using Finder or File explorer)
3. Delete the README.md file.
4. In Obsidian, go to Settings -> Files & Links -> Default location for new attachments -> _attachments  (make this folder if it doesn't exist).
5. Set up templates:
	1. Settings -> Core plugins -> Templates (switch on). 
	2. Settings -> Templates -> Template folder location -> _templates.
	3. (Optional) set hotkey in Settings -> Hotkeys -> Templates: Insert Template -> ⌘T
6. Check you have the below plugins enabled: Settings -> Core Plugins
7. (Optional) Change the colour theme to something you like! You can find this in Settings -> Appearance -> Themes


### Plugins

These are the core plugins I am using (most are enabled by default):

- File explorer: duh
- Search: duh 
- Quick switcher: a very useful way of quickly jumping to a new note: you just press ⌘O then start typing the note name to jump to it.
- Graph view: duh
- Backlinks / Outgoing links: duh
- Tag pane: a helpful way of looking at your tags
- Page preview: nice syntax
- Templates: a must
- Note composer: I have this but I've only used it rarely
- Command palette: a must
- Starred: a new-ish plugin that helps you save common searches
- Markdown format importer: useful in my workflows to paste Notion content into Obsidian
- Word count: up to you
- Workspaces: handy! I've saved a note view and a graph view.
- Sync: optional but I like it


Community plugins:

- Mind Map: occasionally useful to visualise notes as a mindmap
- Obsidian git: I like having an extra backup to a private github
- Tag wrangler: very useful extension for renaming tags


## Advanced setup

Make sure you have python 3 installed on your system. The helper script can be run from your Obsidian Vault:

```
cd ObsidianVault && python _scripts/obsidian_util.py
```

In my `~/.zshrc` I then created an alias for this, such that when I type `obsidian` into terminal my script runs. 

```
alias obsidian="cd $HOME/ObsidianVault && python _scripts/obsidian_util.py"
```

### Polymer dashboard

The Polymer dashboard (a spaced repetition tool) requires `streamlit` to be installed (`pip install streamlit`). It can be run using:

```
cd ObsidianVault && streamlit run _scripts/polymer.py
```

If you are having trouble with Polymer, please follow the below steps:

1. Shut down the dashboard (e.g ctrl-C wherever you ran `streamlit run _scripts/polymer.py`)
2. Delete the `_scripts/db.json` file. **Note:** this will delete your current flashcard progress
3. Re-run the dashboard

### GPT embeddings

`_scripts/gpt_search.py` implements a smart search. To get it working:

1. Put in your OpenAI key at the top of the file.
2. Open terminal and create an alias. My tool is called `nmr` but you can call it something else. 

```
alias nmr="cd $HOME/ObsidianVault && python _scripts/gpt_search.py"
```

## Organising my Second Brain

The ideas behind this are discussed in the blog posts, but here is a reference.

### Folders

- Underscore folders represent Obsidian internals
- `Topics` stores Topic types for faster browsing
- `Sources` contains my notes on any information media: books, articles, videos etc
- `Molecules` contains my personal observations/ideas/thoughts
- `Authors` are Source note authors.
- Atoms go in the top level

### Tags

I use tags to represent "is-a" relations (i.e types)

- Core types:
	- atom: the base note type for an individual piece of knowledge derived from a source
	- molecule: my own observation – a permanent note
	- topic: used to signify that a note is a category placeholder
	- author: the creator of a piece of content
	- todo: something I need to fill in
	- project: a long-term project
- Source types:
	- book
	- article: e.g blog post, web article
	- post: social media / forum
	- academic: textbook, journal article
	- video
	- podcast
	- primer (e.g sellside)
	- presentation
	- course 
- Atom types:
	- tool: something that I can use to solve a problem
	- cognitive-bias
	- framework: a way of thinking about the world
	- school-of-thought: a historical school of thought
	- theorem: a mathematical law
	- person: someone of note
	- event: a historical event
	- amusing: a popular saying, aphorism, "law"
	- heuristic: a "common wisdom" way of doing something
	- trading-strat: a trading strategy
	- instrument: a financial instrument

