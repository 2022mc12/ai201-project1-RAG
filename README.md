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
500 characters

**Overlap:**
100 characters

**Why these choices fit your documents:**
Chunk size: I will split the document by paragraph first, since most of the reddit posts are few sentences and the newspaper/blogs have short paragraphs. I will then split this further by checking the size of each paragraph: if the paragraph exceeds 500 characters (I estimated this threshold), I will split it into n even chunks so each chunk is less than 500 characters.

Overlap: I will keep a overlap of 100 characters (this is roughly one sentence) in order to preserve the context of the chunks. Note that I will only do this if I am splitting a paragraph: if the entire paragraph fits in one chunk, no overlap is needed.

**Final chunk count:**
290

**Example Chunks:**

Chunk 1  [source: Reddit]  [file name: Commuter Advice Post] (14 chars)
Wallet. Water.

Chunk 2  [source: School Newspaper]  [file name: Off Campus Housing] (499 chars)
Just off the Brooklyn and Manhattan Bridges, Downtown Brooklyn and Brooklyn Heights offer the best residential proximity to Tandon students. Spanning from Brooklyn Bridge Park to York Street in the north, to Dekalb Avenue and Schermerhorn Street in the south, the area is very residential and offers unrivaled views of lower Manhattan. For commuters, the F and R trains offer less than 30 minute rides to stations near campus like Broadway-Lafayette Street, West Fourth Street and Eighth Street-NYU.

Chunk 3  [source: Reddit]  [file name: Commuter Experience Post] (307 chars)
sting having to commute almost daily? I feel like NYU already not having a campus, along with Tandon being even more separated, could give me trouble with making friends and all that. How difficult is it to be in clubs? I’ve heard that most of the activities would be at night, so how would you manage that?

Chunk 4  [source: School Newspaper]  [file name: Commuting Effects on College Experience] (391 chars)
is a current Steinhardt graduate student from New Jersey who also completed her undergraduate at the same school. Patel has commuted every year besides her first-year as an undergraduate student where she lived in the dorms. As a commuter, Patel shared that she also felt lonely in the city because she wasn’t making as many friends or developing the friendships she already had.

Chunk 5  [source: School Newspaper]  [file name: Off Campus Housing] (360 chars)
Newtown Creek to the south, its location in Queens offers another cheap option to NYU students looking for more affordable housing. While its production-focused history gives the neighborhood an industrial feel, new housing developments have recently added a modern touch, making the area a less hectic option that still retains the look of downtown Manhattan.


---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**
all-MiniLM-L6-v2
**Production tradeoff reflection:**
I will use all-MiniLM-L6-v2 via sentence-transformer because it is efficient and works well for my data chunks (short paragraphs).

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**
     "You are a careful question-answering assistant. Answer the user's "
        "question using ONLY the source excerpts provided in the user message.\n\n"
        "Rules:\n"
        "- Ground every claim in the excerpts. Do not use outside knowledge, "
        "assumptions, or guesses.\n"
        "- Each excerpt is tagged with its origin as [source — filename]. When you "
        "use information from an excerpt, cite that origin inline (e.g. "
        "\"according to [Reddit — Commuter Advice Post]\").\n"
        "- If the excerpts only partially answer the question, answer what you can "
        "and state clearly what is missing.\n"
        "- If the excerpts do not contain the answer, do not invent one. Respond "
        "exactly with: \"I couldn't find anything relevant in the loaded documents. "
        "Please rephrase your question.\"\n"
        "- Be concise and direct. Do not repeat the question back."
**How source attribution is surfaced in the response:**
It asks the LLM to cite the source in the format of [source-filename] and also ask it to clearly state if the excerpts don't contain the answer.

---
## Query Interface
**Input:** Question about commuter student experience/advice at NYU

**Output:** LLM generated answer that references given sources

**Example Query:** What do students think about commuting from NJ?

**Example Response:** According to [Reddit — Commuter Experience Post], students commuting from NJ express concerns about feeling isolated and exhausted due to daily commuting. One student mentions that they think they "will totally feel the same way" when commuting from NJ, implying that they anticipate feeling isolated. Another student who commuted from a different location (Staten Island) had a "nonexistent social life" and found it "impossible to make friends" due to commuting, but it's not directly stated if this is the same for NJ commuters.

---

## Retrieval — Relevant Chunks Returned for Queries
Query 1: What are some recommended things to do during your commute?

Returned Chunks:
* Student Blog — Transportation Experience: For those who are new to commuting, my biggest advice is to make the most of your travel time and, most importantly, pay attention. Yes, download your readings, listen to podcasts related to your coursework, or practice a language if you’re learning one while commuting, but also be observant. The city never sleeps, meaning it’s constantly changing. Keep up!
* Reddit — Commuter Advice Post: Commuter kids, what do you not leave the house without?
* Reddit — Commuter Experience Post: This is comforting to hear cuz I think I will totally feel the same way. I live in NJ and that's how I feel when I come home on weekends. Trying commuting for this semester, lets see how it goes :')

Explanation: The first chunk is relevant because it directly answers the question. The second and third chunks are relevant to commuting advice but does not answer the question.

Query 2: What do students think about commuting from NJ
* Reddit — Commuter Experience Post: Next year I’m going to be commuting from NJ all the way down to Brooklyn, I wanted to ask others here who may also be commuting from Jersey. Do you feel isolated from the rest of the students here? Is it exhausting having to commute almost daily? I feel like NYU already not having a campus, along with Tandon
* Reddit — Commuter Experience Post: This is comforting to hear cuz I think I will totally feel the same way. I live in NJ and that's how I feel when I come home on weekends. Trying commuting for this semester, lets see how it goes :')
* Reddit — Commuter Experience Post: As a commuter student that commuted from Staten island during the first semester of my freshman year…. It was TERRIBLE… I had a nonexistent social life and it was impossible to make friends.. Going to clubs were inconvenient because of the time conflicts and I lose even more time commuting back home.. Glad I stopped commuting after that semester.

Explanation: The first and second chunks are relevant because it directly answers the question (commuting from NJ). The third chunk is relevant to commuting advice but is referring to Staten Island instead of NJ.

Query 3: What do students say about attending clubs to meet new people on campus? 
* Student Blog — Transportation Experience: t of your comfort zone to attend campus events, especially if it’s your first time around. But the more you stick around after class—joining clubs, making and hanging out with friends—the more NYU feels like home. There is a community for commuters within NYU . You are left feeling as though you never really left campus in the first place. As a commuter student, I am a part of many clubs, in

* Student Blog — Transportation Experience: ou never really left campus in the first place. As a commuter student, I am a part of many clubs, including Gentlemen of Quality , Academic Achievement Program and even CAS Presidential Honors Program . Most of my friends come from these clubs and programs. Thinking back to my first year at NYU, I remember signing up for drag bingo with all my friends and ending up winning the grand prize.

* School Newspaper — Commuting Effects on College Experience: “I wasn’t on campus as much and didn’t get to hang out with them [my friends] often and make stronger bonds,” she said.

---
## Grounded Generation with Source Attribution
Source Attribution: 
Q: What are some recommended things to do during your commute?

A: According to [Student Blog — Transportation Experience], recommended things to do during your commute include downloading readings, listening to podcasts related to coursework, or practicing a language. Additionally, it is advised to be observant of the city as it is constantly changing.

Q: What do students think about commuting from NJ 

A: According to [Reddit — Commuter Experience Post], students commuting from NJ express concerns about feeling isolated and exhausted due to daily commuting. One student mentions that they think they "will totally feel the same way" when commuting from NJ, implying that they anticipate feeling isolated. Another student who commuted from a different location (Staten Island) had a "nonexistent social life" and found it "impossible to make friends" due to commuting, but it's not directly stated if this is the same for NJ commuters.


out-of-scope query:

Q: Does the school offer free Metrocards? 

A: I couldn't find anything relevant in the loaded documents. Please rephrase your question.

---
## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->


| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What are the names of the commuter spaces on the Manhattan campus? | Kimmel Commuter Lounge and Lipton Commuter Den| According to [University Page — NYU Commuter Resource Page], the names of the commuter spaces are not specified, it only mentions that commuter students have access to "a variety of spaces and lounges" but does not provide a list of their names. | Relevant | Inaccurate |
| 2 | Does the school offer free Metrocards? | No| I couldn't find anything relevant in the loaded documents. Please rephrase your question. | Off-target | Inaccurate|
| 3 | What are some recommended things to do during your commute?| Listen to podcasts, be observant, do class readings.|According to [Student Blog — Transportation Experience], recommended things to do during your commute include downloading readings, listening to podcasts related to coursework, or practicing a language. Additionally, it is advised to be observant of the city as it is constantly changing.| Relevant | Accurate|
| 4 | What do students think about commuting from NJ | General concensus is that it can be a very long commute (varies from 1-3 hours) and that it can be exhausting. Few students mentioned that it is not that bad once you get used to it.| According to [Reddit — Commuter Experience Post], students commuting from NJ express concerns about feeling isolated and exhausted due to daily commuting. One student mentions that they think they "will totally feel the same way" when commuting from NJ, implying that they anticipate feeling isolated. Another student who commuted from a different location (Staten Island) had a "nonexistent social life" and found it "impossible to make friends" due to commuting, but it's not directly stated if this is the same for NJ commuters. | Relevant | Partially accurate|
| 5 | What do students say about attending clubs to meet new people on campus? | Most agree that it is a good way to meet new people, and it is what you make of it. | According to [Student Blog — Transportation Experience], as a commuter student, the author is "a part of many clubs, including Gentlemen of Quality, Academic Achievement Program and even CAS Presidential Honors Program" and states that "Most of my friends come from these clubs and programs." This suggests that attending clubs can be an effective way for students to meet new people on campus. | Relevant | Accurate|

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
What are the names of the commuter spaces on the Manhattan campus? 

**What the system returned:**
According to [University Page — NYU Commuter Resource Page], the names of the commuter spaces are not specified, it only mentions that commuter students have access to "a variety of spaces and lounges" but does not provide a list of their names. 

**Root cause (tied to a specific pipeline stage):**
The chunking was not ideal for this specific part because the answer was split into a separate chunk (the author created a new paragraph for this). The chunk with the answer did not have the context (commuter spaces) so the model is not able to recognize this.

**What you would change to fix it:**
I would use different chunking strategies for different documents. I think my method works well for the reddit posts and the articles in general, but having 2 different strategies might be better.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**
I was able to use that as a reference to ask Claude to generate code. It was very detailed and I did not have to provide too much extra context because it is all there.

**One way your implementation diverged from the spec, and why:**
I added a MIN CHAR limit for my chunks because after seeing the chunks, I noticed that some chunks are very small and do not provide useful information (some replies for Reddit posts are one or two words).

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

- *What I gave the AI:* I gave Claude my retrieval approach section and pipeline diagram from my planning doc and told it to generate the embedding step.
- *What it produced:* It produced code to loading chunks from my ingestion pipeline, embedding with all-MiniLM-L6-v2, and store chunks in ChromaDB with source metadata.
- *What I changed or overrode:* It used the sentence transformer library and I changed it so that it is using the built-in sentence transformer model in Chroma DB instead.

**Instance 2**

- *What I gave the AI:* I gave Claude my chunking approach section and pipeline diagram from my planning doc and told it to generate the chunking step.
- *What it produced:* It produced code to create chunks from my raw text data.
- *What I changed or overrode:* The code worked well, but did not address edge cases (for example, very small chunks). I have to add in an minimum threshold for the chunk size to filter out small chunks that are not helpful.
