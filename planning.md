# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
I will be focusing on resources and advice for commuter students at NYU. This knowledge is valuable and difficult to find because there are very few official resources available. Relevant information is scattered across different forums, discussion threads, and websites, making it time-consuming for students to locate the answers they need. This RAG system will consolidate these resources into a single searchable knowledge base, allowing students to quickly find relevant information without manually searching through numerous webpages and online discussions.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1-15 | Reddit | Top 15 Reddit posts when I search "Resources and advice for commuter students" in the r/nyu subreddit. | [Reddit results link](https://www.reddit.com/r/nyu/search/?q=Resources+and+advice+for+commuter+students+&cId=d94a4d0f-e50c-47e3-92a9-1f2b6bd50214&iId=cb863939-7957-4351-b192-b3ffd1665d74)|
| 16-25 | School Newspaper | Top 10 School Newspaper articles when I search "Commuter student" in the search bar| [Article results link](https://nyunews.com/?s=commuter+student)|
| 26-28 | Student Blogs| Top 3 search results (I extracted 3 from the search results page instead of deciding on a random number here)| [Search Results Link](https://meet.nyu.edu/?s=commuter)|
| 29 | University Page| NYU Neighborhood Resource Page| [NYU Neighborhood Resource Page](https://www.nyu.edu/students/student-information-and-resources/neighborhood-resources.html?challenge=d06e90d7-4d8f-4b88-9d8c-10b73beb60f1)|
| 30 | University Page | NYU Commuter Resource Page | [NYU Commuter Resource Page](https://www.nyu.edu/students/communities-and-groups/commuters-off-campus-students/involvement.html?challenge=d06e90d7-4d8f-4b88-9d8c-10b73beb60f1)|

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**
I will split the document by paragraph first, since most of the reddit posts are few sentences and the newspaper/blogs have short paragraphs. I will then split this further by checking the size of each paragraph: if the paragraph exceeds 500 characters (I estimated this threshold), I will split it into n even chunks so each chunk is less than 500 characters.

**Overlap:**
I will keep a overlap of 100 characters (this is roughly one sentence) in order to preserve the context of the chunks. Note that I will only do this if I am splitting a paragraph: if the entire paragraph fits in one chunk, no overlap is needed.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**
I will use all-MiniLM-L6-v2 via sentence-transformer because it is efficient and works well for my data chunks (short paragraphs).

**Top-k:**
I will use top 3 retrieved chunks in order to provide the LLM with relevant data and to minimize noise.

**Production tradeoff reflection:**
If I were deploying this system for real users, I would prioritize retrieval quality over computational efficiency and use a larger, higher-performing embedding model instead of all-MiniLM-L6-v2. 
---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What are the names of the commuter spaces on the Manhattan campus? | Kimmel Commuter Lounge and Lipton Commuter Den|
| 2 | Does the school offer free Metrocards? | No|
| 3 | What are some recommended things to do during your commute?| Listen to podcasts, be observant, do class readings.|
| 4 | What do students think about commuting from NJ | General concensus is that it can be a very long commute (varies from 1-3 hours) and that it can be exhausting. Few students mentioned that it is not that bad once you get used to it.|
| 5 | What do students say about attending clubs to meet new people on campus? | Most agree that it is a good way to meet new people, and it is what you make of it. |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. Reddit users has varying opinions on some topics (for example, how bad/good the commute is from NJ) and the RAG system should be able to acknowledge that instead of just agreeing with one side.

2. For the larger paragraphs, it will be split further into smaller chunks, which can split key information. 

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

Document Ingestion (Webscraping via Selenium) -> Chunking (Python) -> Embedding + Vector Store (all-MiniLM-L6-v2 via sentence-transformers + ChromaDB) -> Retrieval (ChromaDB) -> Generation (Groq API using llama-3.3-70b-versatile model)
      
---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**
I will give Claude the Documents I am using, and ask it to come up with code I can use to scrape the data from the sources. Then I will read over it and make edits to ensure that it matches what I want it to do. I will verify by checking the final outputted text files. 

**Milestone 4 — Embedding and retrieval:**
I will give Claude my Chunking Strategy section and ask it to implement chunk_text(). I will verify by printing out random chunks to ensure that the text is split as expected.

**Milestone 5 — Generation and interface:**
I will give Claude the UI requirements section and ask it to come up with a simple web UI using Gradio. I will verify by going to `http://localhost:7860` and check that the UI is working.