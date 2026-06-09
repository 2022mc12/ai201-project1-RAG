# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

I will be focusing on resources and advice for commuter students at NYU. This knowledge is valuable and difficult to find because there are very few official resources available. Relevant information is scattered across different forums, discussion threads, and websites, making it time-consuming for students to locate the answers they need. This RAG system will consolidate these resources into a single searchable knowledge base, allowing students to quickly find relevant information without manually searching through numerous webpages and online discussions.
---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->


| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Reddit | Incoming Freshman Commuter Post | [Reddit link](https://www.reddit.com/r/nyu/comments/wvd2mv/incoming_freshman_commuter_how_do_you_throw/)|
| 2 | Reddit | Commuter Experience | [Reddit link](https://www.reddit.com/r/nyu/comments/19cjab1/commuters_how_is_your_college_experience/)|
| 3 | Reddit |Commuter Dining Plan Post | [Reddit link](https://www.reddit.com/r/nyu/comments/1g4djm0/nyu_no_one_wants_your_rip_off_commuter_plan/)|
| 4 | Reddit | Commuter Financial Aid Post | [Reddit link](https://www.reddit.com/r/nyu/comments/kibfsz/commuter_financial_aid/)|
| 5 | Reddit | Commuter Advice Post | [Reddit link](https://www.reddit.com/r/nyu/comments/oq36pn/commuter_kids_what_do_you_not_leave_the_house/)|
| 6 | School Newspaper | Commuting Effects on College Experience: Socially, Professionally, and Mentally| [Article link](https://nyunews.com/uta/features/2020/04/06/being-a-commuter-at-nyu/)|
| 7 | School Newspaper | Off Campus Housing| [Article link](https://nyunews.com/underthearch/housing/2025/3/11/neighborhood-guide/)|
| 8 | Student Blog| Transportation Experience| [Meet NYU Blog](https://meet.nyu.edu/advice/life-on-the-move-navigating-nyc-as-an-nyu-commuter-student/)|
| 9 | University Page| NYU Neighborhood Resource Page| [NYU Neighborhood Resource Page](https://www.nyu.edu/students/student-information-and-resources/neighborhood-resources.html?challenge=d06e90d7-4d8f-4b88-9d8c-10b73beb60f1)|
| 10 | University Page | NYU Commuter Resource Page | [NYU Commuter Resource Page](https://www.nyu.edu/students/communities-and-groups/commuters-off-campus-students/involvement.html?challenge=d06e90d7-4d8f-4b88-9d8c-10b73beb60f1)|


---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**

**Overlap:**

**Why these choices fit your documents:**

**Final chunk count:**

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**

**Production tradeoff reflection:**

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*
