import express from "express";

import {
    startLecture,
    endLecture
} from "../controllers/lectureController.js";

const router = express.Router();

router.post("/start", startLecture);
router.post("/end", endLecture);

export default router;