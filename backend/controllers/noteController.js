import Note from "../models/Note.js";

// Get all notes
export const getNotes = async (req, res) => {

    try {

        const notes = await Note.find({

            lectureId: req.params.lectureId

        });

        res.json({

            success: true,

            notes

        });

    } catch (error) {

        res.status(500).json({

            success: false,

            message: error.message

        });

    }

};

// Update a note
export const updateNote = async (req, res) => {

    try {

        const { editedText } = req.body;

        const note = await Note.findById(req.params.id);

        if (!note) {

            return res.status(404).json({

                success: false,

                message: "Note not found"

            });

        }

        note.edited = true;
        note.editedText = editedText;

        await note.save();

        res.json({

            success: true,

            note

        });

    } catch (error) {

        res.status(500).json({

            success: false,

            message: error.message

        });

    }

};