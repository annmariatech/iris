import express from "express";

import {
    saveAttentionEvent
} from "../controllers/attentionController.js";

const router = express.Router();

router.post("/", saveAttentionEvent);

export default router;