import express from "express";
import dotenv from "dotenv";
import cors from "cors";
import helmet from "helmet";
import morgan from "morgan";

import connectDB from "./config/db.js";

import lectureRoutes from "./routes/lectureRoutes.js";
import captionRoutes from "./routes/captionRoutes.js";
import attentionRoutes from "./routes/attentionRoutes.js";
import noteRoutes from "./routes/noteRoutes.js";

dotenv.config();

const app = express();

app.use(cors());
app.use(helmet());
app.use(morgan("dev"));
app.use(express.json());
app.use("/api/lectures", lectureRoutes);
app.use("/api/captions", captionRoutes);
app.use("/api/attention", attentionRoutes);
app.use("/api/notes", noteRoutes);
// Health check
app.get("/", (req, res) => {
    res.status(200).json({
        success: true,
        message: "Lecture AI Backend Running 🚀"
    });
});

const PORT = process.env.PORT || 5001;

const startServer = async () => {
    try {
        await connectDB();

        app.listen(PORT, () => {
            console.log(`🚀 Server running on port ${PORT}`);
        });
    } catch (error) {
        console.error("Server failed to start:");
        console.error(error.message);
    }
};

startServer();