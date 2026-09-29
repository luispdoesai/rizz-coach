# 📚 Coaching Methodologies & Behavioral Science Frameworks

OpenWingman is built on empirically verified behavioral science, relationship research, and established modern dating coaching frameworks. Rather than relying on outdated "pickup artist" (PUA) gimmicks or generic platitudes, every engine in OpenWingman enforces proven principles from world-renowned dating experts.

---

## 🏛️ The 5 Pillars of OpenWingman

### 1. Mark Manson (*Models: Attract Women Through Honesty*)
* **Non-Neediness & Demeanor**: High attractiveness is driven by non-neediness—communicating desire without seeking validation or approval. The person who invests less anxiety holds the frame.
* **Polarization**: Safe, agreeable small talk kills romantic tension. True polarization means expressing distinctive opinions and playful stances that filter for genuine compatibility.
* **Vulnerability Without Over-Sharing**: Being authentic without dumping emotional baggage or pedestalizing matches.
* *Engine Integration*: [`analyzer.md`](file:///Users/luispadilla/Desktop/rizz-coach/rizz_coach/prompts/analyzer.md), [`scorer.md`](file:///Users/luispadilla/Desktop/rizz-coach/rizz_coach/prompts/scorer.md), [`profile.md`](file:///Users/luispadilla/Desktop/rizz-coach/rizz_coach/prompts/profile.md)

---

### 2. Logan Ury (*How to Not Die Alone*, Director of Relationship Science at Hinge)
* **Anti-Interview Mode**: Banning resume-like small talk ("How was your day?", "What do you do for work?", "Where are you from?"). Replacing them with experiential hooks and situational banter.
* **The Momentum Rule**: Conversations on dating apps decay rapidly after 4–8 exchanges. OpenWingman prioritizes transitioning from text to in-person dates within the first week.
* **Prompt Specificity**: Profile prompts that are generic ("I love traveling, tacos, and dogs") fail. Prompts must be concrete and offer an effortless conversational runway.
* *Engine Integration*: [`scorer.py`](file:///Users/luispadilla/Desktop/rizz-coach/rizz_coach/core/scorer.py), [`profile.py`](file:///Users/luispadilla/Desktop/rizz-coach/rizz_coach/core/profile.py), [`autopsy.py`](file:///Users/luispadilla/Desktop/rizz-coach/rizz_coach/core/autopsy.py)

---

### 3. Matthew Hussey (*Get the Guy*)
* **"Dropping the Handkerchief"**: Making it effortless and inviting for the other person to participate by leaving open loops and curiosity gaps.
* **Playful Challenge**: Communicating high standards with charm, avoiding passivity or over-eagerness.
* **Unbothered Revivals**: When a match ghosts, never send passive-aggressive texts. Send curiosity pings or playful frame-flips that restart momentum with zero guilt.
* *Engine Integration*: [`autopsy.md`](file:///Users/luispadilla/Desktop/rizz-coach/rizz_coach/prompts/autopsy.md), [`analyzer.md`](file:///Users/luispadilla/Desktop/rizz-coach/rizz_coach/prompts/analyzer.md)

---

### 4. Todd V / Modern Communication Coaches
* **Calibrated Push-Pull**: Balancing interest (pull) with playful disqualification or teasing (push) to create dynamic tension rather than predictable validation.
* **Effort & Investment Calibration**: Never sending a 40-word paragraph in response to a 3-word text. Matching pacing prevents looking desperate.
* **False Time Constraints & Low-Pressure Logistics**: Proposing dates with relaxed parameters ("Grabbing a quick drink on Thursday around Soho, come join for 30 mins") to eliminate awkward pressure.
* *Engine Integration*: [`scorer.md`](file:///Users/luispadilla/Desktop/rizz-coach/rizz_coach/prompts/scorer.md), [`analyzer.md`](file:///Users/luispadilla/Desktop/rizz-coach/rizz_coach/prompts/analyzer.md), [`automation.py`](file:///Users/luispadilla/Desktop/rizz-coach/rizz_coach/core/automation.py)

---

### 5. Blaine Anderson (*Dating by Blaine*)
* **Photo Hierarchy**: 
  - Photo 1: Direct eye contact, clear smile with teeth, flattering natural lighting, no hats or sunglasses.
  - Photo 2: Full-length body shot in a stylish outfit.
  - Photo 3: Candid social proof / with friends.
  - Photo 4: Active hobby/lifestyle.
* **Cliche Eradication**: Eliminating gym mirror selfies, car selfies, and ambiguous group pictures.
* *Engine Integration*: [`profile.md`](file:///Users/luispadilla/Desktop/rizz-coach/rizz_coach/prompts/profile.md)

---

## 📂 Managing & Customizing Prompts

All system prompts are isolated into standard Markdown files located in [`rizz_coach/prompts/`](file:///Users/luispadilla/Desktop/rizz-coach/rizz_coach/prompts/):
- [`analyzer.md`](file:///Users/luispadilla/Desktop/rizz-coach/rizz_coach/prompts/analyzer.md): Subtext translation, frame holder, investment ratio, and 3 tactical moves.
- [`scorer.md`](file:///Users/luispadilla/Desktop/rizz-coach/rizz_coach/prompts/scorer.md): Message rating, anti-pattern cringe flags, and +20 Rizz rewrite.
- [`profile.md`](file:///Users/luispadilla/Desktop/rizz-coach/rizz_coach/prompts/profile.md): Photo audit, bio critique, and 3 high-converting bio replacements.
- [`autopsy.md`](file:///Users/luispadilla/Desktop/rizz-coach/rizz_coach/prompts/autopsy.md): Ghosting diagnostic, fatal turn detection, and revival texts.
- [`gym.md`](file:///Users/luispadilla/Desktop/rizz-coach/rizz_coach/prompts/gym.md): Sparring persona roleplay and sideline coaching tips.

You can edit these markdown files at any time to tweak tone, add new rules, or adapt them to your dating style!
