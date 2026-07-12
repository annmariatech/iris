import express from "express";

import {
    saveCaption
} from "../controllers/captionController.js";

const router = express.Router();

router.post("/", saveCaption);

export default router;