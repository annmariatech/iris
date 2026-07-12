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

const captions = await Caption.find({
    lectureId,
    timestamp: {
        $gte: new Date(startTime),
        $lte: new Date(endTime)
    }
});

const transcript = captions
    .map(c => c.text)
    .join(" ");

const summary = await generateSummary(transcript);

attentionEvent.missedTranscript = transcript;
attentionEvent.summary = summary;

await attentionEvent.save();