import mongoose from "mongoose";

const noteSchema = new mongoose.Schema(
    {
        lectureId: {
            type: mongoose.Schema.Types.ObjectId,
            ref: "Lecture",
            required: true
        },

        originalText: {
            type: String,
            required: true
        },

        editedText: {
            type: String,
            default: ""
        },

        tag: {
            type: String,
            enum: [
                "Question",
                "Answer",
                "Explanation"
            ],
            default: "Explanation"
        },

        edited: {
            type: Boolean,
            default: false
        },

        source: {
            type: String,
            default: "AI"
        }
    },
    {
        timestamps: true
    }
);

export default mongoose.model("Note", noteSchema);