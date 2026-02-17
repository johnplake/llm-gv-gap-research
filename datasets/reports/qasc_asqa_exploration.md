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

### Examples (sampled across splits)

#### QASC example 1 (train)
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

#### QASC example 2 (train)
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

#### QASC example 3 (test)
**Q:** What will a substance taste like if it changes a litmus paper red?

**Candidate answers (8-way MCQ):**
- A. Anthax
- B. Sour
- C. Sweet
- D. black
- E. Hot
- F. Bitter
- G. lead
- H. urine

#### QASC example 4 (test)
**Q:** What can cause skidding?

**Candidate answers (8-way MCQ):**
- A. mosses, liverworts, hornworts
- B. changes in the environment
- C. making a slow turn
- D. stopping the car quickly
- E. electrical impulses
- F. keeping the car turned off
- G. gently easing on the brakes
- H. dust particles

#### QASC example 5 (validation)
**Q:** a surface that is not what is likely to be covered with something that eats and digests foods?

**Candidate answers (8-way MCQ):**
- A. cartilage
- B. plastic
- C. dirty
- D. sterilized ✅
- E. a hosta
- F. covered in bacteria
- G. Unsafe
- H. tooth enamel

**Supporting facts:**
- fact1: Any surface that has not been sterilized is likely to be covered with bacteria.
- fact2: Bacteria eat and bacteria digest foods.

#### QASC example 6 (validation)
**Q:** Absorption of minerals occurs mainly where?

**Candidate answers (8-way MCQ):**
- A. unicellular organisms
- B. trees and flowers
- C. the Himalayas
- D. small intestine ✅
- E. the environment
- F. flagella
- G. after the snow melts
- H. Microscopic vessels.

**Supporting facts:**
- fact1: Absorption of nutrients occurs mainly in the small intestine.
- fact2: Food and minerals are both nutrients.

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

### Examples (sampled across splits)

#### ASQA example 1 (train)
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

#### ASQA example 2 (train)
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

#### ASQA example 3 (dev)
**Ambiguous Q:** Who is the present game minister of india?

**Disambiguations (qa_pairs):**
- 1. Who is the 12th game minister of india?
  - short answers: Rajyavardhan Singh Rathore, Col. Rajyavardhan Singh Rathore, AVSM
- 2. Who is the 11th game minister of india?
  - short answers: Vijay Goel
- 3. Who is the 10th game minister of india?
  - short answers: Jitendra Singh

**One long-form reference answer (annotations[0].long_answer):**
> The 10th Minister of Youth Affairs and Sports was Jitendra Singh, the 11th was Vijay Goel and the 12th was Rajyavardhan Singh Rathore.

#### ASQA example 4 (dev)
**Ambiguous Q:** Who sings i'll be seeing you in the notebook?

**Disambiguations (qa_pairs):**
- 1. Who sings "I'll Be Seeing You" in the movie The Notebook?
  - short answers: Jimmy Durante.
- 2. Who sings a version of "I'll Be Seeing You" in The Notebook?
  - short answers: Billie Holiday
- 3. Who sings the version of "I'll Be Seeing You" that is heard second in The Notebook?
  - short answers: Jimmy Durante
- 4. Who sings the version of "I'll Be Seeing You that is heard first in The Notebook?
  - short answers: Billie Holiday

**One long-form reference answer (annotations[0].long_answer):**
> In the 2006 romantic novel (The Notebook) that was later adapted into a film in 2004, American actor and singer Jimmy Durante's 1960's song "I'll Be Seeing You" is heard second in movie. The first time this song is heard in the movie is in a version sang by Billie Holiday.
