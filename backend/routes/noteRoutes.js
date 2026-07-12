import express from "express";

import {
    getNotes,
    updateNote
} from "../controllers/noteController.js";

const router = express.Router();

router.get("/:lectureId", getNotes);

router.put("/:id", updateNote);

export default router;