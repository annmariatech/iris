import mongoose from "mongoose";

const lectureSchema = new mongoose.Schema(
    {
        title: {
            type: String,
            default: "Untitled Lecture",
            trim: true
        },

        subject: {
            type: String,
            default: "",
            trim: true
        },

        startTime: {
            type: Date,
            required: true
        },

        endTime: {
            type: Date,
            default: null
        },

        status: {
            type: String,
            enum: ["ONGOING", "COMPLETED"],
            default: "ONGOING"
        }
    },
    {
        timestamps: true
    }
);

export default mongoose.model("Lecture", lectureSchema);