import Lecture from "../models/Lecture.js";
import Caption from "../models/Caption.js";
import Note from "../models/Note.js";

import {
    generateNotes,
    classifyNotes
} from "../services/aiService.js";

import { cleanTranscript } from "../utils/transcriptCleaner.js";

// Start a new lecture
export const startLecture = async (req, res) => {
    try {
        const { title, subject } = req.body;

        const lecture = await Lecture.create({
            title: title || "Untitled Lecture",
            subject: subject || "",
            startTime: new Date()
        });

        res.status(201).json({
            success: true,
            lecture
        });

    } catch (error) {
        res.status(500).json({
            success: false,
            message: error.message
        });
    }
};

// End a lecture
export const endLecture = async (req, res) => {
    try {

        const { lectureId } = req.body;

        const lecture = await Lecture.findById(lectureId);

        if (!lecture) {
            return res.status(404).json({
                success: false,
                message: "Lecture not found"
            });
        }

        lecture.endTime = new Date();
        lecture.status = "COMPLETED";

        await lecture.save();

        const captions = await Caption.find({
    lectureId
}).sort({ timestamp: 1 });

const transcript = cleanTranscript(captions);

const notes = await generateNotes(transcript);

const taggedNotes = JSON.parse(
    await classifyNotes(notes)
);

for (const note of taggedNotes) {

    await Note.create({

        lectureId,

        originalText: note.text,

        tag: note.tag

    });

}

        res.json({
            success: true,
            lecture
        });

    } catch (error) {
        res.status(500).json({
            success: false,
            message: error.message
        });
    }
};