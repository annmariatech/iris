import Lecture from "../models/Lecture.js";

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