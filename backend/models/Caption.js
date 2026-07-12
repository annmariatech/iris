import mongoose from "mongoose";

const captionSchema = new mongoose.Schema(
    {
        lectureId: {
            type: mongoose.Schema.Types.ObjectId,
            ref: "Lecture",
            required: true
        },

        timestamp: {
            type: Date,
            required: true
        },

        text: {
            type: String,
            required: true,
            trim: true
        }
    },
    {
        timestamps: true
    }
);

captionSchema.index({ lectureId: 1, timestamp: 1 });

export default mongoose.model("Caption", captionSchema);