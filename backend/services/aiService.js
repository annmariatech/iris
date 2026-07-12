import groq from "../config/ai.js";

const MODEL = process.env.MODEL_NAME;

export const generateSummary = async (text) => {
    const response = await groq.chat.completions.create({
        model: MODEL,
        messages: [
            {
                role: "system",
                content:
                    "Summarize the following lecture transcript into 2-3 concise bullet points."
            },
            {
                role: "user",
                content: text
            }
        ],
        temperature: 0.3
    });

    return response.choices[0].message.content;
};

export const generateNotes = async (transcript) => {
    const response = await groq.chat.completions.create({
        model: MODEL,
        messages: [
            {
                role: "system",
                content:
                    `Convert this lecture transcript into study notes.

Requirements:
- Bullet points
- Remove repetitions
- Keep important concepts
- No introduction
- No conclusion`
            },
            {
                role: "user",
                content: transcript
            }
        ],
        temperature: 0.2
    });

    return response.choices[0].message.content;
};

export const classifyNotes = async (notes) => {

    const response = await groq.chat.completions.create({

        model: MODEL,

        messages: [

            {
                role: "system",
                content:
`Classify every bullet point as one of:

Question
Answer
Explanation

Return ONLY JSON.

Example:

[
{
"text":"Binary Search works on sorted arrays.",
"tag":"Explanation"
}
]`
            },

            {
                role: "user",
                content: notes
            }

        ],

        temperature: 0.1

    });

    return response.choices[0].message.content;

};