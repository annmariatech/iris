import AttentionEvent from "../models/AttentionEvent.js";

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