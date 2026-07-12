export const cleanTranscript = (captions) => {

    let transcript = captions
        .map(c => c.text)
        .join(" ");

    transcript = transcript.replace(/\b(uh|umm|okay|actually|basically)\b/gi, "");

    transcript = transcript.replace(/\s+/g, " ");

    return transcript.trim();

};