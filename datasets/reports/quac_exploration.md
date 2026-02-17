# QuAC dataset exploration

This report focuses on: what’s in the dataset, and concrete Q/answer examples.

## QuAC (`allenai/quac`) — Question Answering in Context

**High-level:** Dialogue-based extractive QA grounded in a Wikipedia section. Each dataset row is a dialogue with lists of questions and answers.

### Splits
- train: 11,567 dialogues
- validation: 1,000 dialogues

### Fields
- columns: `['dialogue_id', 'wikipedia_page_title', 'background', 'section_title', 'context', 'turn_ids', 'questions', 'followups', 'yesnos', 'answers', 'orig_answers']`

### Where are the ‘multiple answers’? 
- The dataset stores answers per-turn inside the `answers` object.
- In multi-reference splits, `answers.texts[turn]` can contain multiple reference spans (a list).

### Examples (sampled across splits)

#### Example 1 (train)
**Wikipedia page:** The Devil Wears Prada (band)
**Section:** With Roots Above and Branches Below (2008-2010)
**Background:** The Devil Wears Prada is an American Christian metalcore band from Dayton, Ohio, formed in 2005. It consists of members Mike Hranica (vocals, additional guitar), Jeremy DePoyster (rhythm guitar, vocals), Kyle Sipress (lead guitar, backing vocals), and Andy Trick (bass). The band had maintained its original lineup until keyboardist James Baney left the band. To date, the group has released six full-length albums: Dear Love:

**First 3 turns:**
- Turn 0: Q: Was 2008 a success for The Devil Wear Prada?
  - A refs: In Autumn 2008, they debuted a song off of the upcoming record while on tour
  - yesno: 0 ; followup: 0
- Turn 1: Q: Was the tour a success?
  - A refs: CANNOTANSWER
  - yesno: 2 ; followup: 1
- Turn 2: Q: What happened to The Devil Wears Prada in 2010?
  - A refs: it was announced that The Devil Wears Prada were voted as 2009's Band of the Year
  - yesno: 2 ; followup: 0

#### Example 2 (train)
**Wikipedia page:** Harry Dexter White
**Section:** Accusations by Jenner and McCarthy 1953
**Background:** Harry Dexter White was born in Boston, Massachusetts, the seventh and youngest child of Jewish Lithuanian immigrants, Joseph Weit and Sarah Magilewski, who had settled in America in 1885. In 1917 he enlisted in the U.S. Army, and was commissioned as lieutenant and served in France in a non-combat capacity in World War I. He did not begin his university studies until age 30, first at Columbia University, then at Stanford University, where he earned a first degree in economics. After completing a Ph.D. in economics at Harvard University at 38 years of age, White taught four years at Lawrence University in Wisconsin.

**First 3 turns:**
- Turn 0: Q: What was the accusation?
  - A refs: looked extensively into the problem of unauthorized and uncontrolled powers exercised by non-elected officials, specifically White.
  - yesno: 2 ; followup: 0
- Turn 1: Q: Was the accusations found to be valid?
  - A refs: Attorney General Herbert Brownell Jr. revealed that the FBI had warned the Truman administration about White before the President appointed him to the IMF.
  - yesno: 2 ; followup: 0
- Turn 2: Q: Why did they warn them?
  - A refs: revealed that the White House had received the FBI report on "Soviet Espionage in the United States," including the White case,
  - yesno: 2 ; followup: 0

#### Example 1 (validation)
**Wikipedia page:** Will Forte
**Section:** Post-SNL, MacGruber and film roles (2011-2014)
**Background:** Orville Willis Forte IV was born in Alameda County, California. His father, Orville Willis Forte III, is a financial broker, and his mother, Patricia C. (nee Stivers), is an artist and former schoolteacher. He was raised in Moraga, before moving to Lafayette. He went by Billy in his early years until he was teased at school for it also being a girl's name, at which point he decided he would from there on be known as Will.

**First 3 turns:**
- Turn 0: Q: What is the relation between Will Forte and film roles
  - A refs: Forte was positive regarding the film, saying, "What you see with this movie is exactly what we wanted to do. It's; He assumed his shot at a film career was ruined, and he imagined that if acting did not work out, he would return to writing primarily.; Forte was positive regarding the film,; his expansion into film with MacGruber,; MacGruber was shot on a tight schedule of 28 days in Albuquerque, New Mexico, during the summer of 2009.
  - yesno: 2 ; followup: 0
- Turn 1: Q: What was Will FOrte role in the movie?
  - A refs: It's the three of us having a bunch of fun writing it, then having fun making it with a bunch of our friends--old friends and new friends.; Forte was positive regarding the film,; writing it, then having fun making it with a bunch of our friends; The film was released in May 2010 and received mixed reviews.
  - yesno: 2 ; followup: 0
- Turn 2: Q: Did the film win any away?
  - A refs: CANNOTANSWER; CANNOTANSWER; CANNOTANSWER
  - yesno: 2 ; followup: 0

#### Example 2 (validation)
**Wikipedia page:** Bernard Lewis
**Section:** Views and influence on contemporary politics
**Background:** Bernard Lewis, FBA (born 31 May 1916) is a British American historian specializing in oriental studies. He is also known as a public intellectual and political commentator. Lewis is the Cleveland E. Dodge Professor Emeritus of Near Eastern Studies at Princeton University. Lewis' expertise is in the history of Islam and the interaction between Islam and the West.

**First 3 turns:**
- Turn 0: Q: What was Bernard's view and influence on contemporary politics?
  - A refs: In 1966, Lewis was a founding member of the learned society, Middle East Studies Association of North America (MESA),; He is a pioneer of the social and economic history of the Middle East and is famous for his extensive research of the Ottoman archives.; Lewis argues that the Middle East is currently backward and its decline was a largely self-inflicted condition resulting from both culture and religion,; Lewis argues that the Middle East is currently backward and its decline was a largely self-inflicted condition resulting from both culture and religion,
  - yesno: 2 ; followup: 0
- Turn 1: Q: Who is the person hat oppose this view?
  - A refs: CANNOTANSWER; CANNOTANSWER; CANNOTANSWER
  - yesno: 2 ; followup: 1
- Turn 2: Q: Does the view has any oposition?
  - A refs: CANNOTANSWER; CANNOTANSWER; CANNOTANSWER
  - yesno: 2 ; followup: 1
