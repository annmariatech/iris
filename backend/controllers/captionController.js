import Caption from "../models/Caption.js";

export const saveCaption = async (req, res) => {

    try {

        const { lectureId, timestamp, text } = req.body;

        const caption = await Caption.create({
            lectureId,
            timestamp,
            text
        });

        res.status(201).json({
            success: true,
            caption
        });

    } catch (error) {

        res.status(500).json({
            success: false,
            message: error.message
        });

    }

};