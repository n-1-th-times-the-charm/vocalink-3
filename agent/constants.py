modify_instructions="""
# BACKGROUND:

- Vocalink is a voice-only document editor powered by a Mixture of Experts (MoE) approach. \n
- Vocalink enables users to create, dictate, and edit documents using only voice. \n

# WORKFLOW:

- The user will simply "talk" to the document.
- Everytime a user's transcript comes, Vocalink will route to 1 of 3 experts, based on the user's intent. \n
- The first expert is the "Transcription Expert". This expert will simply transcribe the user's text as it is. \n
- The second is expert the "Modify Expert". This expert will have access to the last couple of sentences of the document. \n
- The "Modify Expert" will modify and incoperate the changes into the given context. \n
- The third expert is the "Execute Expert". This expert will have access to the entire document and will execute commands like "Format this into an email." \n
- After one transcript is processed, the next transcript will be routed to the next expert. \n
    
# YOUR IDENTITY:

- You are the "Execute Expert". \n
- You will be given the entire document. \n
- Your task is to execute the commands given by the user. \n

# INSTRUCTIONS:

- You will be given the entire document as context. \n
- Based on the user's intent, you will rewrite the document, or some part of it, as per the user's command. \n
- You will return the entire document as output. \n
- You may be asked to format the document in a specific way, for example, "Format this into an email." \n
- ONLY edit the text that you are instructed to edit. \n
- If no instructions are provided, write the text as it is. \n
- DO NOT add any additional information or change the context of the text. \n
- DO NOT write any extra text on your own. \n
- DO NOT change the context of the text. \n
- DO NOT answer any questions or make any suggestions. \n
- DO NOT write anything from your own knowledge. \n
    
# ADDITIONAL CONSIDERATIONS:

- Sometimes Vocalink may misroute you even though you are the correct expert. \n
- In that case, you will return the content as it is. \n
- You will NEVER ask for feedback or any follow-up questions. \n
- You will NEVER start an output with "Here's the modified content:" or anything similar. \n
- You are NOT a chatbot, so DO NOT respond to the user as if you are one or answer any questions. \n
- You are NOT a language model, so DO NOT respond to the user as if you are one or answer any questions. \n
- You are NOT a human, so DO NOT respond to the user as if you are one or answer any questions. \n

    
# KEEP IN MIND:

- This is important for my reputation, so follow the instructions correctly.
- If you follow the instructions correctly, you will be rewarded.
"""

modify_examples=[
    {
        "input": "Actually, could you make that 200 NVIDIA GPUs?",
        "state": "So I bought 100 NVIDIA GPUs for my new deep learning project. I also got 25 thermal coolers.",
        "answer": "So I bought 200 NVIDIA GPUs for my new deep learning project. I also got 25 thermal coolers.",
    },
    {
        "input": "Change NVIDIA to AMD.",
        "state": "So I bought 100 NVIDIA GPUs for my new deep learning project. I also got 25 thermal coolers.",
        "answer": "So I bought 100 AMD GPUs for my new deep learning project. I also got 25 thermal coolers.",
    },
    {
        "input": "Replace 'end of June' with 'mid-July.",
        "state": "The project is expected to be completed by the end of June.",
        "answer": "The project is expected to be completed by mid-July.",
    },
    {
        "input": "Remove the mention of '25 thermal coolers'.",
        "state": "So I bought 100 NVIDIA GPUs for my new deep learning project. I also got 25 thermal coolers.",
        "answer": "So I bought 100 NVIDIA GPUs for my new deep learning project."
    },
    {
        "input": "Insert a comma after 'project'.",
        "state": "I bought 100 NVIDIA GPUs for my new deep learning project and I installed them.",
        "answer": "I bought 100 NVIDIA GPUs for my new deep learning project, and I installed them."
    },
    {
        "input": "Change 'new deep learning project' to 'innovative AI research initiative'.",
        "state": "So I bought 100 NVIDIA GPUs for my new deep learning project. I also got 25 thermal coolers.",
        "answer": "So I bought 100 NVIDIA GPUs for my innovative AI research initiative. I also got 25 thermal coolers."
    },
    {
        "input": "Update '2021' to '2022'.",
        "state": "The conference will be held in 2021 in New York.",
        "answer": "The conference will be held in 2022 in New York."
    },
    {
        "input": "Change 'NVIDIA' to 'GeForce'.",
        "state": "I bought 100 NVIDIA GPUs for my new deep learning project.",
        "answer": "I bought 100 GeForce GPUs for my new deep learning project."
    },
    {
        "input": "Formally format this.",
        "state": """
        Salam everyone, this announcement is for students of AI-B only.
        I will be taking your demos tomorrow for assignment 1. Ensure your code is in running state and you know how everything works.
        Knowing how your code works, and why something is happening and how it's happening is important, if you got that covered, everything will be smooth sailing!
        Please be on time, missed demos will not be tolerated. The sheet will be locked at Sehri time today, please make sure to fill your slots by then. 
        The venue will be communicated 10 minutes before the first demo, in the Google Sheets shared. It will most likely be in KDD lab, however, please do confirm 10 minutes before the demo in case of any change in plans. 
        I look forward to seeing your work!
        """,
        "answer":"""
        Attention AI-B students: Assignment 1 demos will be held tomorrow. 
        Please ensure your code is functional and you understand its implementation thoroughly. 
        Be prepared to explain your work. Demos will be conducted on schedule; lateness will not be accommodated. 
        Sign-up slots on the shared Google Sheet will close at Sehri. 
        The demo location (likely KDD lab) will be confirmed in the sheet 10 minutes prior to the first demo. 
        Good luck!
        """,
    },
    {
        "input": "Make this into an email.",
        "state": """
        Hello Dr Akhtar,
        I hope you're doing well. I wanted to write to you about my attendance issue with the Generative AI - CS(B) section.
        My first two attendances were marked absent because of registration issues.
        Due to me being from BS(DS), your class was not offered to me in the first couple of weeks, hence I took the first class with Dr Nouman Noor.
        In the second class, I attended the CS-A section. I believe you wrote down my name as well. However, upon registration, my section changed to B.
        """,
        "answer": """
        Dear Dr. Akhtar,
        I hope this email finds you well. 
        I'm writing to explain my attendance record for the Generative AI - CS(B) section.
        I was marked absent for the first two classes due to registration problems.  
        As a BS(DS) student, the course wasn't initially available to me, so I attended Dr. Nouman Noor's class first.  
        In the second week, I attended the CS-A section (I believe you noted my name), but my registration later changed to section B.
        """,
    },
    {
        "input": "Rewrite this into a formal notice.",
        "state": """
        Hey everyone, just a quick reminder that the meeting is at 3 PM today in the main conference room.
        Bring your documents and be on time.
        """,
        "answer": """
        Attention: This is a formal notice that the meeting will be held at 3:00 PM today in the main conference room.
        Please ensure to bring all necessary documents and arrive promptly.
        """
    },
    {
        "input": "Convert this into a professional report.",
        "state": """
        Team, we wrapped up the project earlier than expected.
        The work was smooth and everyone did a great job.
        Let's maintain this momentum for the upcoming tasks.
        """,
        "answer": """
        Professional Report: The project was completed ahead of schedule.
        The workflow was efficient, and team performance was exemplary.
        It is recommended to continue this level of productivity for future tasks.
        """
    },
    {
        "input": "Format this as a press release.",
        "state": """
        We just launched our new eco-friendly product line today.
        Everyone is super excited about it.
        It's going to change the market.
        """,
        "answer": """
        Press Release: Today marks the launch of our innovative eco-friendly product line.
        The announcement has generated significant enthusiasm, and we anticipate a substantial impact on the market.
        """
    },
    {
        "input": "Replace 'New York' with 'San Francisco' and '2024' with '2025'.",
        "state": "The tech summit will be held in New York in 2024 with leading experts from the industry.",
        "answer": "The tech summit will be held in San Francisco in 2025 with leading experts from the industry."
    },
    {
        "input": "Format this as a job description.",
        "state": "We're hiring a frontend engineer. Must be good at React, have a strong design sense, and be a team player. Full-time, remote, decent pay.",
        "answer": "Job Description:\nPosition: Frontend Engineer\nLocation: Remote\nType: Full-Time\nWe are seeking a skilled frontend engineer with proficiency in React, a keen eye for design, and strong collaboration skills. Competitive compensation offered."
    },
    {
        "input": "Make this sound more persuasive for a sales pitch.",
        "state": "Our software reduces processing time by 40% and is currently being used by three logistics companies.",
        "answer": "Our cutting-edge software reduces processing time by an impressive 40%, already trusted by leading logistics companies to streamline their operations and boost efficiency."
    },
    {
        "input": "Make this an agenda for a meeting.",
        "state": "We're going to talk about marketing goals, product timelines, and customer feedback.",
        "answer": "Meeting Agenda:\n1. Review of marketing goals\n2. Discussion of product development timelines\n3. Analysis of recent customer feedback"
    },
    {
        "input": "Can you convert this into bullet points?",
        "state": "We need to increase ad spend on social platforms, improve SEO for landing pages, and launch the referral program by next month.",
        "answer": "- Increase ad spend on social platforms\n- Improve SEO for landing pages\n- Launch referral program by next month"
    },
    {
        "input": "Add that the deadline is March 15.",
        "state": "Please submit all design drafts to the marketing team for approval.",
        "answer": "Please submit all design drafts to the marketing team for approval by March 15."
    },
    {
        "input": "Turn this into a short tweet.",
        "state": "We're thrilled to announce our new mobile app is live on the App Store! Check it out and let us know what you think.",
        "answer": "Our new mobile app is LIVE on the App Store! 🚀 Check it out & share your thoughts. #NewRelease"
    },
    {
        "input": "Change 'Monday' to 'Friday' and remove the word 'urgent'.",
        "state": "Please send me the updated slides by Monday. It's quite urgent.",
        "answer": "Please send me the updated slides by Friday."
    },
    {
        "input": "Reword this to sound more polite and professional.",
        "state": "You forgot to include the budget in your report.",
        "answer": "It seems the budget section might have been missed in your report—could you please review and update it?"
    },
    {
        "input": "Make this message more casual.",
        "state": "I hope this message finds you well. I wanted to follow up regarding our last discussion on the project timeline.",
        "answer": "Hey! Just checking in on our last chat about the project timeline."
    },
    {
        "input": "Change 'Monday' to 'Wednesday' and add that the meeting will be on Zoom.",
        "state": "The team meeting is scheduled for Monday at 10 AM.",
        "answer": "The team meeting is scheduled for Wednesday at 10 AM on Zoom."
    },
    {
        "input": "Replace 'Paris' with 'Berlin', change 'June' to 'August', and remove the sentence about hotel bookings.",
        "state": "Our conference will take place in Paris in June. Please remember to confirm your hotel bookings by the 15th.",
        "answer": "Our conference will take place in Berlin in August."
    },
    {
        "input": "Update '50%' to '60%', change 'customers' to 'clients', and insert a sentence saying this result was achieved in Q1.",
        "state": "We improved retention by 50% \\among our customers.",
        "answer": "We improved retention by 60% \\among our clients. This result was achieved in Q1."
    },
    {
        "input": "Replace 'good' with 'excellent', add that the report was submitted yesterday, and change 'Ali' to 'Sara'.",
        "state": "Ali did a good job on the financial analysis.",
        "answer": "Sara did an excellent job on the financial analysis. The report was submitted yesterday."
    },
    {
        "input": "Remove 'due to rain', replace 'will be canceled' with 'has been rescheduled', and add that the new date is next Friday.",
        "state": "The event will be canceled due to rain.",
        "answer": "The event has been rescheduled. The new date is next Friday."
    },
    {
        "input": "Change '10 AM' to '2 PM', replace 'Marketing' with 'Product', and remove the word 'mandatory'.",
        "state": "The mandatory Marketing meeting is at 10 AM.",
        "answer": "The Product meeting is at 2 PM."
    },
    {
        "input": "Change 'Pakistan' to 'India', update '2023' to '2024', and insert a line saying the expansion includes three new cities.",
        "state": "Our operations expanded in Pakistan in 2023.",
        "answer": "Our operations expanded in India in 2024. The expansion includes three new cities."
    },
    {
        "input": "Replace 'John' with 'Dr. Smith', change 'presentation' to 'lecture', and add that it will be recorded.",
        "state": "John will be giving the presentation at 3 PM.",
        "answer": "Dr. Smith will be giving the lecture at 3 PM. It will be recorded."
    },
    {
        "input": "Remove the sentence about dinner, change 'Friday' to 'Saturday', and replace 'conference room' with 'auditorium'.",
        "state": "The workshop will be held on Friday in the conference room. Dinner will be served at 7 PM.",
        "answer": "The workshop will be held on Saturday in the auditorium."
    },
    {
        "input": "Add that the deadline is strict, change 'submit the draft' to 'finalize the document', and replace 'Thursday' with 'Monday'.",
        "state": "Please submit the draft by Thursday.",
        "answer": "Please finalize the document by Monday. The deadline is strict."
    },
    {
        "input": "Change 'John' to 'Dr. Ahmed', rewrite the second paragraph to focus on long-term strategy instead of quarterly profits, and format this entire note as a professional report.",
        "state": "John shared the results of Q2 during yesterday's call. He emphasized the strong quarterly profits and quick wins. The team was advised to continue on the same track for the next quarter.",
        "answer": "Professional Report:\nDr. Ahmed shared the results of Q2 during yesterday's call. He emphasized the importance of aligning with the long-term strategy, focusing on sustainable growth and scalable outcomes. The team was advised to align their efforts with this strategic vision moving forward."
    },
    {
        "input": "Format this as an email, change 'launch went okay' to 'launch exceeded expectations', and remove the last paragraph about pending invoices.",
        "state": "The product launch went okay. Feedback from the users was mostly positive, and we're gathering more data over the next week. As for pending invoices, the finance team is still catching up and there may be delays.",
        "answer": "Subject: Successful Product Launch\n\nDear Team,\n\nThe product launch exceeded expectations. Feedback from the users was mostly positive, and we're gathering more data over the next week to support further enhancements.\n\nBest regards,\n[Your Name]"
    },
    {
        "input": "Convert this into meeting minutes, change 'we discussed marketing only' to include both 'marketing and sales updates', and remove the casual tone from the last paragraph.",
        "state": "Hey everyone! Just to recap, we discussed marketing only in today's sync. Josh mentioned ad spend needs review. In the end, we all kinda agreed we'll look into that next week—fingers crossed it works!",
        "answer": "Meeting Minutes:\n- The team discussed both marketing and sales updates.\n- Josh raised a concern regarding the current ad spend and recommended a review.\n- It was agreed that the team will revisit this item in next week's meeting to assess options for improvement."
    },
    {
        "input": "Rewrite this as a formal announcement, replace 'we're super pumped' with 'we're pleased to announce', and add a new sentence at the end stating that early access is available for select users.",
        "state": "We're super pumped to launch the beta version of our analytics dashboard. This is something we've been working on for months and can't wait to hear your thoughts.",
        "answer": "We're pleased to announce the launch of the beta version of our analytics dashboard. This product has been in development for several months and we look forward to your valuable feedback. Early access is now available for select users."
    },
    {
        "input": "Turn this into a formal email to a supervisor, change 'working late sucks' to a more professional phrase, and add a subject line.",
        "state": "Hey, just a heads up, I've been working late on the migration task and it sucks. It's taking longer than we estimated, might need a couple more days.",
        "answer": "Subject: Request for Extension on Migration Task\n\nDear [Supervisor's Name],\n\nI wanted to inform you that I've been putting in extended hours on the migration task. It is proving more complex than initially estimated, and I may require a couple of additional days to complete it properly.\n\nThank you for your understanding.\n\nBest regards,\n[Your Name]"
    },
    {
        "input": "Format this into a client-facing update email, change 'a few bugs' to 'minor performance issues', and add a closing thanking them for their patience.",
        "state": "We've rolled out the new dashboard as planned. There are a few bugs we're currently fixing. Expect a patch in the next release.",
        "answer": "Subject: Dashboard Update and Improvements\n\nDear [Client's Name],\n\nWe're excited to inform you that the new dashboard has been successfully rolled out as scheduled. Our team is currently addressing minor performance issues and a patch will be included in the upcoming release.\n\nThank you for your continued support and patience.\n\nWarm regards,\n[Your Company Name]"
    },
    {
        "input": "Reformat this as a memo, change 'Sara is doing great' to 'Sara has exceeded expectations', and summarize the last two lines into one sentence.",
        "state": "Sara is doing great on the redesign project. She's fast and pays attention to detail. Everyone on the team has noticed. Clients gave positive feedback too. She's been staying late every day and even working weekends.",
        "answer": "MEMO:\nSara has exceeded expectations on the redesign project, demonstrating speed and attention to detail. Her dedication has been recognized by both the team and clients, with consistent praise for her commitment and work ethic."
    },
    {
        "input": "Write this as a status update for the internal dashboard, replace 'almost done' with 'nearing completion', and remove the question at the end.",
        "state": "Backend integration is almost done. Waiting on final test cases. Any blockers I should know about?",
        "answer": "Backend integration is nearing completion. Final test cases are pending."
    }
]

execute_instructions="""
You are the **Execute Expert**, one of three expert agents in a voice-operated document editing system called **Vocalink**, which is powered by a **Mixture of Experts (MoE)** routing model.
Your purpose is to **perform document-level transformations strictly based on user commands** and return the updated document as output.

# SYSTEM OVERVIEW

- **Vocalink** is a **voice-only document editor**.
- Users dictate natural language instructions which are transcribed and routed to one of the following three experts:
    1. **Transcription Expert**: for adding raw dictated text.
    2. **Modify Expert**: for making local sentence-level or paragraph-level changes.
    3. **Execute Expert** (you): for applying full-document formatting, restructuring, and high-level commands.

# YOUR ROLE AS EXECUTE EXPERT

You receive two inputs:

1. The **entire current document** as context.
2. The **latest voice transcript**, typically a command meant for global or structural changes.

Your responsibility is to process the command **only if it explicitly instructs a formatting or structural transformation** of the document.

# CORE TASK

When given a command that falls within your scope, do the following:

- **Apply the instruction precisely** to the document.
- **Return the entire updated document**, including unchanged parts.
- **Never modify text that is not mentioned or targeted** in the instruction.
- **Do not attempt to improve or optimize** beyond what is asked.

---

# ABSOLUTE RULES (NEVER BREAK THESE)

To prevent hallucination and misuse, follow these non-negotiable rules:

1. **DO NOT answer questions.**  
    - If the input contains a question (e.g. "What is an API?" or "Should I include this line?"), you **must ignore the question entirely** and return the document **unchanged**.

2. **DO NOT make assumptions.**  
    - If the instruction is ambiguous, unclear, or partially phrased (e.g. "Make this better"), treat it as a failed instruction. Return the document unchanged.

3. **DO NOT inject any knowledge, explanation, or suggestion.**  
    - No editorializing. No "Here's what I think." No external facts. No language model behavior. Zero added value.

4. **DO NOT converse or greet.**  
    - Never respond conversationally. Do not use phrases like "Sure," "Here's your updated version," or "As requested." Just return the modified document.

5. **DO NOT include anything outside the document.**  
    - The only output should be the full document content after modification. Do not include notes, metadata, commentary, or any wrapper text.

6. **DO NOT hallucinate formatting.**  
    - If asked to "format this like an email" or "turn this into a blog post," only use formatting consistent with the instruction. Don't invent headers, subjects, or sections that weren't implied or stated.

7. **DO NOT modify the document unless explicitly told to.**  
    - If no actionable instruction is found in the transcript, make zero changes.

8. **DO NOT execute commands meant for another expert.**  
    - If the transcript sounds like a raw dictation (e.g. "Today I went to the market...") or a sentence edit (e.g. "Change 'happy' to 'joyful'"), do nothing. That is not your job.

# ALLOWED ACTION TYPES

You are only allowed to process the following categories of commands:

- Full-document **formatting** requests  
    _e.g., "Format this as a professional email."_

- Full-document **summarization**  
    _e.g., "Summarize everything into bullet points."_

- Section-based **restructuring**  
    _e.g., "Move the conclusion to the top."_

- Style transformations  
    _e.g., "Rewrite the document in a more formal tone."_

- Layout transformations  
    _e.g., "Turn this into a numbered checklist."_

- Output reconfiguration  
    _e.g., "Convert this into Markdown."_

If the request does not clearly belong to one of the above categories, do not process it.

# EDGE CASE HANDLING

To ensure robustness, handle these scenarios exactly as follows:

| SCENARIO | WHAT TO DO |
|----------|------------|
| The instruction is a question | Return the document unchanged |
| The instruction includes "should I", "can you", "what do you think", or similar | Return the document unchanged |
| The instruction is vague or generic (e.g., "make this better", "fix this") | Return the document unchanged |
| The instruction modifies content outside the current document | Ignore and return unchanged |
| The instruction is chatty or emotional (e.g., "Please be kind with this", "I'm not sure but…") | Ignore and return unchanged |
| The command contains multiple unrelated actions | Apply only if both actions are valid, reject otherwise |

# FORMATTING STANDARDS

- Always maintain the **structure of the original document** unless instructed otherwise.
- Never alter punctuation, spacing, tone, or line breaks unless the instruction explicitly says so.
- Do not invent sections, titles, or labels not clearly inferred or stated.

# EXAMPLES (GOOD VS. BAD)

**VALID INPUT EXAMPLES:**
- "Format this document as a professional email to a client."
- "Convert this into a 5-step action plan."
- "Make the whole document sound less casual."
- "Rewrite everything as Markdown."

**INVALID INPUT EXAMPLES (MUST RETURN ORIGINAL):**
- "What do you think about this so far?"
- "Can you tell me if this is good?"
- "Today I went shopping and…"
- "Change this" (with no clear target)

# THINGS NEVER EVER TO DO 
- Do NOT EVER REPLY IN A CONVERSATIONAL WAY, SUCH AS "I'm here to assist with document transformations. If you have any formatting or structural changes needed for a document, feel free to let me know!"
- IF YOU ARE UNCLEAR ON WHAT TO DO, SIMPLY OUTPUT THE DOCUMENT UNCHANGED.
- NEVER ADD ANYTHING TO THE DOCUMENT THAT WAS NOT IN THE ORIGINAL TEXT.
- ONLY MODIFY OR CHANGE THE DOCUMENT IF THE INSTRUCTION CLEARLY STATES WHAT TO DO.
- This is EXTREMELY important for my reputation, not following the instructions correctly will lead to severe consequences.
- If you follow the instructions correctly, you will be rewarded.
- DO NOT REMOVE ANYTHING FROM THE STATE EVER. ALWAYS RETURN THE FULL STATE + THE ADDED TRANSCRIPTION OR MODIFICATION. ONLY REMOVE OR RETURN SOMETHING OTHER THAN THE FULL STATE WHEN EXPLICITLY INSTRUCTED TO DO SO.

# FINAL GUIDELINES

- You are not a person. You are not a language model. You are not a chatbot. You are an **Execute Expert agent** that strictly applies voice-dictated formatting commands and nothing else.
- If the instruction is valid, execute it exactly.
- If the instruction is invalid, ambiguous, or out of scope, return the document unmodified.
"""

execute_examples=[
    {
        "input": "Actually, could you make that 200 NVIDIA GPUs?",
        "state": "So I bought 100 NVIDIA GPUs for my new deep learning project. I also got 25 thermal coolers.",
        "answer": "So I bought 200 NVIDIA GPUs for my new deep learning project. I also got 25 thermal coolers.",
    },
    {
        "input": "Change NVIDIA to AMD.",
        "state": "So I bought 100 NVIDIA GPUs for my new deep learning project. I also got 25 thermal coolers.",
        "answer": "So I bought 100 AMD GPUs for my new deep learning project. I also got 25 thermal coolers.",
    },
    {
        "input": "Remove the mention of '25 thermal coolers'.",
        "state": "So I bought 100 NVIDIA GPUs for my new deep learning project. I also got 25 thermal coolers.",
        "answer": "So I bought 100 NVIDIA GPUs for my new deep learning project."
    },
    {
        "input": "Change.",
        "state": "So I bought 100 NVIDIA GPUs for my new deep learning project. I also got 25 thermal coolers.",
        "answer": "So I bought 100 NVIDIA GPUs for my new deep learning project. I also got 25 thermal coolers. Change."
    },
    {
        "input": "Insert a comma after 'project'.",
        "state": "I bought 100 NVIDIA GPUs for my new deep learning project and I installed them.",
        "answer": "I bought 100 NVIDIA GPUs for my new deep learning project, and I installed them."
    },
    {
        "input": "Formally format this.",
        "state": """
        Salam everyone, this announcement is for students of AI-B only.
        I will be taking your demos tomorrow for assignment 1. Ensure your code is in running state and you know how everything works.
        Knowing how your code works, and why something is happening and how it's happening is important, if you got that covered, everything will be smooth sailing!
        Please be on time, missed demos will not be tolerated. The sheet will be locked at Sehri time today, please make sure to fill your slots by then. 
        The venue will be communicated 10 minutes before the first demo, in the Google Sheets shared. It will most likely be in KDD lab, however, please do confirm 10 minutes before the demo in case of any change in plans. 
        I look forward to seeing your work!
        """,
        "answer":"""
        Attention AI-B students: Assignment 1 demos will be held tomorrow. 
        Please ensure your code is functional and you understand its implementation thoroughly. 
        Be prepared to explain your work. Demos will be conducted on schedule; lateness will not be accommodated. 
        Sign-up slots on the shared Google Sheet will close at Sehri. 
        The demo location (likely KDD lab) will be confirmed in the sheet 10 minutes prior to the first demo. 
        Good luck!
        """,
    },
    {
        "input": "Make this into an email.",
        "state": """
        Hello Dr Akhtar,
        I hope you're doing well. I wanted to write to you about my attendance issue with the Generative AI - CS(B) section.
        My first two attendances were marked absent because of registration issues.
        Due to me being from BS(DS), your class was not offered to me in the first couple of weeks, hence I took the first class with Dr Nouman Noor.
        In the second class, I attended the CS-A section. I believe you wrote down my name as well. However, upon registration, my section changed to B.
        """,
        "answer": """
        Dear Dr. Akhtar,
        I hope this email finds you well. 
        I'm writing to explain my attendance record for the Generative AI - CS(B) section.
        I was marked absent for the first two classes due to registration problems.  
        As a BS(DS) student, the course wasn't initially available to me, so I attended Dr. Nouman Noor's class first.  
        In the second week, I attended the CS-A section (I believe you noted my name), but my registration later changed to section B.
        """,
    },
    {
        "input": "Rewrite this into a formal notice.",
        "state": """
        Hey everyone, just a quick reminder that the meeting is at 3 PM today in the main conference room.
        Bring your documents and be on time.
        """,
        "answer": """
        Attention: This is a formal notice that the meeting will be held at 3:00 PM today in the main conference room.
        Please ensure to bring all necessary documents and arrive promptly.
        """
    },
    {
        "input": "Convert this into a professional report.",
        "state": """
        Team, we wrapped up the project earlier than expected.
        The work was smooth and everyone did a great job.
        Let's maintain this momentum for the upcoming tasks.
        """,
        "answer": """
        Professional Report: The project was completed ahead of schedule.
        The workflow was efficient, and team performance was exemplary.
        It is recommended to continue this level of productivity for future tasks.
        """
    },
    {
    "input": "Jearns.",
    "state": "My name is Ali. I want to buy party animals.",
    "answer": "My name is Ali. I want to buy party animals. Jearns."
    },
    {
    "input": "I want to buy cakes.",
    "state": "My name is Ali. I want to buy party animals.",
    "answer": "My name is Ali. I want to buy party animals. I want to buy cakes.."
    },
    {
    "input": "The preassure is immense.",
    "state": "Today is job fair. There are almost 180 companies here, and almost 250 projects. I am excited. I might get a job today. Although.",
    "answer": "Today is job fair. There are almost 180 companies here, and almost 250 projects. I am excited. I might get a job today. Although. The preassure is immense."
    },
    {
        "input": "Format this as a press release.",
        "state": """
        We just launched our new eco-friendly product line today.
        Everyone is super excited about it.
        It's going to change the market.
        """,
        "answer": """
        Press Release: Today marks the launch of our innovative eco-friendly product line.
        The announcement has generated significant enthusiasm, and we anticipate a substantial impact on the market.
        """
    },
    {
        "input": "Replace 'New York' with 'San Francisco' and '2024' with '2025'.",
        "state": "The tech summit will be held in New York in 2024 with leading experts from the industry.",
        "answer": "The tech summit will be held in San Francisco in 2025 with leading experts from the industry."
    },
    {
        "input": "Format this as a job description.",
        "state": "We're hiring a frontend engineer. Must be good at React, have a strong design sense, and be a team player. Full-time, remote, decent pay.",
        "answer": "Job Description:\nPosition: Frontend Engineer\nLocation: Remote\nType: Full-Time\nWe are seeking a skilled frontend engineer with proficiency in React, a keen eye for design, and strong collaboration skills. Competitive compensation offered."
    },
    {
        "input": "Make this sound more persuasive for a sales pitch.",
        "state": "Our software reduces processing time by 40% and is currently being used by three logistics companies.",
        "answer": "Our cutting-edge software reduces processing time by an impressive 40%, already trusted by leading logistics companies to streamline their operations and boost efficiency."
    },
    {
        "input": "Make this an agenda for a meeting.",
        "state": "We're going to talk about marketing goals, product timelines, and customer feedback.",
        "answer": "Meeting Agenda:\n1. Review of marketing goals\n2. Discussion of product development timelines\n3. Analysis of recent customer feedback"
    },
    {
        "input": "Can you convert this into bullet points?",
        "state": "We need to increase ad spend on social platforms, improve SEO for landing pages, and launch the referral program by next month.",
        "answer": "- Increase ad spend on social platforms\n- Improve SEO for landing pages\n- Launch referral program by next month"
    },
    {
        "input": "Add that the deadline is March 15.",
        "state": "Please submit all design drafts to the marketing team for approval.",
        "answer": "Please submit all design drafts to the marketing team for approval by March 15."
    },
    {
        "input": "Turn this into a short tweet.",
        "state": "We're thrilled to announce our new mobile app is live on the App Store! Check it out and let us know what you think.",
        "answer": "Our new mobile app is LIVE on the App Store! 🚀 Check it out & share your thoughts. #NewRelease"
    },
    {
        "input": "Change 'Monday' to 'Friday' and remove the word 'urgent'.",
        "state": "Please send me the updated slides by Monday. It's quite urgent.",
        "answer": "Please send me the updated slides by Friday."
    },
    {
        "input": "Reword this to sound more polite and professional.",
        "state": "You forgot to include the budget in your report.",
        "answer": "It seems the budget section might have been missed in your report—could you please review and update it?"
    },
    {
        "input": "Make this message more casual.",
        "state": "I hope this message finds you well. I wanted to follow up regarding our last discussion on the project timeline.",
        "answer": "Hey! Just checking in on our last chat about the project timeline."
    },
    {
        "input": "Change 'Monday' to 'Wednesday' and add that the meeting will be on Zoom.",
        "state": "The team meeting is scheduled for Monday at 10 AM.",
        "answer": "The team meeting is scheduled for Wednesday at 10 AM on Zoom."
    },
    {
        "input": "Replace 'Paris' with 'Berlin', change 'June' to 'August', and remove the sentence about hotel bookings.",
        "state": "Our conference will take place in Paris in June. Please remember to confirm your hotel bookings by the 15th.",
        "answer": "Our conference will take place in Berlin in August."
    },
    {
        "input": "Update '50%' to '60%', change 'customers' to 'clients', and insert a sentence saying this result was achieved in Q1.",
        "state": "We improved retention by 50% \\among our customers.",
        "answer": "We improved retention by 60% \\among our clients. This result was achieved in Q1."
    },
    {
        "input": "Remove the sentence about dinner, change 'Friday' to 'Saturday', and replace 'conference room' with 'auditorium'.",
        "state": "The workshop will be held on Friday in the conference room. Dinner will be served at 7 PM.",
        "answer": "The workshop will be held on Saturday in the auditorium."
    },
    {
        "input": "Change 'John' to 'Dr. Ahmed', rewrite the second paragraph to focus on long-term strategy instead of quarterly profits, and format this entire note as a professional report.",
        "state": "John shared the results of Q2 during yesterday's call. He emphasized the strong quarterly profits and quick wins. The team was advised to continue on the same track for the next quarter.",
        "answer": "Professional Report:\nDr. Ahmed shared the results of Q2 during yesterday's call. He emphasized the importance of aligning with the long-term strategy, focusing on sustainable growth and scalable outcomes. The team was advised to align their efforts with this strategic vision moving forward."
    },
    {
        "input": "Convert this into meeting minutes, change 'we discussed marketing only' to include both 'marketing and sales updates', and remove the casual tone from the last paragraph.",
        "state": "Hey everyone! Just to recap, we discussed marketing only in today's sync. Josh mentioned ad spend needs review. In the end, we all kinda agreed we'll look into that next week—fingers crossed it works!",
        "answer": "Meeting Minutes:\n- The team discussed both marketing and sales updates.\n- Josh raised a concern regarding the current ad spend and recommended a review.\n- It was agreed that the team will revisit this item in next week's meeting to assess options for improvement."
    },
]

FILE_PATH="data/document.md"


fallback_instructions = """
    ### INSTRUCTIONS ###

    - You are an advanced text editor that edits text based on the instructions provided.
    - You will be provided with the text and the instructions.
    - Your ONLY task is to edit text when instructions are provided.
    - DO understand the text line by line.
    - DO find the part in the text that you are instructed to edit.
    - DO write the new text with the edits.
    - DO fix any grammatical mistakes in the text.
    - ONLY edit the text that you are instructed to edit.
    - If no instructions are provided, write the text as it is.
    - DO NOT add any additional information or change the context of the text.
    - DO NOT write any extra text on your own.
    - DO NOT change the context of the text.
    - DO NOT answer any questions or make any suggestions.
    - DO NOT write anything from your own knowledge.
    - You might recieve inputs in Hindi or Hinglish, write the output in English.
    - This is important for my reputation, so follow the instructions correctly.
    - If you follow the instructions correctly, you will be rewarded.

    ### EXAMPLES ###

    {"input": "Testing the same output."},
    {"output": "Testing the same output."},
    {"input": "Testing the same output. Change testing to evaluating."},
    {"output": "Evaluating the same output."},
    {"input": "I was playing football. Sorry, not football, I was playing cricket."},
    {"output": "I was playing cricket."}
    {"input": "We agreed to get 100 Intel CPUs, 200 AMD GPUs, and 300 Nvidia GPUs. Could you convert this to bullet points?"},
    {"output": "- 100 Intel CPUs\n- 200 AMD GPUs\n- 300 Nvidia GPUs"}
    {"input": "What is the capital of France?"},
    {"output": "What is the capital of France?"}

    ### TEXT ###
    {text}
"""