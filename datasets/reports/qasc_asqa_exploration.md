# QASC + ASQA dataset exploration

This report focuses on: what’s in the dataset, and concrete Q/answers examples.

## QASC (`allenai/qasc`)

**High-level:** Multiple *candidate answers* per question (8-way MCQ), with a single labeled correct choice (`answerKey`).

### Splits
- train: 8,134
- test: 920
- validation: 926

### Fields
- columns: `['id', 'question', 'choices', 'answerKey', 'fact1', 'fact2', 'combinedfact', 'formatted_question']`

### Where are the ‘multiple answers’? 
- `choices.text` contains **8 candidate answer strings**
- `answerKey` selects the correct one

### Examples

#### QASC example 1
**Q:** What can a certain protein affect in meat?

**Candidate answers (8-way MCQ):**
- A. health
- B. piousness
- C. stamina
- D. retina
- E. toughness ✅
- F. liveliness
- G. saltiness
- H. Energy

**Supporting facts:**
- fact1: Cartilage is a tough tissue that contains a protein called collagen.
- fact2: Collagen contributes to meat toughness.

#### QASC example 2
**Q:** What forms when molecules react with one another?

**Candidate answers (8-way MCQ):**
- A. biochemistry
- B. Chemical energy
- C. Energy.
- D. atoms
- E. chemical bonds ✅
- F. elements
- G. flow of electrons
- H. Organic compounds

**Supporting facts:**
- fact1: Chemical bonds form when substances react with one another.
- fact2: All substances are composed of molecules.

#### QASC example 3
**Q:** Using what can require burning gasoline?

**Candidate answers (8-way MCQ):**
- A. Lead
- B. oil
- C. calculator
- D. woodfire
- E. fire
- F. running shoes
- G. coal
- H. car ✅

**Supporting facts:**
- fact1: using a gasoline engine requires burning gasoline
- fact2: After the car is moving, the gasoline engine kicks in.

## ASQA (`din0s/asqa`) — Answer Summaries for Questions which are Ambiguous

**High-level:** One ambiguous question + multiple disambiguated QA pairs (`qa_pairs`), plus long-form reference answers (`annotations[].long_answer`).

### Splits
- train: 4,353
- dev: 948

### Fields
- columns: `['ambiguous_question', 'qa_pairs', 'wikipages', 'annotations', 'sample_id']`

### Where are the ‘multiple answers’? 
- `qa_pairs` is a list: each element has a disambiguated `question` and a list of short answers in `short_answers`
- `annotations` contains one or more long-form answers that (ideally) cover all disambiguations

### Examples

#### ASQA example 1
**Ambiguous Q:** When do jim and pam kiss in the office?

**Disambiguations (qa_pairs):**
- 1. When is the episode of season 2 where jim and pam kiss in the office?
  - short answers: May 11, 2006
- 2. When is the episode of season 4 where jim and pam kiss in the office?
  - short answers: October 4, 2007
- 3. What episode of season 2 do jim and pam kiss in the office?
  - short answers: Episode 22, Casino Night
- 4. What episode of season 4 do jim and pam kiss in the office?
  - short answers: Dunder Mifflin Infinity, Episodes 3/4

**One long-form reference answer (annotations[0].long_answer):**
> Pamela Halpert is a fictional character on the U.S. television sitcom The Office, played by Jenna Fischer. Her character shares romantic interest with Jim Halpert, whom she begins dating in the fourth season. In episode 22 named Casino Night, Jim and Pam kiss after Jim tells Pam that he is in love with her. This episode aired on May 11, 2006. In the season 4 premiere Fun Run, Jim and Pam confess that they have started dating after the camera crew catches them kissing. The office ultimately learns of their relationship in Dunder Mifflin Infinity. Fun Run aired on September 27, 2007 and Dunder Mifflin Infinity aired on October 4, 2007.

#### ASQA example 2
**Ambiguous Q:** Whats the name of the evil queen in snow white?

**Disambiguations (qa_pairs):**
- 1. What's the actual name of the evil queen in snow white?|What's the name of the evil queen in snow white called by the people?
  - short answers: Queen Grimhilde
- 2. What's the name of the evil queen in snow white called by the dopey?
  - short answers: The Evil Queen
- 3. What's the name of the evil queen in snow white called by the grumpy?
  - short answers: the Wicked Queen
- 4. What's the name of the evil queen in snow white in relation to snow white?
  - short answers: Snow White's stepmother

**One long-form reference answer (annotations[0].long_answer):**
> In the 1937 Walt Disney film Snow White and the Seven Dwarfs, the Queen was originally to be named Queen Grimhilde, but she is never actually named in the film. However, in the 1937–1938 film tie-in serial comic strip Snow White and the Seven Dwarfs written by Merrill De Maris, one of the writers of the Disney film, the Queen is actually named Queen Grimhilde. Additionally, in Walt Disney's 1937 animated feature film Snow White and the Seven Dwarfs, the Evil Queen is known as the Wicked Queen or just the Queen. This character is based on the Evil Queen character from the 1812 German fairy tale Snow White by the Brothers Grimm. However, in the film, Walt Disney changed the Queen from Snow White's biological mother to Snow White's stepmother.

#### ASQA example 3
**Ambiguous Q:** When did the movie incredible's come out?

**Disambiguations (qa_pairs):**
- 1. When did the movie incredible's come out at BFI London Film Festival?
  - short answers: October 27, 2004
- 2. When did the movie incredible's come out in the United States?
  - short answers: November 5, 2004

**One long-form reference answer (annotations[0].long_answer):**
> The Incredibles is a 2004 American computer-animated superhero film produced by Pixar Animation Studios and released by Walt Disney Pictures, set in a fictitious version of the 1960s following Bob and Helen Parr, a couple of superheroes, known as Mr. Incredible and Elastigirl, who hide their powers in accordance with a government mandate, and attempt to live a quiet suburban life with their three children. Bob's desire to help people draws the entire family into a confrontation with a vengeful fan-turned-foe. The film premiered on October 27, 2004, at the BFI London Film Festival and had its general release in the United States on November 5, 2004.
