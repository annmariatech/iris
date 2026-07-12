import AttentionEvent from "../models/AttentionEvent.js";
import Caption from "../models/Caption.js";
import { generateSummary } from "../services/aiService.js";

export const saveAttentionEvent = async (req, res) => {

    try {

        const {
            lectureId,
            startTime,
            endTime
        } = req.body;

        const duration =
            (new Date(endTime) - new Date(startTime)) / 1000;

        const attentionEvent =
            await AttentionEvent.create({
                lectureId,
                startTime,
                endTime,
                duration
            });

        // Find captions during the distraction period
        const captions = await Caption.find({
            lectureId,
            timestamp: {
                $gte: new Date(startTime),
                $lte: new Date(endTime)
            }
        });

        // Combine captions into one transcript
        const transcript = captions
            .map(c => c.text)
            .join(" ");

        // Generate AI summary only if transcript exists
        if (transcript.trim().length > 0) {

            const summary = await generateSummary(transcript);

            attentionEvent.missedTranscript = transcript;
            attentionEvent.summary = summary;

            await attentionEvent.save();
        }

        res.status(201).json({
            success: true,
            attentionEvent
        });

    } catch (error) {

        res.status(500).json({
            success: false,
            message: error.message
        });

    }

};